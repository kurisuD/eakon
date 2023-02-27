#!/usr/bin/env python3
# coding=utf-8
"""
Air conditioner classes
"""
__version__ = "0.0.9"
__available_models__ = ["daikin", "hitachi", "panasonic", "toshiba"]

import abc
import json
import logging
from abc import ABC
from importlib import import_module
from pathlib import Path
from typing import Union

from eakon.enums import common_enum


class HVAC:
    """
    Parent class for air conditioner
    """
    __enum = common_enum

    one_mark = None
    one_space = None
    zero_mark = None
    zero_space = None
    pi = None

    def __init__(self, power=None, mode=None, temperature=None, wide_vanne_mode=None, area_mode=None, fan_power=None,
                 fan_high_power=None, fan_long=None, fan_vertical_mode=None, fan_horizontal_mode=None,
                 save_on_update=False, restore=False, room_clean=False, enum=common_enum):

        self.__name = type(self).__name__
        self._enum = enum

        if restore:
            self.restore()

        self._mode = self._enum.Mode.UNDEFINED
        self._wide_vanne_mode = None
        self._area_mode = None
        self._fan_power = None
        self._fan_high_power = None
        self._fan_long = None
        self._fan_vertical_mode = None
        self._fan_horizontal_mode = None
        self._power = None
        self._temperature = None
        self._room_clean = None
        self._save_on_update = False

        self.power = power
        self.mode = mode
        self.temperature = temperature
        if wide_vanne_mode:
            self.wide_vanne_mode = wide_vanne_mode
        if area_mode:
            self.area_mode = area_mode
        if fan_power:
            self.fan_power = fan_power
        if fan_high_power:
            self.fan_high_power = fan_high_power
        if fan_long:
            self.fan_long = fan_long
        if fan_vertical_mode:
            self.fan_vertical_mode = fan_vertical_mode
        if fan_horizontal_mode:
            self.fan_horizontal_mode = fan_horizontal_mode
        if room_clean:
            self.room_clean = room_clean
        self.save_on_update = save_on_update

    def to_dict(self):
        """
        Stores the current state in a dictionary
        :return: dict
        """
        return {
            "mode": "Mode.{}".format(self.mode.name),
            "wide_vanne_mode": "WideVanneMode.{}".format(self.wide_vanne_mode.name),
            "area_mode": "AreaMode.{}".format(self.area_mode.name),
            "fan_power": "FanPower.{}".format(self.fan_power.name),
            "fan_high_power": "FanHighPower.{}".format(self.fan_high_power.name),
            "fan_long": "FanLong.{}".format(self.fan_long.name),
            "fan_vertical_mode": "FanVerticalMode.{}".format(self.fan_vertical_mode.name),
            "fan_horizontal_mode": "FanHorizontalMode.{}".format(self.fan_horizontal_mode.name),
            "power": "Power.{}".format(self.power.name),
            "temperature": "Temperature.{}".format(self.temperature),
            "room_clean": "RoomClean.{}".format(self.room_clean),
        }

    def restore(self):
        """
        restore the state of the class from file.
        """
        json_file = Path("/tmp/") / "eakon_{}.json".format(self.__name)
        try:
            if json_file.exists():
                logging.info("loading state from {}".format(json_file))
                hvac_dict = json.loads(json_file.read_text())
                for k, v in hvac_dict.items():
                    if isinstance(v, int):
                        val = v
                    else:
                        split = v.split(".")
                        val = getattr(self._enum, split[0])[split[1]]
                    self.__setattr__(k, val)
            else:
                logging.warning("failed to load from {} : file doesn't exists.".format(json_file))
        except IOError:
            logging.exception("failed to load from {}".format(json_file))
        except Exception as exc:
            logging.exception(exc)

    def save(self):
        """
        Saves the current state in a json file
        """
        if self._save_on_update:
            json_file = Path("/tmp/") / "eakon_{}.json".format(self.__name)
            try:
                state = self.to_dict()
                state.pop("power")
                json_file.write_text(json.dumps(state))
                logging.info(f"save state to {json_file}")
            except IOError:
                logging.exception(f"failed to save {json_file}")

    def __str__(self):
        rtn = "Model :\t\t\t\t\t{}\n".format(self.__name)
        rtn += "power :\t\t\t\t\t{}\n".format(self._enum.Power(self.power).name)
        rtn += "mode :\t\t\t\t\t{}\n".format(self._enum.Mode(self.mode).name)
        rtn += "temperature :\t\t\t{}\u00B0C\n".format(self.temperature)
        rtn += "wide_vanne_mode :\t\t{}\n".format(self._enum.WideVanneMode(self.wide_vanne_mode).name)
        rtn += "area_mode :\t\t\t\t{}\n".format(self._enum.AreaMode(self.area_mode).name)
        rtn += "fan_power :\t\t\t\t{}\n".format(self._enum.FanPower(self.fan_power).name)
        rtn += "fan_high_power :\t\t{}\n".format(self._enum.FanHighPower(self.fan_high_power).name)
        rtn += "fan_vertical_mode :\t\t{}\n".format(self._enum.FanVerticalMode(self.fan_vertical_mode).name)
        rtn += "fan_horizontal_mode :\t{}\n".format(self._enum.FanHorizontalMode(self.fan_horizontal_mode).name)
        rtn += "fan_long :\t\t\t\t{}\n".format(self._enum.FanLong(self.fan_long).name)
        rtn += "room_clean :\t\t\t{}\n".format(self._enum.RoomClean(self.room_clean).name)
        return rtn

    @property
    def power(self):
        """
        Get/Set the power state
        :return: Power
        """
        return self._power if self._power else None

    @power.setter
    def power(self, power):
        if power:
            if not isinstance(power, self._enum.Power):
                raise TypeError('must be an instance of Power Enum')
            self._power = power
            self.save()

    @property
    def mode(self):
        """
        Get/Set the mode state
        :return: Mode
        """
        return self._mode if self._mode else self._enum.Mode.UNDEFINED

    @mode.setter
    def mode(self, mode):
        if mode:
            if not isinstance(mode, self._enum.Mode):
                raise TypeError('must be an instance of Mode Enum')
            self._mode = mode
            self.save()

    @property
    def min_temp(self) -> int:
        """
        Minimum temperature setting
        :return:
        """
        return self._enum.TempRange.MIN.value

    @property
    def max_temp(self) -> int:
        """
        Maximum temperature setting
        :return:
        """
        return self._enum.TempRange.MAX.value

    @property
    def temp_step(self) -> float:
        """
        Increments of temperature increase that are possible
        :return:
        """
        return self._enum.TempRange.STEP.value

    @property
    def temperature(self) -> Union[int, float, None]:
        """
        Get/Set the temperature
        :return: int
        """
        return self._temperature if self._temperature else None

    @temperature.setter
    def temperature(self, temperature: Union[int, float]):
        if temperature:
            if temperature < self.min_temp:
                self._temperature = self.min_temp
            elif temperature > self.max_temp:
                self._temperature = self.max_temp
            else:
                self._temperature = temperature
            self.save()

    @property
    def wide_vanne_mode(self):
        """
        Get/Set the wide vanne mode
        :return: WideVanneMode
        """
        return self._wide_vanne_mode if self._wide_vanne_mode else self._enum.WideVanneMode.UNDEFINED

    @wide_vanne_mode.setter
    def wide_vanne_mode(self, wide_vanne_mode):
        if wide_vanne_mode:
            if not isinstance(wide_vanne_mode, self._enum.WideVanneMode):
                raise TypeError('must be an instance of WideVanneMode Enum')
            self._wide_vanne_mode = wide_vanne_mode
            self.save()

    @property
    def area_mode(self):
        """
        Get/Set the area mode
        :return: AreaMode
        """
        return self._area_mode if self._area_mode else self._enum.AreaMode.UNDEFINED

    @area_mode.setter
    def area_mode(self, area_mode):
        if area_mode:
            if not isinstance(area_mode, self._enum.AreaMode):
                raise TypeError('must be an instance of AreaMode Enum')
            self._area_mode = area_mode
            self.save()

    @property
    def fan_power(self):
        """
        Get/Set the fan mode
        :return: FanPower
        """
        return self._fan_power if self._fan_power else self._enum.FanPower.UNDEFINED

    @fan_power.setter
    def fan_power(self, fan_power):
        if fan_power:
            if not isinstance(fan_power, self._enum.FanPower):
                raise TypeError('must be an instance of FanPower Enum')
            self._fan_power = fan_power
            self.save()

    @property
    def fan_high_power(self):
        """
        Get/Set the high power
        :return: FanHighPower
        """
        return self._fan_high_power if self._fan_high_power else self._enum.FanHighPower.UNDEFINED

    @fan_high_power.setter
    def fan_high_power(self, fan_high_power):
        if fan_high_power:
            if not isinstance(fan_high_power, self._enum.FanHighPower):
                raise TypeError('must be an instance of FanHighPower Enum')
            self._fan_high_power = self._enum.FanHighPower.NOT_AVAILABLE
            self.save()

    @property
    def fan_long(self):
        """
        Get/Set the Long Fan setting
        :return: FanLong
        """
        return self._fan_long if self._fan_long else self._enum.FanLong.UNDEFINED

    @fan_long.setter
    def fan_long(self, fan_long):
        if fan_long:
            if not isinstance(fan_long, self._enum.FanLong):
                raise TypeError('must be an instance of FanLong Enum')
            self._fan_long = self._enum.FanLong.NOT_AVAILABLE
            self.save()

    @property
    def fan_vertical_mode(self):
        """
        Get/Set the high power
        :return: FanVerticalMode
        """
        return self._fan_vertical_mode if self._fan_vertical_mode else self._enum.FanVerticalMode.UNDEFINED

    @fan_vertical_mode.setter
    def fan_vertical_mode(self, fan_vertical_mode):
        if fan_vertical_mode:
            if not isinstance(fan_vertical_mode, self._enum.FanVerticalMode):
                raise TypeError('must be an instance of FanVerticalMode Enum')
            self._fan_vertical_mode = fan_vertical_mode
            self.save()
        else:
            self._fan_vertical_mode = self._enum.FanVerticalMode.UNDEFINED

    @property
    def fan_horizontal_mode(self):
        """
        Get/Set the high power
        :return: FanHorizontalMode
        """
        return self._fan_horizontal_mode if self._fan_horizontal_mode else self._enum.FanHorizontalMode.UNDEFINED

    @fan_horizontal_mode.setter
    def fan_horizontal_mode(self, fan_horizontal_mode):
        if fan_horizontal_mode:
            if not isinstance(fan_horizontal_mode, self._enum.FanHorizontalMode):
                raise TypeError('must be an instance of FanHorizontalMode Enum')
            self._fan_horizontal_mode = fan_horizontal_mode
            self.save()
        else:
            self._fan_horizontal_mode = self._enum.FanHorizontalMode.UNDEFINED

    @property
    def room_clean(self):
        """
        Sets room air cleaning function ??
        :return:
        """
        return self._room_clean if self._room_clean else self._enum.RoomClean.UNDEFINED

    @room_clean.setter
    def room_clean(self, room_clean):
        if room_clean:
            if not isinstance(room_clean, self._enum.RoomClean):
                raise TypeError('must be an instance of RoomClean Enum')
            self._room_clean = room_clean
            self.save()
        else:
            self._room_clean = self._enum.RoomClean.UNDEFINED

    @property
    def save_on_update(self):
        """
        Get/Set the flag to save any changes to disk
        :return:
        """
        return self.__save_on_update

    @save_on_update.setter
    def save_on_update(self, save_on_update):
        if save_on_update is not None:
            if not isinstance(save_on_update, bool):
                raise TypeError('must be an instance of bool')
            self.__save_on_update = save_on_update

    def _get_one(self):
        return [self.one_mark, self.one_space]

    def _get_zero(self):
        return [self.zero_mark, self.zero_space]

    @abc.abstractmethod
    def _get_bitstring(self):
        pass

    @abc.abstractmethod
    def _get_wave(self):
        pass

    @property
    def bitstring(self):
        """
        returns the bits before encoding to a wave chain
        :return:
        """
        return self._get_bitstring()

    @property
    def wave(self):
        """
        returns a wave chain
        :return:
        """
        return self._get_wave()

    @property
    def enums(self):
        """
        Facility dictionary for accessing the different enums for a given model
        :return: dict of _enum
        """
        return self._enum.get_enums_dict()

    @property
    def actions_options_dict(self) -> dict:
        """
        returns a dictionary of actions:options
        :return:
        """
        hvac_actions = {}
        for action, options in self.enums.items():
            hvac_actions[action] = [x for x in options.__members__.keys() if x != "UNDEFINED"]
        return hvac_actions


