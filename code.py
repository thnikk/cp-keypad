import keypad
import board
import usb_hid
import time
from adafruit_hid.keyboard import Keyboard, find_device
from adafruit_hid.nkro import BitmapKeyboard
# LED libraries
import neopixel
from rainbowio import colorwheel
from config import keymap, idletime, led_mode, custom_colors, led_brightness

# Set key pins statically
key_pins = ( board.D2, board.D3, board.D1 )
keys = keypad.Keys(key_pins, value_when_pressed=False, pull=True, interval=0.020)
pixels = neopixel.NeoPixel(board.D0, len(keymap)-1, brightness=led_brightness, auto_write=False)
kbd = BitmapKeyboard(usb_hid.devices)

count = 0       # Counter for loop speed
second_timer = 0   # Timer for loop speed 

hue = 0         # Byte for colorwheel
led_timer = 0    # Timer for LED effects

pressed = [ 0, 0, 0, 0, 0 ] # Stores key states 
num_pressed = 0 # Stores the number of keypresses within a second
num_pressed_last = 0 # Stores the number of keypresses from the previous second
num_pressed_buffer = 0

idle_time = time.monotonic() # Timer for idle timeout

while True:

    # Print count value every second and reset to 0
    if (time.monotonic() - second_timer) >= 1:
        second_timer = time.monotonic() # Reset timer
        num_pressed_last = num_pressed
        # print("BPS:", num_pressed)
        num_pressed = 0
        print(count)
        count=0
    else:
        count+=1


    # Update LEDs once every 20 ms 
    if (time.monotonic() - led_timer) >= 0.020:
        led_timer = time.monotonic() # Reset timer
        if (time.monotonic() - idle_time) > idletime:
            pixels.brightness = 0
        else:
            pixels.brightness = led_brightness
        if led_mode == 0:
            # Color cycle
            hue+=1
            for i in range(0, len(keymap)-1):
                if (pressed[i] == 0):
                    color = (hue + (i * 20) % 255)
                    pixels[i] = colorwheel(color)
                else:
                    pixels[i] = (255, 255, 255)
        elif led_mode == 1:
            # Custom color
            for i in range(0, len(keymap)-1):
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


    # Check for keypad event
    ev = keys.events.get()
    if ev is not None:
        # Reset idle timer
        idle_time = time.monotonic()
        # Press or release on events
        if ev.pressed:
            # print("Pressing", keymap[ev.key_number])
            for key in keymap[ev.key_number]:
                kbd.press(key)
            pressed[ev.key_number] = 1
            num_pressed+=1
        else:
            # print("Releasing", keymap[ev.key_number])
            for key in keymap[ev.key_number]:
                kbd.release(key)
            pressed[ev.key_number] = 0
