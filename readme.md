# CircuitPython Keypad
This code uses time.monotonic_ns(), which requires long integer support. SAMD21 boards like my current (as of writing in 2022) xiao based keypads are not compatible. It's possible to use time.monotonic() instead, but this will lose acccuracy over time and subsequently cause the timers in the code to reduce in speed after about an hour. 

For this reason, prototype RP2040 xiao based models are being used for developemnt. This means that this code will be used for future models but will not be backwards compatible due to limitations in the currently used hardware.

## Why CircuitPython?
I've written a lot of different versions of firmware for my keypads over the years. I think I'm relatively compitent with Arduino, and I have much less experience with Python, but that's not the same for a lot of people. Python is a very popular language and makes a lot of things a lot easier. Even with less experience, adding features is a bit easier with python.

One big advantage is being able to configure the keypad through a plaintext file. This removes the need for any configurator, and gives more control to the user if they want to edit the code of the keypad without having to set up a development environment.

One of the biggest things for me is the ability to disable CDC (serial) and UMS (mass storage) at runtime. This provides great ways to debug and configure the keypad without being stuck with a serial or mass storage device constantly being connected, potentially conflicting with other programs. I've had keypads freak out when opening Cura (a 3D printing program) because of how it checks for serial devices, and if you don't have any other removable drives connected, it can be annoying to see one whenever the keypad is plugged in.

## MIDI support
I'm not sure where to put this so here's another section. CircuitPython actually lets you use the keypad as a MIDI device, but I've disabled it in boot.py to reduce unnecessary USB endpoints. 

I think it would be cool to make a MIDI keypad, but it's not something I have a lot of experience with and I don't think it fits into this firmware. I also suspect that most people would want completely different functionality, so I think providing a skeleton firmware that's easy to modify would make more sense than retrofitting this code. It should be easy enough so if you know any python, give it a try (just make sure you delete boot.py).

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
 - [ ] Touch support (may be a pipe dream due to speed)
