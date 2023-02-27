#!/usr/bin/env python3
# coding=utf-8
"""
Daikin HVAC enumerations classes
"""
from enum import Enum


class TempRange(Enum):
    MIN = 16
    STEP = 1.0
    MAX = 30


class Power(Enum):
    """
    Daikin Power
    """
    UNDEFINED = None
    ON = 0x9
    OFF = 0x8


class Mode(Enum):
    """
    Daikin Mode
    """
    AUTO = 0x0
    DRY = 0x2
    COOL = 0x3
    HEAT = 0x4
    FAN = 0x6
    UNDEFINED = AUTO


class FanVerticalMode(Enum):
    """
    Daikin Fan vertical sweeping
    """
    SWING = 0xf
    BOTTOM = 0x50
    BOTTOM_MIDDLE = 0x40
    MIDDLE = 0x30
    TOP_MIDDLE = 0x20
    TOP = 0x10
    UNDEFINED = SWING


class FanHorizontalMode(Enum):
    """
    Daikin Fan horizontal sweeping
    """
    AREA_SWING_LEFT_CENTER = 1
    AREA_SWING_RIGHT_CENTER = 2
    AREA_SWING_FULL = 3
    AREA_KAZE_YOKE = 4
    UNDEFINED = None


class FanPower(Enum):
    """
    Daikin Fan power
    """
    AUTO = 0xa
    QUIET = 0xb
    FORCE1 = 0x3
    FORCE2 = 0x4
    FORCE3 = 0x5
    FORCE4 = 0x6
    FORCE5 = 0x7
    UNDEFINED = AUTO


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


class FanHighPower(Enum):
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
    """
    not available
    """
    NOT_AVAILABLE = -1
    UNDEFINED = NOT_AVAILABLE


def get_enums_dict():
    """

    :return:
    """
    return {"Power": Power,
            "Mode": Mode,
            "FanVerticalMode": FanVerticalMode,
            "FanHorizontalMode": FanHorizontalMode,
            "FanPower": FanPower,
            }


if __name__ == '__main__':
    print(Mode.UNDEFINED)
    print(Mode.AUTO)
