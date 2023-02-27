#!/usr/bin/env python3
# coding=utf-8
"""
Panasonic HVAC enumerations classes
Taken from https://qiita.com/awawaInu/items/25c6e17fcc2e655d5d42
also in english at https://www.analysir.com/blog/2014/12/27/reverse-engineering-panasonic-ac-infrared-protocol/
Half degrees aren't implemented.
"""
from enum import Enum


class TempRange(Enum):
    MIN = 16
    STEP = 1.0  # will need update later on
    MAX = 30


class Power(Enum):
    """
    Power
    """
    UNDEFINED = None
    OFF = 0b00001000
    ON = 0b00001001


class Mode(Enum):
    """
    Mode
    """
    FAN = 0b01100000
    DRY = 0b00100000
    COOL = 0b00110000
    HEAT = 0b01000000
    AUTO = 0b00000000
    UNDEFINED = DRY


class FanVerticalMode(Enum):
    """
    Fan vertical sweeping
    """
    TOP = 0b10000000
    MID_TOP = 0b01000000
    MIDDLE = 0b11000000
    MID_BOTTOM = 0b00100000
    BOTTOM = 0b10100000
    SWING = 0b11110000
    UNDEFINED = SWING


class FanHorizontalMode(Enum):
    """
    not available
    """
    NOT_AVAILABLE = -1
    UNDEFINED = NOT_AVAILABLE


class FanPower(Enum):
    """
    Fan power
    """
    AUTO = 0b1100
    FORCE1 = 0b0010
    FORCE2 = 0b0101
    FORCE3 = 0b1010
    FORCE4 = 0b1110
    UNDEFINED = AUTO


class FanHighPower(Enum):
    """
    Extra power settings
    """
    QUIET = 0x04
    POWERFUL = 0x80
    NORMAL = 0
    UNDEFINED = NORMAL


class WideVanneMode(Enum):
    """
    not available
    """
    NOT_AVAILABLE = -1
    UNDEFINED = NOT_AVAILABLE


class AreaMode(Enum):
    """
    not available
    """
    NOT_AVAILABLE = -1
    UNDEFINED = NOT_AVAILABLE


class FanLong(Enum):
    """
    not available
    """
    NOT_AVAILABLE = -1
    UNDEFINED = NOT_AVAILABLE


class RoomClean(Enum):
    ON = 0x02
    OFF = 0x00
    UNDEFINED = OFF


def get_enums_dict():
    """

    :return:
    """
    return {"Power": Power,
            "Mode": Mode,
            "FanVerticalMode": FanVerticalMode,
            "FanPower": FanPower,
            "FanHighPower": FanHighPower,
            "RoomClean": RoomClean,
            }


if __name__ == '__main__':
    print([FanVerticalMode])
    print(list(map(str, FanVerticalMode)))
