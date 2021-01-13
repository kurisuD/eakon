#!/usr/bin/env python3
# coding=utf-8
"""
Air conditionner classes
"""
import abc
import json
import logging
from abc import ABC
from importlib import import_module
from pathlib import Path

from eakon.enums import common_enum


class HVAC:
    """
    Parent class for air conditionner
    """
    __temp_max = 40
    __temp_min = 10
    __enum = common_enum

    one_mark = None
    one_space = None
    zero_mark = None
    zero_space = None
    pi = None

    def __init__(self, power=None, mode=None, temperature=None, wide_vanne_mode=None, area_mode=None, fan_power=None,
                 fan_high_power=None, fan_long=None, fan_vertical_mode=None, fan_horizontal_mode=None,
                 save_on_update=False, restore=False, enum=common_enum):

        self.__name = type(self).__name__
        self.enum = enum
        self._enums_dict = None

        if restore:
            self.restore()

        self._mode = self.enum.Mode.UNDEFINED
        self._wide_vanne_mode = None
        self._area_mode = None
        self._fan_power = None
        self._fan_high_power = None
        self._fan_long = None
        self._fan_vertical_mode = None
        self._fan_horizontal_mode = None
        self._power = None
        self._temperature = None
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
        self.save_on_update = save_on_update

    def to_dict(self):
        """
        Stores the current state in a dictionnary
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
            "temperature": "Temperature.{}".format(self.temperature)
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
                        val = getattr(self.enum, split[0])[split[1]]
                    self.__setattr__(k, val)
            else:
                logging.warning("failed to load from {} : file doesn't exists.".format(json_file))
        except IOError:
            logging.exception("failed to load from {}".format(json_file))
        except Exception as e:
            logging.exception(e)

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
        rtn += "power :\t\t\t\t\t{}\n".format(self.enum.Power(self.power).name)
        rtn += "mode :\t\t\t\t\t{}\n".format(self.enum.Mode(self.mode).name)
        rtn += "temperature :\t\t\t{}\u00B0C\n".format(self.temperature)
        rtn += "wide_vanne_mode :\t\t{}\n".format(self.enum.WideVanneMode(self.wide_vanne_mode).name)
        rtn += "area_mode :\t\t\t\t{}\n".format(self.enum.AreaMode(self.area_mode).name)
        rtn += "fan_power :\t\t\t\t{}\n".format(self.enum.FanPower(self.fan_power).name)
        rtn += "fan_high_power :\t\t{}\n".format(self.enum.FanHighPower(self.fan_high_power).name)
        rtn += "fan_vertical_mode :\t\t{}\n".format(self.enum.FanVerticalMode(self.fan_vertical_mode).name)
        rtn += "fan_horizontal_mode :\t{}\n".format(self.enum.FanHorizontalMode(self.fan_horizontal_mode).name)
        rtn += "fan_long :\t\t\t\t{}\n".format(self.enum.FanLong(self.fan_long).name)
        return rtn

    @property
    def power(self):
        """
        Get/Set the power
        :return: Power
        """
        return self._power if self._power else None

    @power.setter
    def power(self, power):
        if power:
            if not isinstance(power, self.enum.Power):
                raise TypeError('must be an instance of Power Enum')
            self._power = power
            self.save()

    @property
    def mode(self):
        """
        Get/Set the mode
        :return: Mode
        """
        return self._mode if self._mode else self.enum.Mode.UNDEFINED

    @mode.setter
    def mode(self, mode):
        if mode:
            if not isinstance(mode, self.enum.Mode):
                raise TypeError('must be an instance of Mode Enum')
            self._mode = mode
            self.save()

    @property
    def temperature(self) -> int:
        """
        Get/Set the temperature
        :return: int
        """
        return self._temperature if self._temperature else None

    @temperature.setter
    def temperature(self, temperature: int):
        if temperature:
            if temperature < self.__temp_min:
                self._temperature = self.__temp_min
            elif temperature > self.__temp_max:
                self._temperature = self.__temp_max
            else:
                self._temperature = temperature
            self.save()

    @property
    def wide_vanne_mode(self):
        """
        Get/Set the wide vanne mode
        :return: WideVanneMode
        """
        return self._wide_vanne_mode if self._wide_vanne_mode else self.enum.WideVanneMode.UNDEFINED

    @wide_vanne_mode.setter
    def wide_vanne_mode(self, wide_vanne_mode):
        if wide_vanne_mode:
            if not isinstance(wide_vanne_mode, self.enum.WideVanneMode):
                raise TypeError('must be an instance of WideVanneMode Enum')
            self._wide_vanne_mode = wide_vanne_mode
            self.save()

    @property
    def area_mode(self):
        """
        Get/Set the area mode
        :return: AreaMode
        """
        return self._area_mode if self._area_mode else self.enum.AreaMode.UNDEFINED

    @area_mode.setter
    def area_mode(self, area_mode):
        if area_mode:
            if not isinstance(area_mode, self.enum.AreaMode):
                raise TypeError('must be an instance of AreaMode Enum')
            self._area_mode = area_mode
            self.save()

    @property
    def fan_power(self):
        """
        Get/Set the fan mode
        :return: FanPower
        """
        return self._fan_power if self._fan_power else self.enum.FanPower.UNDEFINED

    @fan_power.setter
    def fan_power(self, fan_power):
        if fan_power:
            if not isinstance(fan_power, self.enum.FanPower):
                raise TypeError('must be an instance of FanPower Enum')
            self._fan_power = fan_power
            self.save()

    @property
    def fan_high_power(self):
        """
        Get/Set the high power
        :return: FanHighPower
        """
        return self._fan_high_power if self._fan_high_power else self.enum.FanHighPower.UNDEFINED

    @fan_high_power.setter
    def fan_high_power(self, fan_high_power):
        if fan_high_power:
            if not isinstance(fan_high_power, self.enum.FanHighPower):
                raise TypeError('must be an instance of FanHighPower Enum')
            self._fan_high_power = self.enum.FanHighPower.NOT_AVAILABLE
            self.save()

    @property
    def fan_long(self):
        """
        Get/Set the Long Fan setting
        :return: FanLong
        """
        return self._fan_long if self._fan_long else self.enum.FanLong.UNDEFINED

    @fan_long.setter
    def fan_long(self, fan_long):
        if fan_long:
            if not isinstance(fan_long, self.enum.FanLong):
                raise TypeError('must be an instance of FanLong Enum')
            self._fan_long = self.enum.FanLong.NOT_AVAILABLE
            self.save()

    @property
    def fan_vertical_mode(self):
        """
        Get/Set the high power
        :return: FanVerticalMode
        """
        return self._fan_vertical_mode if self._fan_vertical_mode else self.enum.FanVerticalMode.UNDEFINED

    @fan_vertical_mode.setter
    def fan_vertical_mode(self, fan_vertical_mode):
        if fan_vertical_mode:
            if not isinstance(fan_vertical_mode, self.enum.FanVerticalMode):
                raise TypeError('must be an instance of FanVerticalMode Enum')
            self._fan_vertical_mode = fan_vertical_mode
            self.save()
        else:
            self._fan_vertical_mode = self.enum.FanVerticalMode.UNDEFINED

    @property
    def fan_horizontal_mode(self):
        """
        Get/Set the high power
        :return: FanHorizontalMode
        """
        return self._fan_horizontal_mode if self._fan_horizontal_mode else self.enum.FanHorizontalMode.UNDEFINED

    @fan_horizontal_mode.setter
    def fan_horizontal_mode(self, fan_horizontal_mode):
        if fan_horizontal_mode:
            if not isinstance(fan_horizontal_mode, self.enum.FanHorizontalMode):
                raise TypeError('must be an instance of FanHorizontalMode Enum')
            self._fan_horizontal_mode = fan_horizontal_mode
            self.save()
        else:
            self._fan_horizontal_mode = self.enum.FanHorizontalMode.UNDEFINED

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
        if not self._enums_dict:
            self._enums_dict = self.enum.get_enums_dict()
        return self._enums_dict

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


if __name__ == '__main__':
    from pap_logger import PaPLogger

    PaPLogger(level=logging.INFO, verbose_fmt=True)
    for model in ["toshiba", "hitachi", "daikin", "toto"]:
        try:
            e = get_eakon_instance_by_model(model)
            e.power = e.enums["Power"].ON
            e.temperature = 26
            e.mode = e.enums["Mode"].COOL
            logging.info("\r\n{}".format(e))
            logging.info(e.bitstring)
        except NotImplementedError as e:
            logging.warning(e)
