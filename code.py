# Import necessary libraries
## GPIO libraries
import board
import digitalio
## Keyboard libraries
import usb_hid
from adafruit_hid.keyboard import Keyboard, find_device
from adafruit_hid.nkro import BitmapKeyboard
from adafruit_hid.keycode import Keycode
## Media keys
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.consumer_control import ConsumerControl
from consumer_control_code_extended import CCCX
## Mouse
from adafruit_hid.mouse import Mouse
## LED libraries
import neopixel
from rainbowio import colorwheel
## Timing
import time
## Import settings from config file
from config import key_pins, keymap, idletime, led_mode, custom_colors, led_brightness, db_interval, logo_color, led_map

# Initialize keys and associated lists
key_array = [] # Stores all key objects in a list
pressed = [] # Stores pressed values that function as a lock, making press/release actions only happen once
db_timer = [] # Per-key debounce timer
for key_pin in key_pins:
    key = digitalio.DigitalInOut(key_pin) # Create temp variable for digitalio object with pin
    key.direction = digitalio.Direction.INPUT # Set to input
    key.pull = digitalio.Pull.UP # Set to pullup
    key_array.append(key) # Append temp variable to key array list so it can be used later
    # These values are appended here to set the length of the list depending on the number of keys
    pressed.append(1) # Append a value per-key to the pressed list and default to 1 to prevent keys held at boot from doing anything until released
    db_timer.append(time.monotonic_ns()) # Append a value per-key to the debounce timer list

# Initialize LEDs
pixels = neopixel.NeoPixel(board.D0, len(custom_colors), brightness=led_brightness, auto_write=False)
## Initialize logo LED and set to static color
logo = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=led_brightness, auto_write=False)
logo[0] = logo_color
logo.show()

# Initialize keyboard
kbd = BitmapKeyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

# Define some variables
## Loop counter
count = 0       # Counter for loop speed
second_timer = 0   # Timer for loop speed 
## LEDs
led_timer = 0    # Timer for LED effects
### Color cycle mode
hue = 0         # Byte for colorwheel
### BPS mode
num_pressed = 0 # Stores the number of keypresses within a second
num_pressed_last = 0 # Stores the number of keypresses from the previous second
num_pressed_buffer = 0
## Keyboard timer 
key_timer = 0   # Timer for checking keys
## Keyboard update counter
update_count = 0
## Idle timer
idle_timer = time.monotonic_ns() # Timer for idle timeout 
idletime_ns = idletime * 1000000000 # Convert seconds to nanoseconds

# Evaluate keycodes and mark consumercontrol keycodes
# ConsumerControlCode/Keycode/Mouse/CCCX.<button> all evaluate to a byte, and some keys
# overlap and use the same code. CircuitPython has no way of knowing which a keycode is for,
# so we express it as a string in config.py and evaluate it here while assigning a variable depending on the mode.
# This is done outside of the main loop because eval is slow, so doing it once in setup will keep the loop speed higher.
mode_keymap = []
for x, keys in enumerate(keymap):
    mode_keys = []
    for y, key in enumerate(keys):
        if "ConsumerControl" in key or "CCCX" in key:
            mode_keys.append(1)
        elif "Mouse" in key:
            mode_keys.append(2)
        else:
            mode_keys.append(0)
        keymap[x][y] = eval(keymap[x][y])
    mode_keymap.append(mode_keys)

# Convert db_interval to ns
db_interval = db_interval * 10000000000000
print(db_interval)

while True:

    # Set variable here for easy shorthand
    time_ns = time.monotonic_ns()

    # Print debug info every second
    if (time_ns - second_timer) >= 1000000000:
        second_timer = time_ns # Reset timer
        num_pressed_last = num_pressed # Buffer num_pressed
        print("BPS:", num_pressed) # Print bps value
        num_pressed = 0 # Reset num_pressed
        print("Speed:", count, "/", update_count) # Print speed (loops per second)
        print("Brightness:", pixels.brightness) # Print LED brightness
        update_count=0 # Reset keyboard update counter
        count=0 # Reset main loop counter
        print("ns since boot:", time_ns) # Print time.monotonic_ns()
        # print("Mode keymap:", mode_keymap)
        # print("Keymap:", keymap)
    else:
        count+=1 # Increment value when not printing


    # Update LEDs once every 20 ms 
    if (time_ns - led_timer) >= 20000000:
        led_timer = time_ns # Reset timer
        # Idle timeout
        if (idletime > 0):
            if (time_ns - idle_timer) > idletime_ns:
                if (pixels.brightness > 0): pixels.brightness = pixels.brightness - 0.01
            else:
                if (pixels.brightness < led_brightness): pixels.brightness = pixels.brightness + 0.01
            logo.brightness = pixels.brightness
            logo.show()
        if led_mode == 0: # Color cycle
            hue+=1 # Increment value
            for i in range(0, len(custom_colors)): # Iterate through keys
                if (pressed[i] == 0): # If not pressed,
                    # set color to hue plus offset based on key position
                    pixels[led_map[i]] = colorwheel(hue + (i * 20) % 255)
                else:
                    pixels[led_map[i]] = (255, 255, 255) # Set to white if pressed
        elif led_mode == 1: # Custom color
            for i in range(0, len(custom_colors)): # Iterate through keys
                if (pressed[i] == 0):
                    pixels[led_map[i]] = custom_colors[i] # Set to colors defined in config
                else:
                    pixels[led_map[i]] = (255, 255, 255) # Set to white if pressed
        elif led_mode == 2: # BPS
            # Step color up if presses per second has increased
            if num_pressed_last > num_pressed_buffer: num_pressed_buffer += 1
            # Step down color if value has decreased
            if num_pressed_last < num_pressed_buffer: num_pressed_buffer -= 1
            # Assign color based on value * 10
            pixels.fill(colorwheel(num_pressed_buffer * 10))
        pixels.show()

    # Update key status 1000 times per second
    if (time_ns - key_timer) >= 500000:
        key_timer = time_ns # Reset timer
        update_count+=1 # Increase keyboard loop counter
        # Check keys
        for x, key in enumerate(key_array): # Iterate through keys
            if (time_ns - db_timer[x]) >= db_interval: # If debounce time has passed for the key
                if not key.value and not pressed[x]: # If the key has been pressed
                    for y, kc in enumerate(keymap[x]): # Press all keys for active key
                        if (mode_keymap[x][y] == 1): # Check the mode and use consumercontrol if 1
                            cc.press(kc)
                        elif (mode_keymap[x][y] == 2): # Mouse if 2
                            mouse.press(kc)
                        else: # Otherwise use keyboard
                            kbd.press(kc)
                    pressed[x] = 1 # This causes the press action to only run once until released
                    num_pressed+=1 # Add to counter for bps
                    db_timer[x] = time_ns # Update debounce timer for key
                    idle_timer = time_ns # Reset idle timer
                elif key.value and pressed[x]: # If the key has been released
                    for y, kc in enumerate(keymap[x]): # Release all keys for active key
                        if (mode_keymap[x][y] == 1): # Check the mode and use consumercontrol if 1
                            cc.release()
                        elif (mode_keymap[x][y] == 2): # Mouse if 2
                            mouse.release(kc)
                        else: # Otherwise use keyboard
                            kbd.release(kc)
                    pressed[x] = 0 # This causes the release action to only run once until pressed
                    db_timer[x] = time_ns # Update debounce timer
                    idle_timer = time_ns # Reset idle timer

        
