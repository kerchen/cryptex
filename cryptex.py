import curses
import logging
import sys
import threading

import hardware
import hmi

sys.path.append("bottle")
import server


LOG_FILENAME = "/home/pi/cryptex.log"

log = logging.getLogger(__name__)


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
