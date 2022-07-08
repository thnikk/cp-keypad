import board
import usb_hid
import time
from adafruit_hid.keyboard import Keyboard, find_device
from adafruit_hid.nkro import BitmapKeyboard
# LED libraries
import neopixel
from rainbowio import colorwheel
from config import key_pins, keymap, idletime, led_mode, custom_colors, led_brightness, db_interval, logo_color
import digitalio

key_array = []
pressed = []
db_timer = []
for key_pin in key_pins:
    key = digitalio.DigitalInOut(key_pin)
    key.direction = digitalio.Direction.INPUT
    key.pull = digitalio.Pull.UP
    key_array.append(key)
    pressed.append(0)
    db_timer.append(time.monotonic_ns())

pixels = neopixel.NeoPixel(board.D0, len(custom_colors), brightness=led_brightness, auto_write=False)
kbd = BitmapKeyboard(usb_hid.devices)

count = 0       # Counter for loop speed
second_timer = 0   # Timer for loop speed 

hue = 0         # Byte for colorwheel
led_timer = 0    # Timer for LED effects

key_timer = 0   # Timer for checking keys

num_pressed = 0 # Stores the number of keypresses within a second
num_pressed_last = 0 # Stores the number of keypresses from the previous second
num_pressed_buffer = 0

update_count = 0

idle_timer = time.monotonic_ns() # Timer for idle timeout
idletime_ns = idletime * 1000000000 # Convert seconds to nanoseconds

# Set logo color to white at boot
logo = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1, auto_write=False)
logo[0] = logo_color
logo.show()

while True:

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
        count+=1


    # Update LEDs once every 20 ms 
    if (time_ns - led_timer) >= 20000000:
        led_timer = time_ns # Reset time
        # Idle timeout
        if (time_ns - idle_timer) > idletime_ns:
            if (pixels.brightness > 0): pixels.brightness = pixels.brightness - 0.01
        else:
            if (pixels.brightness < led_brightness): pixels.brightness = pixels.brightness + 0.01
        if led_mode == 0:
            # Color cycle
            hue+=1
            for i in range(0, len(custom_colors)):
                if (pressed[i] == 0):
                    color = (hue + (i * 20) % 255)
                    pixels[i] = colorwheel(color)
                else:
                    pixels[i] = (255, 255, 255)
        elif led_mode == 1:
            # Custom color
            for i in range(0, len(custom_colors)):
                if (pressed[i] == 0):
                    pixels[i] = custom_colors[i]
                else:
                    pixels[i] = (255, 255, 255)
        elif led_mode == 2:
            # BPS
            if num_pressed_last > num_pressed_buffer: num_pressed_buffer += 1
            if num_pressed_last < num_pressed_buffer: num_pressed_buffer -= 1
            pixels.fill(colorwheel(num_pressed_buffer * 10))
        pixels.show()

    # Update key status 1000 times per second
    if (time_ns - key_timer) >= 500000:
        update_count+=1
        key_timer = time_ns # Reset timer
        # Check keys
        for x, key in enumerate(key_array):
            if (time_ns - db_timer[x]) >= db_interval:
                if not key.value and not pressed[x]:
                    for kc in keymap[x]:
                        kbd.press(kc)
                    pressed[x] = 1
                    num_pressed+=1 # Add to counter for bps
                    db_timer[x] = time_ns
                    idle_timer = time_ns
                elif key.value and pressed[x]:
                    for kc in keymap[x]:
                        kbd.release(kc)
                    pressed[x] = 0
                    db_timer[x] = time_ns
                    idle_timer = time_ns

        
