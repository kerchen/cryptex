import RPi.GPIO as GPIO
import io
import logging

import shared_cfg


MODE_SWITCH_SCRIPT = "/home/pi/switch-mode.sh"

# TFT buttons
SWITCH_MODE_BUTTON_PIN = 15
SEND_PASSWORD_BUTTON_PIN = 11
TFT_BUTTON_3_PIN = 16
TFT_BUTTON_4_PIN = 13

# Encoder inputs
ENC_A_PIN = 40
ENC_B_PIN = 38
ENC_BUTTON_PIN = 35
#ENC_BIT4_PIN = 36
ENC_COMMON_PIN = 33
ENC_QUAD_PINS = [ ENC_B_PIN, ENC_A_PIN ]



log = logging.getLogger(__name__)


def set_device_mode(mode):
    if True:
        log.critical("NOT setting USB mode.")
        return

    if mode == HID_USB_MODE:
        subprocess.call([MODE_SWITCH_SCRIPT, "hid"])
    elif mode == RNDIS_USB_MODE:
        subprocess.call([MODE_SWITCH_SCRIPT, "rndis"])
    else:
        log.warn("Unknown device mode requested.")


def setup_gpio():
    GPIO.setwarnings(False)
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


def check_gpio(current_enc_value):
    enc_button_pressed = False

    if GPIO.event_detected(SWITCH_MODE_BUTTON_PIN):
        log.debug('Mode switch button pressed')
        if shared_cfg.is_in_keyboard_mode():
            set_device_mode(shared_cfg.RNDIS_USB_MODE)
            shared_cfg.activate_web_mode()
            return
        else:
            log.warn("Switching to 'keyboard' mode must be done in web browser.")

    if GPIO.event_detected(SEND_PASSWORD_BUTTON_PIN):
        if shared_cfg.is_in_keyboard_mode():
            log.debug('Send password button pressed')
            #send_password()
        else:
            log.debug('Send password button pressed but not in keyboard mode')

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

    return new_enc_value, enc_button_pressed


def send_password():
    dev = io.open("/dev/hidg0","wb")
    dev.write("\0\0\4\0\0\0\0\0")
    dev.write("\0\0\0\0\0\0\0\0")
    dev.close()


