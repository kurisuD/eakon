#!/usr/bin/env python3
# coding=utf-8
"""
Air conditionner classes
"""

import logging
import sys

import bitstring

from eakon import HVAC
from eakon.enums import daikin_enum


class Daikin(HVAC):
    """
    Daikin ARC478A5
    """
    __MARK = 433
    __ONE_SPACE = 1288
    __ZERO_SPACE = 440
    __temp_max = 30
    __temp_min = 16
    __init_mark = [__MARK, __ZERO_SPACE] * 5
    __start_mark = [__MARK, 25194, 3495, 1746]

    frame = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, enum=daikin_enum)
        self.one_mark = self.__MARK
        self.one_space = self.__ONE_SPACE
        self.zero_mark = self.__MARK
        self.zero_space = self.__ZERO_SPACE

    def _get_wave(self):
        wave = self.__init_mark.copy()
        wave.extend(self.__start_mark)

        for x in self._get_bitstring_frame1():
            wave.extend(self._get_zero() if x == "0" else self._get_one())
        wave.extend(self.__start_mark)

        for x in self._get_bitstring_frame2():
            wave.extend(self._get_zero() if x == "0" else self._get_one())
        wave.extend([self.__MARK])

        return wave

    def _get_bitstring(self):
        return self._get_bitstring_frame1() + self._get_bitstring_frame2()

    def _get_bitstring_frame1(self):
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
        uint: 8 = cs
        """

        data = {
            'h1': 0x11,
            'h2': 0xda,
            'h3': 0x27,
            "b1": 0x00,
            "b2": 0x02,
            "b3": 0x00,
            "b4": 0x00,
            "b5": 0x00,
            "b6": 0x00,
            "b7": 0x00,
            "b8": 0x00,
            "b9": 0x00 if self.power == self.enum.Power.ON else 0x80,
            "b10": self.fan_vertical_mode.value if self.fan_vertical_mode != self.enum.FanVerticalMode.SWING else 0x0,
            "b11": 0x00,
            "b12": 0x00,
            "b13": 0x00,
            "b14": 0x00,
            "b15": 0x00,
            "b16": 0x00
        }

        self._reverse_endianness_and_get_checksum(data)

        return bitstring.pack(fmt, **data).bin

    def _get_bitstring_frame2(self):
        fmt = """
                uint: 8 = h1,
                uint: 8 = h2,
                uint: 8 = h3,
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
                uint: 8 = cs,                
                """

        data = {
            'h1': 0x11,
            'h2': 0xda,
            'h3': 0x27,
            "b18": 0x00,
            "b19": 0x00,
            "b20": self._get_power_and_mode(),
            "b21": self._get_temp_intcode(),
            "b22": self._get_humidity_setting(),
            "b23": self._get_swing_and_force(),
            "b24": 0x00,
            "b25": 0x00,
            "b26": 0x06,
            "b27": 0x60,
            "b28": 0x00,
            "b29": 0x00,
            "b30": 0xc3,
            "b31": 0x00,
            "b32": 0x00
        }

        self._reverse_endianness_and_get_checksum(data)

        return bitstring.pack(fmt, **data).bin

    @staticmethod
    def _reverse_endianness_and_get_checksum(data):
        checksum = 0
        for b in data.values():
            checksum += b
        for k, b in data.items():
            b = bitstring.Bits(uint=b, length=8)
            b._reverse()
            data[k] = b.uint

        try:
            cs = bitstring.Bits(uint=checksum & 0xff, length=8)
        except bitstring.CreationError:
            from pprint import pformat
            logging.exception("Checksum value before reverse was {}".format(checksum))
            logging.exception("Checksum value before reverse after masking : {}".format(checksum & 0xff))
            logging.exception("data was\r\n{}".format(pformat(data)))
            sys.exit(0)
        cs._reverse()
        checksum = {
            "cs": cs.uint
        }
        data.update(checksum)

    def _get_temp_intcode(self):
        if self.mode in (self.enum.Mode.COOL, self.enum.Mode.HEAT):
            return self.temperature * 2
        elif self.mode in (self.enum.Mode.DRY, self.enum.Mode.AUTO):
            return 0x3  # TODO : review
        else:
            return 0xc  # TODO : review

    def _get_power_and_mode(self):
        return (bitstring.Bits(uint=self.mode.value, length=4) + bitstring.Bits(uint=self.power.value, length=4)).uint

    def _get_humidity_setting(self):
        if self.mode in (self.enum.Mode.COOL, self.enum.Mode.FAN):
            return 0x0
        else:
            # more settings available according to http://nandra.segv.jp/ir-remote/daikin2.html
            # not available on ARC478A5, so skipping code, setting to auto
            return 0x8

    def _get_swing_and_force(self):
        swing = 0xf if self.fan_vertical_mode == self.enum.FanVerticalMode.SWING else 0x0
        return (bitstring.Bits(uint=self.fan_power.value, length=4) + bitstring.Bits(uint=swing, length=4)).uint


def _test_daikin(send_ir=False):
    from pap_logger import PaPLogger
    import sys
    import pigpio
    import AnaviInfraredPhat
    from time import sleep

    PaPLogger(level=logging.INFO, verbose_fmt=True)
    hvac = Daikin()
    hvac.power = daikin_enum.Power.ON
    hvac.temperature = 21
    hvac.mode = daikin_enum.Mode.COOL
    hvac.fan_vertical_mode = daikin_enum.FanVerticalMode.TOP

    logging.info("\r{}".format(hvac))
    logging.info(hvac.bitstring)
    logging.info(hvac.wave)

    hvac.power = daikin_enum.Power.OFF
    logging.info("\r{}".format(hvac))
    logging.info(hvac.bitstring)
    logging.info(hvac.wave)
    if send_ir:
        pi = pigpio.pi("node1", 8888)
        if not pi.connected:
            logging.error("Could not connect to pigpiod on node2")
            sys.exit(0)
        anavi_phat = AnaviInfraredPhat.IRSEND(pi, r"/proc/cpuinfo")
        hvac = Daikin()
        hvac.power = daikin_enum.Power.ON

        temp = 21
        for mode in [daikin_enum.Mode.AUTO, daikin_enum.Mode.COOL, daikin_enum.Mode.DRY, daikin_enum.Mode.HEAT]:
            for vert in (
                    daikin_enum.FanVerticalMode.TOP, daikin_enum.FanVerticalMode.TOP_MIDDLE,
                    daikin_enum.FanVerticalMode.MIDDLE,
                    daikin_enum.FanVerticalMode.BOTTOM_MIDDLE, daikin_enum.FanVerticalMode.BOTTOM,
                    daikin_enum.FanVerticalMode.SWING):
                for fp in (daikin_enum.FanPower.AUTO, daikin_enum.FanPower.FORCE1, daikin_enum.FanPower.FORCE2,
                           daikin_enum.FanPower.FORCE3, daikin_enum.FanPower.FORCE4, daikin_enum.FanPower.FORCE5,
                           daikin_enum.FanPower.QUIET):
                    hvac.temperature = temp
                    hvac.mode = mode
                    hvac.fan_vertical_mode = vert
                    hvac.fan_power = fp
                    logging.info("\r{}".format(hvac))
                    logging.info(hvac.bitstring)
                    logging.info(hvac.wave)
                    anavi_phat.send_ir(code=hvac.wave)
                    sleep(15)
                    temp += 1

        hvac.mode = daikin_enum.Mode.AUTO
        hvac.fan_vertical_mode = daikin_enum.FanVerticalMode.TOP
        hvac.fan_power = daikin_enum.FanPower.AUTO
        anavi_phat.send_ir(code=hvac.wave)

        sleep(15)
        hvac.power = daikin_enum.Power.OFF
        logging.info("\r{}".format(hvac))
        logging.info(hvac.bitstring)
        logging.info(hvac.wave)
        anavi_phat.send_ir(code=hvac.wave)


if __name__ == '__main__':
    _test_daikin()
