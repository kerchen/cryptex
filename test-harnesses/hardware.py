import logging
import os
import sys

# Windows
if os.name == 'nt':
    import msvcrt

# Posix (Linux, OS X)
else:
    import termios
    import atexit
    from select import select

my_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(my_path, ".."))
import shared_cfg


log = logging.getLogger(__name__)


class GPIO_stub:
    """Stub implementation of GPIO"""
    def __init__(self):
        pass

    def cleanup(self):
        log.debug("Stub GPIO.cleanup()")



class KBHit:

    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''

        if os.name == 'nt':
            pass

        else:

            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)

            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

            # Support normal-terminal reset at exit
            atexit.register(self.set_normal_term)


    def set_normal_term(self):
        ''' Resets to normal terminal.  On Windows this is a no-op.
        '''

        if os.name == 'nt':
            pass

        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''

        s = ''

        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')

        else:
            return sys.stdin.read(1)


    def getarrow(self):
        ''' Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        '''

        if os.name == 'nt':
            msvcrt.getch() # skip 0xE0
            c = msvcrt.getch()
            vals = [72, 77, 80, 75]

        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]

        return vals.index(ord(c.decode('utf-8')))


    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        if os.name == 'nt':
            return msvcrt.kbhit()

        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []


GPIO = GPIO_stub()
kb = KBHit()

def set_device_mode(mode):
    log.debug("Stub set_device_mode()")


def setup_gpio():
    log.debug("Stub setup_gpio()")


def get_enc_value():
    new_val = 0
    log.debug("Stub get_enc_value()")

    return new_val


def check_gpio(current_enc_value):
    new_enc_value = current_enc_value
    enc_button_pressed = False

    CW_ORDER = [1, 3, 0, 2]
    CCW_ORDER = [2, 0, 3, 1]

    SWITCH_MODE_KEY = '1'
    LOCK_DEVICE_KEY = '4'

    # Mapping of keyboard keys to hardware buttons:
    #  Esc: no hardware equivalent; used to exit simulation
    #  -: One CCW tick of encoder knob
    #  =: One CW tick of encoder knob
    #  Return: Encoder knob button press
    #  1-4: TFT buttons, with left-most = 1

    if kb.kbhit():
        try:
            c = kb.getch()
        except UnicodeDecodeError:
            # Arrow keys will cause this exception.
            c = ' '
            pass
        if ord(c) == 27: # ESC
            log.debug("Esc pressed. Throwing keyboard exception.")
            raise KeyboardInterrupt
        if c == '=': # simulate turning knob one click CW
            log.debug("= pressed. Turning knob CW")
            new_enc_value = CW_ORDER[current_enc_value]
        elif c == '-': # simulate turning knob one click CCW
            log.debug("- pressed. Turning knob CCW")
            new_enc_value = CCW_ORDER[current_enc_value]
        elif ord(c) == 13: # carriage return
            log.debug("CR pressed. Simulating encoder button press.")
            enc_button_pressed = True
        elif c == SWITCH_MODE_KEY:
            if shared_cfg.is_in_keyboard_mode():
                log.debug("Switching mode to 'web'")
                shared_cfg.activate_web_mode()
            else:
                log.debug("Keyboard mode must be enabled from web browser.")

        else:
            log.debug("Unused key {0} pressed.".format(ord(c)))

        log.debug("Key pressed: given {0}, returning {1}, {2}".format(
            current_enc_value, new_enc_value, enc_button_pressed))

    return new_enc_value, enc_button_pressed


if __name__ == "__main__":

    kb = KBHit()

    print('Hit any key, or ESC to exit')

    while True:

        if kb.kbhit():
            c = kb.getch()
            if ord(c) == 27: # ESC
                break
            print(c)

    kb.set_normal_term()
