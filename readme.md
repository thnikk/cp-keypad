# CircuitPython Keypad
This code was rebased using Adafruit's keypad example. This depends on the [keypad](https://docs.circuitpython.org/en/latest/shared-bindings/keypad/index.html) library, which is incompatible with the SAMD21 Seeeduino Xiao, so this is made for use with the RP2040 version of the Xiao, which is a drop-in replacement.

## Why CircuitPython?
I've written a lot of different versions of firmware for my keypads over the years. I think I'm relatively compitent with Arduino, and I have much less experience with Python, but that's not the same for a lot of people. 

Python is a very popular language and makes a lot of things a lot easier. 

One of the biggest things for me is the ability to disable CDC (serial) and UMS (mass storage) at runtime. This provides great ways to debug and configure the keypad without being stuck with a serial or mass storage device constantly being connected, potentially conflicting with other programs. I've had keypads freak out when opening Cura (a 3D printing program) because of how it checks for serial devices, and if you don't have any other removable drives connected, it can be annoying to see one whenever the keypad is plugged in.

## Goals
My biggest goals are reaching feature parity with the Unified-2022 firmware, with the exceptions of:

- No serial remapper since this is done with the config file instead.

