# eakon

eakon is a simple python library to control air-conditioners.

There are many examples of such code on the web, but I found none did not cover my needs:

Each HVAC unit to control needs to have its own instance created (the instance being dependent on the unit maker).

- Each instance keeps track of the current status of the air-conditioner (assuming it is not changed with the unit remote control)

- The status can be made persistent

- handle japanese market air-conditioners

Moreover, the code was to be kept the least esoteric as possible, to ensure readability and evolutions.

Usage of [bitstring](https://github.com/scott-griffiths/bitstring) greatly helped to reach this objective.

## Usage example

During or after instantiation, settings are made, and you get either a bitstring or a wave.
The wave is in a format to be consumed by the [pigpio library](http://abyz.me.uk/rpi/pigpio/), following the example of the [sample irrp.py](http://abyz.me.uk/rpi/pigpio/code/irrp_py.zip) script.

N.B. : The irrp.py script has length limitations.
You can refer to (or better yet, use) my [AnaviInfraredPhat](https://github.com/kurisuD/AnaviInfraredPhat/) library which handles compression of waves for working around length limitations of pigpio.

The compression algorithm is credit of https://korintje.com/archives/28 

```
    hvac = Daikin()
    hvac.power = daikin_enum.Power.ON
    hvac.temperature = 21
    hvac.mode = daikin_enum.Mode.COOL
    hvac.fan_vertical_mode = daikin_enum.FanVerticalMode.TOP

    logging.info("\r{}".format(hvac))
    logging.info(hvac.bitstring)
    logging.info(hvac.wave)
>>
power :                 ON
mode :                  COOL
temperature :           21°C
wide_vanne_mode :       NOT_AVAILABLE
area_mode :             NOT_AVAILABLE
fan_power :             AUTO
fan_high_power :        NOT_AVAILABLE
fan_vertical_mode :     TOP
fan_horizontal_mode :   UNDEFINED
fan_long :              NOT_AVAILABLE

100010000101101111100100000000000100000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000010010010001000010110111110010000000000000000001001110001010100000000000000010100000000000000000110000000000110000000000000000011000011000000000000000001111100
[433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 25194, 3495, 1746, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 1288, 433, 1288, 433, 440, 433, 1288, 433, 1288, 433, 1288, 433, 1288, 433, 1288, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 25194, 3495, 1746, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 1288, 433, 1288, 433, 440, 433, 1288, 433, 1288, 433, 1288, 433, 1288, 433, 1288, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 1288, 433, 1288, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 1288, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 1288, 433, 1288, 433, 1288, 433, 1288, 433, 440, 433, 440, 433]

    hvac.power = daikin_enum.Power.OFF
    logging.info("\r{}".format(hvac))
    logging.info(hvac.bitstring)
    logging.info(hvac.wave)
>>
power :                 OFF
mode :                  COOL
temperature :           21°C
wide_vanne_mode :       NOT_AVAILABLE
area_mode :             NOT_AVAILABLE
fan_power :             AUTO
fan_high_power :        NOT_AVAILABLE
fan_vertical_mode :     TOP
fan_horizontal_mode :   UNDEFINED
fan_long :              NOT_AVAILABLE

100010000101101111100100000000000100000000000000000000000000000000000000000000000000000000000001000010000000000000000000000000000000000000000000000000000010010110001000010110111110010000000000000000000001110001010100000000000000010100000000000000000110000000000110000000000000000011000011000000000000000010111100
[433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 25194, 3495, 1746, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 1288, 433, 1288, 433, 440, 433, 1288, 433, 1288, 433, 1288, 433, 1288, 433, 1288, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 1288, 433, 25194, 3495, 1746, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 1288, 433, 1288, 433, 440, 433, 1288, 433, 1288, 433, 1288, 433, 1288, 433, 1288, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 1288, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 1288, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 1288, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 440, 433, 1288, 433, 440, 433, 1288, 433, 1288, 433, 1288, 433, 1288, 433, 440, 433, 440, 433]

```

The bitstring is mostly used for debugging purpose, but I assume it could be used for other purpose.

## (Known) Supported models

As the name (エアコン) of the library implies, there is a strong focus on japanese brands, and quite possibly is limited to recent (2020) japanese models.

Development was done with the following models of remote controls:
- Daikin ARC47850 (Units models C and CX at least)
- Hitachi SP-RC4 (covers [a lot of hitachi models](https://kadenfan.hitachi.co.jp/ra/parts/supply/sprc4.html))
- Toshiba RG66J5 (apparently all units from 2020, possibly also few years before ?)

Daikin has at least 2 other protocols available in Japan (Moreover, it is likely that protocols used for non-domestic market differs).

Implementation of additional models should be relatively easy.

## Limitations

Only standard functions are implemented, _in extenso_:
- timers aren't supported (by lack of interest)
- extra functions like unit cleaning, triggering of diagnostic, etc... aren't supported
