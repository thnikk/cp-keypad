# CircuitPython Keypad
This code was rebased using Adafruit's keypad example. This depends on the [keypad](https://docs.circuitpython.org/en/latest/shared-bindings/keypad/index.html) library, which is incompatible with the SAMD21 Seeeduino Xiao, so this is made for use with the RP2040 version of the Xiao.

## Why CircuitPython?
I've written a lot of different versions of firmware for my keypads over the years. I think I'm relatively compitent with Arduino, and I have much less experience with Python, but that's not the same for a lot of people. Python is a very popular language and makes a lot of things a lot easier. Even with less experience, adding features is a bit easier with python.

One big advantage is being able to configure the keypad through a plaintext file. This removes the need for any configurator, and gives more control to the user if they want to edit the code of the keypad without having to set up a development environment.

One of the biggest things for me is the ability to disable CDC (serial) and UMS (mass storage) at runtime. This provides great ways to debug and configure the keypad without being stuck with a serial or mass storage device constantly being connected, potentially conflicting with other programs. I've had keypads freak out when opening Cura (a 3D printing program) because of how it checks for serial devices, and if you don't have any other removable drives connected, it can be annoying to see one whenever the keypad is plugged in.

## MIDI support
I'm not sure where to put this so here's another section. CircuitPython actually lets you use the keypad as a MIDI device, but I've disabled it in boot.py to reduce unnecessary USB endpoints. 

I think it would be cool to make a MIDI keypad, but it's not something I have a lot of experience with and I don't think it fits into this firmware. I also suspect that most people would want completely different functionality, so I think providing a skeleton firmware that's easy to modify would make more sense than retrofitting this code. It should be easy enough so if you know any python, give it a try (just make sure you delete boot.py).

## Goals
My biggest goals are reaching feature parity with the Unified-2022 firmware, with the exceptions of:

- No serial remapper since this is done with the config file instead.

## Features

 - [x] Remappable keys
 - [x] Cycle LED mode
 - [x] Custom LED mode
 - [x] Idle timeout
 - [x] BPS led mode
 - [ ] Touch support
