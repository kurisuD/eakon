#!/usr/bin/env python3
# coding=utf-8
"""
This class is a skeleton of all enumerations our parent Hvac class can access to.
All implementations of Hvac must overwrite Hvac class enum property using their own enumerations
"""
from enum import Enum


class Power(Enum):
    NOT_AVAILABLE = -1
    UNDEFINED = None


class Mode(Enum):
    NOT_AVAILABLE = -1
    UNDEFINED = NOT_AVAILABLE


class FanVerticalMode(Enum):
    NOT_AVAILABLE = -1
    UNDEFINED = NOT_AVAILABLE


class FanHorizontalMode(Enum):
    NOT_AVAILABLE = -1
    UNDEFINED = NOT_AVAILABLE


class WideVanneMode(Enum):
    NOT_AVAILABLE = -1
    UNDEFINED = NOT_AVAILABLE


class AreaMode(Enum):
    NOT_AVAILABLE = -1
    UNDEFINED = NOT_AVAILABLE


class FanPower(Enum):
    NOT_AVAILABLE = -1
    UNDEFINED = NOT_AVAILABLE


class FanHighPower(Enum):
    NOT_AVAILABLE = -1
    UNDEFINED = NOT_AVAILABLE


class FanLong(Enum):
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
            "WideVanneMode": WideVanneMode,
            "AreaMode": AreaMode,
            "FanPower": FanPower,
            "FanHighPower": FanHighPower,
            "FanLong": FanLong,
            }
