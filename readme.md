# CircuitPython Keypad
There are two main reasons why this exists: 
1) It's way simpler than the arduino unified-2022 code at only around 200 LOC instead of 900
2) It's way easier to configure since all settings are in an easy to edit config file that doesn't require recompliling the firmware.

## Why CircuitPython?
I've written a lot of different versions of firmware for my keypads over the years. I think I'm relatively compitent with Arduino, and I have much less experience with Python, but that's not the same for a lot of people. Python is a very popular language and makes a lot of things a lot easier. Even with less experience, adding features is a bit easier with python.

One big advantage is being able to configure the keypad through a plaintext file. This removes the need for any configurator, and gives more control to the user if they want to edit the code of the keypad without having to set up a development environment.

One of the biggest things for me is the ability to disable CDC (serial) and UMS (mass storage) at runtime. This provides great ways to debug and configure the keypad without being stuck with a serial or mass storage device constantly being connected, potentially conflicting with other programs. I've had keypads freak out when opening Cura (a 3D printing program) because of how it checks for serial devices, and if you don't have any other removable drives connected, it can be annoying to see one whenever the keypad is plugged in.

## Enabling USB mass storage (required for updating) and serial (for debugging)

Both of these are disabled by default by boot.py and can be enabled by holding down the first two keys while plugging the keypad in. If you only want to enable one of them, mass storage is the first key and serial is the second.

## Entering bootloader mode

If your keypad doesn't have easy access to the reset switch, you can enter bootloader mode by holding down the third key at boot.

## Compatibility
This code uses time.monotonic_ns(), which requires long integer support. SAMD21 boards like my current (as of writing in 2022) xiao based keypads are not compatible. It's possible to use time.monotonic() instead, but this will lose acccuracy over time and subsequently cause the timers in the code to reduce in speed after about an hour. 

For this reason, prototype RP2040 xiao based models are being used for developemnt. This means that this code will be used for future models but will not be backwards compatible due to limitations in the currently used hardware.

## Features

 - [x] Remappable keys
 - [x] Cycle LED mode
 - [x] Custom LED mode
 - [x] Idle timeout
 - [x] BPS led mode
 - [x] Scalable (8 keys is about the highest you can go without losing speed)
 - [x] Separate config file for easy configuration
 - [x] Use config file for setting boot.py keys
 - [x] Configurable logo LED color
 - [x] LED map list for keypads with unmatched key/LED orders
 - [x] Media key support
 - [x] Mouse button support
 - [ ] Touch support (may be a pipe dream due to speed)
