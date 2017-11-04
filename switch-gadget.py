import RPi.GPIO as GPIO
import io
import time
import subprocess

MODE_SWITCH_SCRIPT = "/home/pi/switch-mode.sh"

SWITCH_MODE_BUTTON_PIN = 7
SEND_PASSWORD_BUTTON_PIN = 11

HID_USB_MODE = 1
RNDIS_USB_MODE = 2

def setup_gpio():
    GPIO.setmode(GPIO.BOARD) # RPi pin-numbering scheme
    
    GPIO.setup(SWITCH_MODE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(SWITCH_MODE_BUTTON_PIN, GPIO.RISING, bouncetime=200)

    GPIO.setup(SEND_PASSWORD_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(SEND_PASSWORD_BUTTON_PIN, GPIO.RISING, bouncetime=200)

def check_gpio(mode):
    new_mode = mode
    if GPIO.event_detected(SWITCH_MODE_BUTTON_PIN):
        print('Mode switch button pressed')
        if mode == HID_USB_MODE:
            new_mode = RNDIS_USB_MODE
        elif mode == RNDIS_USB_MODE:
            new_mode = HID_USB_MODE
        else:
            print("Unknown USB mode")
        set_usb_mode(new_mode)

    if GPIO.event_detected(SEND_PASSWORD_BUTTON_PIN):
        if mode == HID_USB_MODE:
            print('Send password button pressed')
            send_password()
        else:
            print('Send password button pressed but not in HID mode')

    return new_mode

def set_usb_mode(mode):
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


def main():
    setup_gpio()

    mode = RNDIS_USB_MODE
    set_usb_mode(mode)

    try:
        while 1:
            mode = check_gpio(mode)
    except KeyboardInterrupt:
        GPIO.cleanup()

    sys.exit(0)


if __name__ == "__main__":
    main()
