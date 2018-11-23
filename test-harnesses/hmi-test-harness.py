import curses
import logging
import sys
import os


my_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(my_path, ".."))

import hmi

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def main():
    log.info("Starting curses")
    curses.wrapper(hmi.cryptex)

    sys.exit(0)


if __name__ == "__main__":
    main()
