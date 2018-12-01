import curses
import logging
import os
import threading
import sys

# This script can be used to exercise most of the system's functionality when
# the actual hardware isn't available.

# TODO: Figure out how to merge this file with cryptex.py so that two
# nearly-identical files don't need to be maintained.

# Import hardware module before adding '..' to the path so that we get the
# hardware stubs instead of the actual hardware functions.
import hardware

my_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(my_path, ".."))
import shared_cfg
import hmi

# Override settings from shared config.
shared_cfg.pw_store_filename = os.path.join(my_path, "..", "master_store.enc")

sys.path.append(os.path.join(my_path, "..", "bottle"))
import server


log = logging.getLogger(__name__)


def main():
    logging.basicConfig(filename="hardware-sim.log", filemode="w", level=logging.DEBUG)

    hardware.setup_gpio()

    log.info("Starting web server")
    web_server_thread = threading.Thread(
        target=server.run_web_server,
        args=(False,)
    )
    web_server_thread.daemon = True
    web_server_thread.start()

    log.info("Starting curses HMI")
    curses.wrapper(hmi.cryptex)

    sys.exit(0)


if __name__ == "__main__":
    main()
