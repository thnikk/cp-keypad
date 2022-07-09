import board

# Model specific values
# DO NOT CHANGE
key_pins = ( board.D2, board.D1, board.D3, board.D4, board.D5, board.D8, board.D7, board.D6 )
led_map = [ 1, 0, 2, 3, 4, 7, 6, 5 ]

# This list sets the keymapping
# Each key is separated by brackets and multiple keys can be used per-key with commas
# For example, [ [Keycode.CTRL, Keycode.SHIFT, Keycode.C], [], [] ]
# You should be able to use as many keys together as you'd like,
# but I wouldn't recommend using more than 3 or 4 as they are pressed simultaneously.
keymap = [ ["Keycode.ONE"], ["Keycode.TWO"], ["Keycode.THREE"], ["Keycode.FOUR"], ["Keycode.FIVE"], ["Keycode.SIX"], ["Keycode.SEVEN"], ["Keycode.EIGHT"] ]

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
custom_colors = [ [255,255,0], [255,0,255], [255,0,255], [255,0,255], [255,0,255], [255,0,255], [255,0,255], [255,0,255] ]

# Logo color
logo_color = [ 255, 255, 255 ]

# Brightness (0-1)
led_brightness = 0.2

# Debounce interval (Seconds)
# This is the amount of time to ignore a change in the key state after it's been pressed/released.
# Sane values are 0.0005 to 0.0020 (5-20 ms)
db_interval = 0.0010 