def get_eakon_instance_by_model(model_name) -> HVAC:
    """
    A helper function to instantiate a new class using a model name.
    :param model_name:
    :return:
    """
    model_name = model_name.lower()
    class_name = model_name.capitalize()
    try:
        module_type = import_module(name=f"eakon.{model_name}")
        model_class = getattr(module_type, class_name)
        return ABC.register(type(class_name, (model_class,), {}))()
    except (ModuleNotFoundError, TypeError) as exc:
        logging.debug("Exception was {}".format(exc))
        raise NotImplementedError(
            "No module {} implementing class {} was found. Model {} is unsupported.".format(model_name, class_name,
                                                                                            model_name))


def get_available_models() -> [str]:
    """
    list of models available for creating an instance
    :return:
    """
    return __available_models__


if __name__ == '__main__':
    from pap_logger import PaPLogger

    PaPLogger(level=logging.INFO, verbose_fmt=True)
    for model in __available_models__:
        try:
            e = get_eakon_instance_by_model(model)
            print(e.min_temp)
            print(e.max_temp)
            e.power = e.enums["Power"].ON
            e.temperature = 26
            e.mode = e.enums["Mode"].COOL
            logging.info("\r\n{}".format(e))
            logging.info(e.bitstring)
        except NotImplementedError as e:
            logging.warning(e)
