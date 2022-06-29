from adafruit_hid.keycode import Keycode

# This list sets the keymapping
# Each key is separated by brackets and multiple keys can be used per-key with commas
# For example, [ [Keycode.CTRL, Keycode.SHIFT, Keycode.C], [], [] ]
# You should be able to use as many keys together as you'd like,
# but I wouldn't recommend using more than 3 or 4 as they are pressed simultaneously.
keymap = [ [Keycode.Z], [Keycode.X], [Keycode.ESCAPE] ]

# LED timeout in seconds
# The LEDs will turn off after this time and come back on when a key is pressed.
idletime = 60

# LED mode
# Mode 0: Color cycle
# Mode 1: Custom colors
# Mode 2: BPS
led_mode = 2

# Custom colors
# Colors used for custom colors mode
custom_colors = [ [255,255,0], [255,0,255] ]

# Brightness (0-1)
led_brightness = 0.2
