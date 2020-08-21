#!/usr/bin/env python3
# coding=utf-8
"""
Hitachi air conditionner classes
"""
import logging

import bitstring

from eakon import HVAC
from eakon.enums import hitachi_enum


class Hitachi(HVAC):
    """
    Mitsubishi FG86
    """
    __HDR_FIRST_MARK = 29785
    __HDR_FIRST_SPACE = 49362
    __HDR_SECOND_MARK = 3388
    __HDR_SECOND_SPACE = 1657
    __MARK = 428
    __ONE_SPACE = 1245
    __ZERO_SPACE = 410
    __temp_max = 32
    __temp_min = 16
    __mark = [__HDR_FIRST_MARK, __HDR_FIRST_SPACE, __HDR_SECOND_MARK, __HDR_SECOND_SPACE]

    frame = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, enum=hitachi_enum)
        self.one_mark = self.__MARK
        self.one_space = self.__ONE_SPACE
        self.zero_mark = self.__MARK
        self.zero_space = self.__ZERO_SPACE

    def _get_wave(self):

        wave = self.__mark.copy()
        for x in self._get_bitstring():
            wave.extend(self._get_zero() if x == "0" else self._get_one())
        wave.extend([self.__MARK])
        return wave

    def _get_bitstring(self):
        fmt = """
        uint: 8 = h1,
        uint: 8 = h2,
        uint: 8 = h3,
        uint: 8 = b1,
        uint: 8 = b2,
        uint: 8 = b3,
        uint: 8 = b4,
        uint: 8 = b5,
        uint: 8 = b6,
        uint: 8 = b7,
        uint: 8 = b8,
        uint: 8 = b9,
        uint: 8 = b10,
        uint: 8 = b11,
        uint: 8 = b12,
        uint: 8 = b13,
        uint: 8 = b14,
        uint: 8 = b15,
        uint: 8 = b16,
        uint: 8 = b17,
        uint: 8 = b18,
        uint: 8 = b19,
        uint: 8 = b20,
        uint: 8 = b21,
        uint: 8 = b22,
        uint: 8 = b23,
        uint: 8 = b24,
        uint: 8 = b25,
        uint: 8 = b26,
        uint: 8 = b27,
        uint: 8 = b28,
        uint: 8 = b29,
        uint: 8 = b30,
        uint: 8 = b31,
        uint: 8 = b32,
        uint: 8 = b33,
        uint: 8 = b34,
        uint: 8 = b35,
        uint: 8 = b36,
        uint: 8 = b37,
        uint: 8 = b38,
        uint: 8 = b39,
        uint: 8 = b40,
        uint: 8 = b41,
        uint: 8 = b42,
        uint: 8 = b43,
        uint: 8 = b44,
        uint: 8 = b45,
        uint: 8 = b46,
        uint: 8 = b47,
        uint: 8 = b48,
        uint: 8 = b49,
        uint: 8 = b50
        """

        header = {'h1': 0x80,
                  'h2': 0x08,
                  'h3': 0x00
                  }
        pre_data = {
            1: 0x02,
            3: 0xff,
            5: 0x33,
            7: 0x49,
            9: 0xc2 if self.temperature == self.__temp_min else 0x22,
            11: self._get_temp_intcode(),
            13: 0x00,
            15: 0x00,
            17: 0x00,
            19: 0x00,
            21: 0x00,
            23: self.mode.value,
            25: 0x0f,  # AH AH
            27: 0x00,
            29: 0x00,
            31: 0x01,
            33: 0xc0,
            35: 0x80,
            37: 0x11,
            39: 0x00,
            41: 0x00,
            43: 0xff,
            45: 0xff,
            47: 0xff,
            49: 0xff,
        }
        data = {}
        for k, v in pre_data.items():
            data["b{}".format(k)] = v
            data["b{}".format(k + 1)] = (~bitstring.Bits(uint=v, length=8)).uint

        bitstring_dict = header
        bitstring_dict.update(data)
        return bitstring.pack(fmt, **bitstring_dict).bin

    def _get_temp_intcode(self):
        temp = bitstring.pack('uint:4=temp',
                              **{'temp': 0 if self.temperature == self.__temp_max else self.temperature - 16})
        temp.reverse()
        return bitstring.pack('uint:2=zero,uint:4=inv_temp,uint:2=max_temp',
                              **{'zero': 0,
                                 'inv_temp': temp.uint,
                                 'max_temp': 1 if self.temperature == self.__temp_max else 2}).int


def _test_hitachi(send_ir=False):
    from pap_logger import PaPLogger
    import sys
    import pigpio
    import AnaviInfraredPhat
    from time import sleep
    anavi_phat = None

    PaPLogger(level=logging.INFO, verbose_fmt=True)

    if send_ir:

        pi = pigpio.pi("node0", 8888)
        if not pi.connected:
            logging.error("Could not connect to pigpiod on node0")
            sys.exit(0)

        anavi_phat = AnaviInfraredPhat.IRSEND(pi, r"/proc/cpuinfo")

    for mode in [hitachi_enum.Mode.COOL, hitachi_enum.Mode.DRY, hitachi_enum.Mode.HEAT]:
        for temp in range(16, 33):
            hvac = Hitachi(temperature=temp, mode=mode)
            logging.info("{}_{} : {}".format(hvac.mode, hvac.temperature, hvac.bitstring))
            logging.info("{}_{} : {}".format(hvac.mode, hvac.temperature, hvac.wave))
            if send_ir:
                anavi_phat.send_ir(code=hvac.wave)
                sleep(5)


if __name__ == '__main__':
    _test_hitachi()
