import board

# Model specific values
# DO NOT CHANGE
key_pins = ( board.D2, board.D3, board.D1 )
led_map = [ 0, 1 ]

# This list sets the keymapping
# Each key is separated by brackets and multiple keys can be used per-key with commas
# For example, [ ["Keycode.CTRL", "Keycode.SHIFT", "Keycode.C"], [], [] ]
# You should be able to use as many keys together as you'd like,
# but I wouldn't recommend using more than 3 or 4 as they are pressed simultaneously.
keymap = [ ["Keycode.Z"], ["Keycode.X"], ["Keycode.ESCAPE"] ]

# LED timeout in seconds
# The LEDs will turn off after this time and come back on when a key is pressed.
idletime = 60

# LED mode
# Mode 0: Color cycle
# Mode 1: Custom colors
# Mode 2: BPS
led_mode = 0

# Custom colors
# Colors used for custom colors mode
custom_colors = [ [255,255,0], [255,0,255] ]

# Logo color
logo_color = [ 0, 0, 0 ]

# Brightness (0-1)
led_brightness = 0.2

# Debounce interval (Seconds)
# This is the amount of time to ignore a change in the key state after it's been pressed/released.
# Sane values are 0.0005 to 0.0020 (5-20 ms)
db_interval = 0.0010 
