#!/usr/bin/env python3
# coding=utf-8
"""
Panasonic HVAC enumerations classes
Taken from https://qiita.com/awawaInu/items/25c6e17fcc2e655d5d42
Half degrees aren't implemented.
"""
from enum import Enum


class Power(Enum):
    """
    Power
    """
    UNDEFINED = None
    OFF = 0b0000
    ON = 0b1000


class Mode(Enum):
    """
    Mode
    """
    DRY = 0b0010
    COOL = 0b1100
    HEAT = 0b0100
    UNDEFINED = DRY


class FanVerticalMode(Enum):
    """
    Fan vertical sweeping
    """
    SWING = 0b000
    TOP = 0b0100
    MID_TOP = 0b1100
    MIDDLE = 0b0010
    MID_BOTTOM = 0b1010
    BOTTOM = 0b1111
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
    FORCE2 = 0b1010
    FORCE3 = 0b1110
    FORCE4 = 0b0101
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
            }


if __name__ == '__main__':
    print([FanVerticalMode])
    print(list(map(str, FanVerticalMode)))
