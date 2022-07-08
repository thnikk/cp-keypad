# Import necessary libraries
## GPIO libraries
import board
import digitalio
## Keyboard libraries
import usb_hid
from adafruit_hid.keyboard import Keyboard, find_device
from adafruit_hid.nkro import BitmapKeyboard
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
logo = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1, auto_write=False)
logo[0] = logo_color
logo.show()

# Initialize keyboard
kbd = BitmapKeyboard(usb_hid.devices)

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
    else:
        count+=1 # Increment value when not printing


    # Update LEDs once every 20 ms 
    if (time_ns - led_timer) >= 20000000:
        led_timer = time_ns # Reset timer
        # Idle timeout
        if (time_ns - idle_timer) > idletime_ns:
            if (pixels.brightness > 0): pixels.brightness = pixels.brightness - 0.01
        else:
            if (pixels.brightness < led_brightness): pixels.brightness = pixels.brightness + 0.01
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
                    for kc in keymap[x]: # Press all keys for active key
                        kbd.press(kc)
                    pressed[x] = 1 # This causes the press action to only run once until released
                    num_pressed+=1 # Add to counter for bps
                    db_timer[x] = time_ns # Update debounce timer for key
                    idle_timer = time_ns # Reset idle timer
                elif key.value and pressed[x]: # If the key has been released
                    for kc in keymap[x]: # Release all keys for active key
                        kbd.release(kc)
                    pressed[x] = 0 # This causes the release action to only run once until pressed
                    db_timer[x] = time_ns # Update debounce timer
                    idle_timer = time_ns # Reset idle timer

        
