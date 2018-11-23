import curses
from datetime import datetime
import logging

import shared_cfg
import hardware

CW_ORDER = [ 1, 3, 0, 2 ]
CCW_ORDER = [ 2, 0, 3, 1 ]

# Button label positions are determined empirically and are dependent on
# character resolution.
# Dictionary key is max x character position.
BTN_LABEL_X_POS = {
        40 : [ 3, 15, 26, 37 ],
        120 : [ 3, 15, 26, 37 ]
        }

log = logging.getLogger(__name__)


def cryptex(stdscr):
    mode = shared_cfg.RNDIS_USB_MODE
    #set_usb_mode(mode)
    enc_value = hardware.get_enc_value()
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
            mode, new_enc_value, eb_pressed = hardware.check_gpio(mode, enc_value)
            #if eb_pressed:
                # do something
            if new_enc_value != enc_value:
                if new_enc_value == CW_ORDER[enc_value]:
                    selection += 1
                elif new_enc_value == CCW_ORDER[enc_value]:
                    selection -= 1
                stdscr.addstr(3, 1, "Selection: {0:<5}".format(selection))
                enc_value = new_enc_value
            stdscr.addstr(4, 1, "PW store loaded: {0}".format(
                "Yes" if shared_cfg.master_store else "No" ))

            stdscr.refresh()
    except KeyboardInterrupt:
        hardware.GPIO.cleanup()

