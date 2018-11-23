import curses
from datetime import datetime
import logging
import sys
import threading

import shared_cfg
import hardware
import hmi

sys.path.append("bottle")
import server


MODE_SWITCH_SCRIPT = "/home/pi/switch-mode.sh"
LOG_FILENAME = "/home/pi/cryptex.log"

log = logging.getLogger(__name__)


#def set_usb_mode(mode):
    #if True:
        #log.critical("NOT setting USB mode.")
        #return

    #if mode == HID_USB_MODE:
        #subprocess.call([MODE_SWITCH_SCRIPT, "hid"])
    #elif mode == RNDIS_USB_MODE:
        #subprocess.call([MODE_SWITCH_SCRIPT, "rndis"])
    #else:
        #log.warn("Unknown USB mode requested.")


def send_password():
    dev = io.open("/dev/hidg0","wb")
    dev.write("\0\0\4\0\0\0\0\0")
    dev.write("\0\0\0\0\0\0\0\0")
    dev.close()


def main():
    logging.basicConfig(filename=LOG_FILENAME, filemode='w', level=logging.DEBUG)

    hardware.setup_gpio()

    web_server_thread = threading.Thread(
            target=server.run_web_server,
            args=(False,)
            )
    web_server_thread.start()

    curses.wrapper(hmi.cryptex)

    sys.exit(0)


if __name__ == "__main__":
    main()
