import RPi.GPIO as GPIO
import io
import logging
import subprocess

import shared_cfg


MODE_SWITCH_SCRIPT = "/home/pi/switch-mode.sh"

# TFT buttons; button 1 is left-most
TFT_BUTTON_1_PIN = 15   # GPIO22
TFT_BUTTON_2_PIN = 11   # GPIO17
TFT_BUTTON_3_PIN = 16   # GPIO23
TFT_BUTTON_4_PIN = 13   # GPIO27

# Encoder inputs
ENC_A_PIN = 40          # GPIO21
ENC_B_PIN = 38          # GPIO20
ENC_BUTTON_PIN = 35     # GPIO19
#ENC_BIT4_PIN = 36      # GPIO16
ENC_COMMON_PIN = 33     # GPIO13
ENC_QUAD_PINS = [ ENC_B_PIN, ENC_A_PIN ]


log = logging.getLogger(__name__)


def set_device_mode(mode):
    if mode == shared_cfg.HID_USB_MODE:
        subprocess.call([MODE_SWITCH_SCRIPT, "hid"])
    elif mode == shared_cfg.RNDIS_USB_MODE:
        subprocess.call([MODE_SWITCH_SCRIPT, "rndis"])
    else:
        log.warn("Unknown device mode requested.")


def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) # RPi pin-numbering scheme
    
    GPIO.setup(TFT_BUTTON_1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(TFT_BUTTON_1_PIN, GPIO.RISING, bouncetime=200)

    GPIO.setup(TFT_BUTTON_2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(TFT_BUTTON_2_PIN, GPIO.RISING, bouncetime=200)

    GPIO.setup(TFT_BUTTON_3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(TFT_BUTTON_3_PIN, GPIO.RISING, bouncetime=200)

    GPIO.setup(TFT_BUTTON_4_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(TFT_BUTTON_4_PIN, GPIO.RISING, bouncetime=200)

    GPIO.setup(ENC_COMMON_PIN, GPIO.OUT)
    GPIO.output(ENC_COMMON_PIN, GPIO.LOW)

    GPIO.setup(ENC_A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(ENC_A_PIN, GPIO.BOTH)

    GPIO.setup(ENC_B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(ENC_B_PIN, GPIO.BOTH)

    GPIO.setup(ENC_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(ENC_BUTTON_PIN, GPIO.RISING, bouncetime=50)

    #GPIO.setup(ENC_BIT4_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.add_event_detect(ENC_BIT4_PIN, GPIO.BOTH, bouncetime=50)


def get_enc_value():
    new_val = 0
    for pin in ENC_QUAD_PINS:
        new_val = new_val * 2 + (1 if GPIO.input(pin) else 0)
    #print("Encoder value: " + str(new_val))

    return new_val


def check_gpio(current_enc_value):
    enc_button_pressed = False
    hw_button_pressed = 0

    if GPIO.event_detected(TFT_BUTTON_1_PIN):
        hw_button_pressed = 1

    if GPIO.event_detected(TFT_BUTTON_2_PIN):
        hw_button_pressed = 2

    if GPIO.event_detected(TFT_BUTTON_3_PIN):
        hw_button_pressed = 3

    if GPIO.event_detected(TFT_BUTTON_4_PIN):
        hw_button_pressed = 4

    if GPIO.event_detected(ENC_BUTTON_PIN):
        enc_button_pressed = True

    encoder_changed = False
    for pin in ENC_QUAD_PINS:
        if GPIO.event_detected(pin):
            log.debug("Event for pin {0} detected".format(pin))
            encoder_changed = True

    new_enc_value = current_enc_value
    if encoder_changed:
        new_enc_value = get_enc_value()

    return new_enc_value, enc_button_pressed, hw_button_pressed


NULL_CHAR = chr(0)

# Standard US keyboard key code mapping
KEY_CODE_DICT = {
    'a': NULL_CHAR * 2 + chr(4) + NULL_CHAR * 5,
    'A': chr(32) + NULL_CHAR + chr(4) + NULL_CHAR * 5,
    'b': NULL_CHAR * 2 + chr(5) + NULL_CHAR * 5,
    'B': chr(32) + NULL_CHAR + chr(5) + NULL_CHAR * 5,
    'c': NULL_CHAR * 2 + chr(6) + NULL_CHAR * 5,
    'C': chr(32) + NULL_CHAR + chr(6) + NULL_CHAR * 5,
    'd': NULL_CHAR * 2 + chr(7) + NULL_CHAR * 5,
    'D': chr(32) + NULL_CHAR + chr(7) + NULL_CHAR * 5,
    'e': NULL_CHAR * 2 + chr(8) + NULL_CHAR * 5,
    'E': chr(32) + NULL_CHAR + chr(8) + NULL_CHAR * 5,
    'f': NULL_CHAR * 2 + chr(9) + NULL_CHAR * 5,
    'F': chr(32) + NULL_CHAR + chr(9) + NULL_CHAR * 5,
    'g': NULL_CHAR * 2 + chr(10) + NULL_CHAR * 5,
    'G': chr(32) + NULL_CHAR + chr(10) + NULL_CHAR * 5,
    'h': NULL_CHAR * 2 + chr(11) + NULL_CHAR * 5,
    'H': chr(32) + NULL_CHAR + chr(11) + NULL_CHAR * 5,
    'i': NULL_CHAR * 2 + chr(12) + NULL_CHAR * 5,
    'I': chr(32) + NULL_CHAR + chr(12) + NULL_CHAR * 5,
    'j': NULL_CHAR * 2 + chr(13) + NULL_CHAR * 5,
    'J': chr(32) + NULL_CHAR + chr(13) + NULL_CHAR * 5,
    'k': NULL_CHAR * 2 + chr(14) + NULL_CHAR * 5,
    'K': chr(32) + NULL_CHAR + chr(14) + NULL_CHAR * 5,
    'l': NULL_CHAR * 2 + chr(15) + NULL_CHAR * 5,
    'L': chr(32) + NULL_CHAR + chr(15) + NULL_CHAR * 5,
    'm': NULL_CHAR * 2 + chr(16) + NULL_CHAR * 5,
    'M': chr(32) + NULL_CHAR + chr(16) + NULL_CHAR * 5,
    'n': NULL_CHAR * 2 + chr(17) + NULL_CHAR * 5,
    'N': chr(32) + NULL_CHAR + chr(17) + NULL_CHAR * 5,
    'o': NULL_CHAR * 2 + chr(18) + NULL_CHAR * 5,
    'O': chr(32) + NULL_CHAR + chr(18) + NULL_CHAR * 5,
    'p': NULL_CHAR * 2 + chr(19) + NULL_CHAR * 5,
    'P': chr(32) + NULL_CHAR + chr(19) + NULL_CHAR * 5,
    'q': NULL_CHAR * 2 + chr(20) + NULL_CHAR * 5,
    'Q': chr(32) + NULL_CHAR + chr(20) + NULL_CHAR * 5,
    'r': NULL_CHAR * 2 + chr(21) + NULL_CHAR * 5,
    'R': chr(32) + NULL_CHAR + chr(21) + NULL_CHAR * 5,
    's': NULL_CHAR * 2 + chr(22) + NULL_CHAR * 5,
    'S': chr(32) + NULL_CHAR + chr(22) + NULL_CHAR * 5,
    't': NULL_CHAR * 2 + chr(23) + NULL_CHAR * 5,
    'T': chr(32) + NULL_CHAR + chr(23) + NULL_CHAR * 5,
    'u': NULL_CHAR * 2 + chr(24) + NULL_CHAR * 5,
    'U': chr(32) + NULL_CHAR + chr(24) + NULL_CHAR * 5,
    'v': NULL_CHAR * 2 + chr(25) + NULL_CHAR * 5,
    'V': chr(32) + NULL_CHAR + chr(25) + NULL_CHAR * 5,
    'w': NULL_CHAR * 2 + chr(26) + NULL_CHAR * 5,
    'W': chr(32) + NULL_CHAR + chr(26) + NULL_CHAR * 5,
    'x': NULL_CHAR * 2 + chr(27) + NULL_CHAR * 5,
    'X': chr(32) + NULL_CHAR + chr(27) + NULL_CHAR * 5,
    'y': NULL_CHAR * 2 + chr(28) + NULL_CHAR * 5,
    'Y': chr(32) + NULL_CHAR + chr(28) + NULL_CHAR * 5,
    'z': NULL_CHAR * 2 + chr(29) + NULL_CHAR * 5,
    'Z': chr(32) + NULL_CHAR + chr(29) + NULL_CHAR * 5,
    '1': NULL_CHAR * 2 + chr(30) + NULL_CHAR * 5,
    '!': chr(32) + NULL_CHAR + chr(30) + NULL_CHAR * 5,
    '2': NULL_CHAR * 2 + chr(31) + NULL_CHAR * 5,
    '@': chr(32) + NULL_CHAR + chr(31) + NULL_CHAR * 5,
    '3': NULL_CHAR * 2 + chr(32) + NULL_CHAR * 5,
    '#': chr(32) + NULL_CHAR + chr(32) + NULL_CHAR * 5,
    '4': NULL_CHAR * 2 + chr(33) + NULL_CHAR * 5,
    '$': chr(32) + NULL_CHAR + chr(33) + NULL_CHAR * 5,
    '5': NULL_CHAR * 2 + chr(34) + NULL_CHAR * 5,
    '%': chr(32) + NULL_CHAR + chr(34) + NULL_CHAR * 5,
    '6': NULL_CHAR * 2 + chr(35) + NULL_CHAR * 5,
    '^': chr(32) + NULL_CHAR + chr(35) + NULL_CHAR * 5,
    '7': NULL_CHAR * 2 + chr(36) + NULL_CHAR * 5,
    '&': chr(32) + NULL_CHAR + chr(36) + NULL_CHAR * 5,
    '8': NULL_CHAR * 2 + chr(37) + NULL_CHAR * 5,
    '*': chr(32) + NULL_CHAR + chr(37) + NULL_CHAR * 5,
    '9': NULL_CHAR * 2 + chr(38) + NULL_CHAR * 5,
    '(': chr(32) + NULL_CHAR + chr(38) + NULL_CHAR * 5,
    '0': NULL_CHAR * 2 + chr(39) + NULL_CHAR * 5,
    ')': chr(32) + NULL_CHAR + chr(39) + NULL_CHAR * 5,
    ' ': NULL_CHAR * 2 + chr(44) + NULL_CHAR * 5,
    '-': NULL_CHAR * 2 + chr(45) + NULL_CHAR * 5,
    '_': chr(32) + NULL_CHAR + chr(45) + NULL_CHAR * 5,
    '=': NULL_CHAR * 2 + chr(46) + NULL_CHAR * 5,
    '+': chr(32) + NULL_CHAR + chr(46) + NULL_CHAR * 5,
    '[': NULL_CHAR * 2 + chr(47) + NULL_CHAR * 5,
    '{': chr(32) + NULL_CHAR + chr(47) + NULL_CHAR * 5,
    ']': NULL_CHAR * 2 + chr(48) + NULL_CHAR * 5,
    '}': chr(32) + NULL_CHAR + chr(48) + NULL_CHAR * 5,
    '\\': NULL_CHAR * 2 + chr(49) + NULL_CHAR * 5,
    '|': chr(32) + NULL_CHAR + chr(49) + NULL_CHAR * 5,
    '`': NULL_CHAR * 2 + chr(50) + NULL_CHAR * 5,
    '~': chr(32) + NULL_CHAR + chr(50) + NULL_CHAR * 5,
    ';': NULL_CHAR * 2 + chr(51) + NULL_CHAR * 5,
    ':': chr(32) + NULL_CHAR + chr(51) + NULL_CHAR * 5,
    '\'': NULL_CHAR * 2 + chr(52) + NULL_CHAR * 5,
    '"': chr(32) + NULL_CHAR + chr(52) + NULL_CHAR * 5,
    ',': NULL_CHAR * 2 + chr(54) + NULL_CHAR * 5,
    '<': chr(32) + NULL_CHAR + chr(54) + NULL_CHAR * 5,
    '.': NULL_CHAR * 2 + chr(55) + NULL_CHAR * 5,
    '>': chr(32) + NULL_CHAR + chr(55) + NULL_CHAR * 5,
    '/': NULL_CHAR * 2 + chr(56) + NULL_CHAR * 5,
    '?': chr(32) + NULL_CHAR + chr(56) + NULL_CHAR * 5
}

def write_report(report):
    with io.open("/dev/hidg0","wb") as dev:
        dev.write(report.encode())


def keyboard_out(text):
    last_char = None
    for c in text:
        if c == last_char:
            write_report(NULL_CHAR * 8)
        write_report(KEY_CODE_DICT[c])
        last_char = c

    write_report(NULL_CHAR*8)
