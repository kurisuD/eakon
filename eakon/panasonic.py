#!/usr/bin/env python3
# coding=utf-8
"""
Panasonic air conditioner classes
"""
import logging
import sys

import bitstring

from eakon import HVAC
from eakon.enums import panasonic_enum


def _convert_byte_endianness(byte: str) -> str:
    assert len(byte) == 8
    byte = list(byte)
    byte.reverse()
    return "".join(byte)


def _convert_int_endianness(val: int) -> int:
    assert 0 <= val <= 255
    return int(_convert_byte_endianness("{:08b}".format(val)), 2)


class Panasonic(HVAC):
    """
    Panasonic basic remote control
    """

    __INTER_FRAME_SPACE = 10022
    __HDR_FIRST_MARK = 3488
    __HDR_FIRST_SPACE = 1729
    __MARK = 444
    __ONE_SPACE = 1295
    __ZERO_SPACE = 429
    # __INTER_FRAME_SPACE = 10000
    # __HDR_FIRST_MARK = 3500
    # __HDR_FIRST_SPACE = 1750
    # __MARK = 444
    # __ONE_SPACE = 1300
    # __ZERO_SPACE = 430
    __temp_max = 30
    __temp_min = 16
    __start_mark = [__HDR_FIRST_MARK, __HDR_FIRST_SPACE]
    __inter_frame_mark = [__MARK, __INTER_FRAME_SPACE]

    frame = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, enum=panasonic_enum)
        self.one_mark = self.__MARK
        self.one_space = self.__ONE_SPACE
        self.zero_mark = self.__MARK
        self.zero_space = self.__ZERO_SPACE

    def _get_wave(self):

        wave = self.__start_mark.copy()
        # for x in self._get_bitstring_frame1():
        #     wave.extend(self._get_zero() if x == "0" else self._get_one())
        # wave.extend(self.__inter_frame_mark)
        # wave.extend(self.__start_mark)

        for x in self._get_bitstring_frame2():
            wave.extend(self._get_zero() if x == "0" else self._get_one())
        wave.extend([self.__MARK])
        return wave

    def _get_bitstring(self):
        return self._get_bitstring_frame2()

    def _get_bitstring_frame1(self):
        fmt = """
        uint: 8 = b1,
        uint: 8 = b2,
        uint: 8 = b3,
        uint: 8 = b4,
        uint: 8 = b5,
        uint: 8 = b6,
        uint: 8 = b7,
        uint: 8 = b8
        """

        frame1_data = {
            "b1": 0x02,
            "b2": 0x20,
            "b3": 0xe0,
            "b4": 0x04,
            "b5": 0x00,
            "b6": 0x00,
            "b7": 0x00,
            "b8": 0x06,
        }
        self._reverse_endianness(frame1_data)
        # data = {}
        # for k, v in frame1_data.items():
        #     data["b{}".format(k)] = v
        #     data["b{}".format(k + 1)] = (~bitstring.Bits(uint=v, length=8)).uint

        return bitstring.pack(fmt, **frame1_data).bin

    def _get_bitstring_frame2(self):
        fmt = """
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
        uint: 8 = b19
        """

        frame2_data = {
            "b1": 0x02,
            "b2": 0x20,
            "b3": 0xe0,
            "b4": 0x04,
            "b5": 0x00,
            "b6": self._get_power_status_and_mode(),
            "b7": _convert_int_endianness(2 * self.temperature),
            "b8": 0x80,
            "b9": self._get_fan_settings(),
            "b10": 0x00,
            "b11": 0x00,
            "b12": 0x06,
            "b13": 0x60,
            "b14": self._get_extra_fan_settings(),
            "b15": 0x02,
            "b16": 0x80,
            "b17": 0x00,
            "b18": 0x06,
            "b19": 0x84,

        }
        self._reverse_endianness(frame2_data)
        # data = {}
        # for k, v in frame1_data.items():
        #     data["b{}".format(k)] = v
        #     data["b{}".format(k + 1)] = (~bitstring.Bits(uint=v, length=8)).uint
        self._get_checksum(frame2_data)
        return bitstring.pack(fmt, **frame2_data).bin

    @staticmethod
    def _get_checksum(data):
        checksum = 0
        for b in data.values():
            checksum += b

        try:
            cs = bitstring.Bits(uint=checksum & 0xff, length=8)
        except bitstring.CreationError:
            from pprint import pformat
            logging.exception("Checksum value before reverse was {}".format(checksum))
            logging.exception("Checksum value before reverse after masking : {}".format(checksum & 0xff))
            logging.exception("data was\r\n{}".format(pformat(data)))
            sys.exit(0)
        # cs._reverse()
        checksum = {
            "cs": cs.uint
        }
        data.update(checksum)

    def _get_power_status_and_mode(self):
        rtn = self.enum.Power(self.power).value + self.mode.value
        # print(rtn," - ",hex(rtn))
        return rtn

    @staticmethod
    def _reverse_endianness(data):
        for k, b in data.items():
            b = bitstring.Bits(uint=b, length=8)
            b._reverse()
            data[k] = b.uint

    def _get_temp_intcode(self):
        temp = bitstring.pack('uint:4=temp',
                              **{'temp': 0 if self.temperature == self.__temp_max else self.temperature - 16})
        temp.reverse()
        return bitstring.pack('uint:2=zero,uint:4=inv_temp,uint:2=max_temp',
                              **{'zero': 0,
                                 'inv_temp': temp.uint,
                                 'max_temp': 1 if self.temperature == self.__temp_max else 2}).int

    def _get_fan_settings(self):
        rtn = self.enum.FanVerticalMode(self.fan_vertical_mode).value + self.enum.FanPower(self.fan_power).value
        return rtn

    def _get_extra_fan_settings(self):
        return self.enum.FanHighPower(self.fan_high_power).value + self.enum.RoomClean(self.room_clean).value


def _test_panasonic(send_ir=False):
    from pap_logger import PaPLogger
    import sys
    import pigpio
    import AnaviInfraredPhat
    from time import sleep
    anavi_phat = None

    PaPLogger(level=logging.INFO, verbose_fmt=True)

    if send_ir:

        pi = pigpio.pi("node1.warwick.local", 8888)
        if not pi.connected:
            logging.error("Could not connect to pigpiod on node1")
            sys.exit(0)

        anavi_phat = AnaviInfraredPhat.IRSEND(pi, r"/proc/cpuinfo")

    # for mode in [panasonic_enum.Mode.COOL, panasonic_enum.Mode.DRY, panasonic_enum.Mode.HEAT]:
    #     for temp in range(16, 17):
    hvac = Panasonic(power=panasonic_enum.Power.ON, temperature=17, mode=panasonic_enum.Mode.COOL)
    logging.info("{}_{} : {}".format(hvac.mode, hvac.temperature, hvac.bitstring))
    logging.info("{}_{} : {}".format(hvac.mode, hvac.temperature, hvac.wave))
    if send_ir:
        anavi_phat.send_ir(code=hvac.wave)
        sleep(5)
        sys.exit(0)


if __name__ == '__main__':
    _test_panasonic(send_ir=False)
