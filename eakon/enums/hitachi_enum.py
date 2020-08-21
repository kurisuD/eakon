#!/usr/bin/env python3
# coding=utf-8
"""
Hitachi HVAC enumerations classes
"""
from enum import Enum


class Power(Enum):
    """
    Power
    """
    UNDEFINED = None
    OFF = 0x00  # TODO
    ON = 0x8f  # TODO


class Mode(Enum):
    """
    Mode
    """
    DRY = 0xaa
    COOL = 0xca
    HEAT = 0x6a
    FAN = 0x84
    UNDEFINED = FAN


class FanVerticalMode(Enum):
    """
    Fan vertical sweeping
    """
    UNDEFINED = 0x0
    SWING = 0x0  # TODO
    NOSWING = 0x0  # TODO


class FanPower(Enum):
    """
    Fan power
    """
    UNDEFINED = None
    AUTO = 0x5  # TODO
    FORCE1 = 0xc  # TODO
    FORCE2 = 0x2  # TODO
    FORCE3 = 0xa  # TODO
    FORCE4 = 0x6  # TODO
    FORCE5 = 0xe  # TODO


class FanHorizontalMode(Enum):
    """
    not available
    """
    NOT_AVAILABLE = -1
    UNDEFINED = NOT_AVAILABLE


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
