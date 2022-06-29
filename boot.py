# Import necessary libraries
# For inputs
import board
import digitalio
# For disabling functions
import storage
import usb_cdc
import usb_midi
# For resetting to bootloader
import microcontroller
# For indicator
import neopixel
# For sleep
import time

# For keyboard
import usb_hid
REPORT_ID = 0x4
REPORT_BYTES = 16
bitmap_keyboard_descriptor = bytes((
        0x05, 0x01,                     # Usage Page (Generic Desktop),
        0x09, 0x06,                     # Usage (Keyboard),
        0xA1, 0x01,                     # Collection (Application),
        0x85, REPORT_ID,                #   Report ID
        # bitmap of modifiers
        0x75, 0x01,                     #   Report Size (1),
        0x95, 0x08,                     #   Report Count (8),
        0x05, 0x07,                     #   Usage Page (Key Codes),
        0x19, 0xE0,                     #   Usage Minimum (224),
        0x29, 0xE7,                     #   Usage Maximum (231),
        0x15, 0x00,                     #   Logical Minimum (0),
        0x25, 0x01,                     #   Logical Maximum (1),
        0x81, 0x02,                     #   Input (Data, Variable, Absolute), ;Modifier byte
        # LED output report
        0x95, 0x05,                     #   Report Count (5),
        0x75, 0x01,                     #   Report Size (1),
        0x05, 0x08,                     #   Usage Page (LEDs),
        0x19, 0x01,                     #   Usage Minimum (1),
        0x29, 0x05,                     #   Usage Maximum (5),
        0x91, 0x02,                     #   Output (Data, Variable, Absolute),
        0x95, 0x01,                     #   Report Count (1),
        0x75, 0x03,                     #   Report Size (3),
        0x91, 0x03,                     #   Output (Constant),
        # bitmap of keys
        0x95, (REPORT_BYTES-1)*8,       #   Report Count (),
        0x75, 0x01,                     #   Report Size (1),
        0x15, 0x00,                     #   Logical Minimum (0),
        0x25, 0x01,                     #   Logical Maximum(1),
        0x05, 0x07,                     #   Usage Page (Key Codes),
        0x19, 0x00,                     #   Usage Minimum (0),
        0x29, (REPORT_BYTES-1)*8-1,     #   Usage Maximum (),
        0x81, 0x02,                     #   Input (Data, Variable, Absolute),
        0xc0                            # End Collection
))

bitmap_keyboard = usb_hid.Device(
    report_descriptor=bitmap_keyboard_descriptor,
    usage_page=0x1,
    usage=0x6,
    report_ids=(REPORT_ID,),
    in_report_lengths=(REPORT_BYTES,),
    out_report_lengths=(1,),
)

usb_hid.enable(
    (
        bitmap_keyboard,
        usb_hid.Device.MOUSE,
        usb_hid.Device.CONSUMER_CONTROL,
    )
)
print("Enabled HID with custom keyboard device.")


# Initialize keys
pins = [board.D2, board.D3, board.D1]
keys = []
for pin in pins:
    key = digitalio.DigitalInOut(pin)
    key.direction = digitalio.Direction.INPUT
    key.pull = digitalio.Pull.UP
    keys.append(key)

# Indicator
pixels = neopixel.NeoPixel(board.D0, 4, brightness=1, auto_write=False)
color = [ 0, 255, 0 ]

# Enable functions depending on keys held
if keys[0].value:
    storage.disable_usb_drive()
    color[0] = 255
else:
    print("Key 1 held at boot, enabling mass storage device.")
if keys[1].value:
    usb_cdc.disable()
    color[2] = 255
else:
    print("Key 2 held at boot, enabling serial connection.")
if not keys[2].value:
    microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
    microcontroller.reset()
    print("Key 3 held at boot, resetting to bootloader.")

# Set LED
pixels.fill((color[0], color[1], color[2]))
pixels.show()

# Disable MIDI
usb_midi.disable()

time.sleep(0.2)

