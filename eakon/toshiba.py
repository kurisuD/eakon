#!/usr/bin/env python3
# coding=utf-8
"""
Air conditionner classes
"""

import logging

import bitstring

from eakon import HVAC
from eakon.enums import toshiba_enum


class Toshiba(HVAC):
    """
    Mitsubishi FG86
    """
    __HDR_FIRST_MARK = 4439
    __HDR_FIRST_SPACE = 4708
    __MARK = 562
    __ONE_SPACE = 1593
    __ZERO_SPACE = 521
    __temp_max = 30
    __temp_min = 16
    __start_mark = [__HDR_FIRST_MARK, __HDR_FIRST_SPACE]
    __repeat_mark = [__HDR_FIRST_SPACE, __HDR_FIRST_MARK, __HDR_FIRST_SPACE]

    frame = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, enum=toshiba_enum)
        self.one_mark = self.__MARK
        self.one_space = self.__ONE_SPACE
        self.zero_mark = self.__MARK
        self.zero_space = self.__ZERO_SPACE

    def _get_wave(self):
        wave = self.__start_mark.copy()
        for x in self._get_bitstring():
            wave.extend(self._get_zero() if x == "0" else self._get_one())
        wave.extend([self.__MARK])

        wave.extend(self.__repeat_mark)

        for x in self._get_bitstring():
            wave.extend(self._get_zero() if x == "0" else self._get_one())
        wave.extend([self.__MARK])

        wave.extend(self.__repeat_mark)

        for x in self._get_footer():
            wave.extend(self._get_zero() if x == "0" else self._get_one())
        wave.extend([self.__MARK])

        return wave

    def _get_bitstring(self):
        fmt = """
        uint: 8 = h1,
        uint: 8 = h2,
        uint: 4 = n5,
        uint: 4 = n6,
        uint: 4 = n7,
        uint: 4 = n8,
        uint: 4 = n9,
        uint: 4 = n10,
        uint: 4 = n11,
        uint: 4 = n12
        """

        data = {
            'h1': 0xc2,
            'h2': 0x3d,
            "n5": self._get_n5(),  # fan vertical mode ?
            "n6": 0xf,
            "n7": (~bitstring.Bits(uint=self._get_n5(), length=4)).uint,
            "n8": 0x0,
            "n9": self._get_temp_intcode(),
            "n10": self.mode.value,
            "n11": (~bitstring.Bits(uint=self._get_temp_intcode(), length=4)).uint,
            "n12": (~bitstring.Bits(uint=self.mode.value, length=4)).uint
        }

        return bitstring.pack(fmt, **data).bin

    def _get_n5(self):
        if self.mode == self.enum.Mode.AUTO or self.mode == self.enum.Mode.DRY:
            return 0x1
        else:
            return 0xb

    def _get_temp_intcode(self):
        temp_dict = {
            16: 0,  # WEIRD
            17: 0,
            18: 1,
            19: 3,
            20: 2,
            21: 6,
            22: 7,
            23: 5,
            24: 4,
            25: 12,
            26: 13,
            27: 9,
            28: 8,
            29: 10,
            30: 11
        }
        assert self.temperature in temp_dict.keys()
        return temp_dict[self.temperature]

    def _get_footer(self):
        fmt = """
        uint: 8 = b1,
        uint: 8 = b2,
        uint: 8 = b3,
        uint: 8 = b4,
        uint: 8 = b5,
        uint: 8 = b6,
        """

        def get_b6():
            if self.temperature > self.__temp_min:
                return 0x3a if self.mode in (self.enum.Mode.AUTO, self.enum.Mode.DRY) else 0x3b
            else:
                return 0x4a if self.mode in (self.enum.Mode.AUTO, self.enum.Mode.DRY) else 0x4b

        data = {
            'b1': 0xd5,
            'b2': 0x65 if self.mode in (self.enum.Mode.AUTO, self.enum.Mode.DRY) else 0x66,
            "b3": 0x00,
            "b4": 0x00 if self.temperature > self.__temp_min else 0x10,
            "b5": 0x00,
            "b6": get_b6(),
        }

        return bitstring.pack(fmt, **data).bin


def _test_toshiba(send_ir=False):
    from pap_logger import PaPLogger
    import sys
    import pigpio
    import AnaviInfraredPhat
    from time import sleep
    anavi_phat = None

    PaPLogger(level=logging.INFO, verbose_fmt=True)

    if send_ir:
        pi = pigpio.pi("node2", 8888)
        if not pi.connected:
            logging.error("Could not connect to pigpiod on node2")
            sys.exit(0)

        anavi_phat = AnaviInfraredPhat.IRSEND(pi, r"/proc/cpuinfo")

    for mode in [toshiba_enum.Mode.COOL, toshiba_enum.Mode.COOL, toshiba_enum.Mode.DRY, toshiba_enum.Mode.HEAT]:
        for temp in range(16, 31):
            hvac = Toshiba(temperature=temp, mode=mode)
            logging.info("{}_{} : {}".format(hvac.mode, hvac.temperature, hvac.bitstring))
            logging.info("{}_{} : {}".format(hvac.mode, hvac.temperature, hvac.wave))
            if send_ir:
                anavi_phat.send_ir(code=hvac.wave)
                sleep(5)


if __name__ == '__main__':
    _test_toshiba()
