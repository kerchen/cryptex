import RPi.GPIO as GPIO
import curses
from datetime import datetime
import io
import os
import sys
import time
import subprocess

this_script_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(this_script_dir, 'pyLCD'))

MODE_SWITCH_SCRIPT = "/home/pi/switch-mode.sh"

# TFT buttons
SWITCH_MODE_BUTTON_PIN = 15
SEND_PASSWORD_BUTTON_PIN = 11
TFT_BUTTON_3_PIN = 16
TFT_BUTTON_4_PIN = 13

# Button label positions are determined empirically and are dependent on
# character resolution.
# Dictionary key is max x character position.
BTN_LABEL_X_POS = {
        40 : [ 3, 15, 26, 37 ]
        }

# Encoder inputs
ENC_A_PIN = 40
ENC_B_PIN = 38
ENC_BUTTON_PIN = 35
#ENC_BIT4_PIN = 36
ENC_COMMON_PIN = 33
ENC_QUAD_PINS = [ ENC_B_PIN, ENC_A_PIN ]

CW_ORDER = [ 1, 3, 0, 2 ]
CCW_ORDER = [ 2, 0, 3, 1 ]

HID_USB_MODE = 1
RNDIS_USB_MODE = 2

def setup_gpio():
    GPIO.setmode(GPIO.BOARD) # RPi pin-numbering scheme
    
    GPIO.setup(SWITCH_MODE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(SWITCH_MODE_BUTTON_PIN, GPIO.RISING, bouncetime=200)

    GPIO.setup(SEND_PASSWORD_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(SEND_PASSWORD_BUTTON_PIN, GPIO.RISING, bouncetime=200)

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

def check_gpio(mode, current_enc_value):
    new_mode = mode
    enc_button_pressed = False

    if GPIO.event_detected(SWITCH_MODE_BUTTON_PIN):
        #print('Mode switch button pressed')
        if mode == HID_USB_MODE:
            new_mode = RNDIS_USB_MODE
        elif mode == RNDIS_USB_MODE:
            new_mode = HID_USB_MODE
        #else:
        #    print("Unknown USB mode")
        set_usb_mode(new_mode)

    if GPIO.event_detected(SEND_PASSWORD_BUTTON_PIN):
        if mode == HID_USB_MODE:
            #print('Send password button pressed')
            send_password()
        #else:
            #print('Send password button pressed but not in HID mode')

    if GPIO.event_detected(ENC_BUTTON_PIN):
        enc_button_pressed = True

    encoder_changed = False
    for pin in ENC_QUAD_PINS:
        if GPIO.event_detected(pin):
            #print("Event for pin {0} detected".format(pin))
            encoder_changed = True

    new_enc_value = current_enc_value
    if encoder_changed:
        new_enc_value = get_enc_value()

    return new_mode, new_enc_value, enc_button_pressed

def set_usb_mode(mode):
    if True:
        print("NOT setting USB mode.")
        return

    if mode == HID_USB_MODE:
        subprocess.call([MODE_SWITCH_SCRIPT, "hid"])
    elif mode == RNDIS_USB_MODE:
        subprocess.call([MODE_SWITCH_SCRIPT, "rndis"])
    else:
        print("Unknown USB mode requested.")

def send_password():
    dev = io.open("/dev/hidg0","wb")
    dev.write("\0\0\4\0\0\0\0\0")
    dev.write("\0\0\0\0\0\0\0\0")
    dev.close()

def cryptex(stdscr):
    mode = RNDIS_USB_MODE
    #set_usb_mode(mode)
    enc_value = get_enc_value()
    selection = 0

    curses.curs_set(0) # Turn off cursor
    maxy, maxx = stdscr.getmaxyx()
    stdscr.border()

    stdscr.addstr(1, 1, "Screen dimensions: {0} x {1}".format(maxx, maxy))
    for x in range(0,maxx):
        stdscr.addstr(maxy-2, x, "{0}".format(x%10))
    stdscr.addstr(1, 1, "Screen dimensions: {0} x {1}".format(maxx, maxy))
    for b in range(0,4):
        stdscr.addstr(maxy-1, BTN_LABEL_X_POS[maxx][b], "{0}".format(b+1))
    stdscr.refresh()

    try:
        while 1:
            stdscr.addstr(2, 1, 
                    "{0}".format(datetime.now().strftime("%Y %m %d %H:%M:%S")))
            mode, new_enc_value, eb_pressed = check_gpio(mode, enc_value)
            #if eb_pressed:
                # do something
            if new_enc_value != enc_value:
                if new_enc_value == CW_ORDER[enc_value]:
                    selection += 1
                elif new_enc_value == CCW_ORDER[enc_value]:
                    selection -= 1
                stdscr.addstr(3, 1, "Selection: {0:<5}".format(selection))
                enc_value = new_enc_value

            stdscr.refresh()
    except KeyboardInterrupt:
        GPIO.cleanup()


def main():
    setup_gpio()

    curses.wrapper(cryptex)

    sys.exit(0)

if __name__ == "__main__":
    main()
