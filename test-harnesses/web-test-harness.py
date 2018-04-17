import logging
import sys
import os

my_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(my_path, ".."))
import shared_cfg

# Override settings from shared config.
shared_cfg.pw_store_filename = os.path.join(my_path, "..", "master_store.enc")

sys.path.append(os.path.join(my_path, "..", "bottle"))
import server


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def main():
    log.info("Starting web server")
    server.run_web_server(True)

    sys.exit(0)


if __name__ == "__main__":
    main()
