import threading

cv = threading.Condition()

SESSION_COOKIE_NAME = "cryptex-session-id"

session_key = None
master_password = None
pw_store_filename = "/home/pi/pw_store.enc"
pw_store = None

def is_valid_session(cookie):
    return cookie and session_key and cookie == session_key
