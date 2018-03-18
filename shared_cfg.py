import threading

cv = threading.Condition()

master_password = None
pw_store_filename = "/home/pi/pw_store.enc"
pw_store = None
