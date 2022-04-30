from adafruit_hid.keycode import Keycode

# This list sets the keymapping
# Each key is separated by brackets and multiple keys can be used per-key with commas
keymap = [ [Keycode.Z], [Keycode.X], [Keycode.ESCAPE] ]

# Time timeout in seconds
idletime = 60

# LED mode
led_mode = 1

# Custom colors
custom_colors = [ [255,255,0], [255,0,255] ]

# Brightness (0-1)
led_brightness = 0.2
