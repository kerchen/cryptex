import curses
import logging
import os
import threading
import sys

my_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(my_path, ".."))
import shared_cfg
import hmi

# Override settings from shared config.
shared_cfg.pw_store_filename = os.path.join(my_path, "..", "master_store.enc")

sys.path.append(os.path.join(my_path, "..", "bottle"))
import server


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def worker():
    server.run_web_server(True)

def main():
    log.info("Starting web server")

    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

    log.info("Starting curses")
    curses.wrapper(hmi.cryptex)

    sys.exit(0)


if __name__ == "__main__":
    main()
