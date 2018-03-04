import sys
import os

my_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(my_path, ".."))
import shared_cfg

# Override settings from shared config.
shared_cfg.db_filename = os.path.join(my_path, "..", "cryptex.db")
shared_cfg.encrypted_db_filename = shared_cfg.db_filename + ".enc"

print(os.path.join(my_path, "..", "bottle"))
sys.path.append(os.path.join(my_path, "..", "bottle"))
import server

def main():
    server.run_web_server(True)

    sys.exit(0)


if __name__ == "__main__":
    main()
