import threading

cv = threading.Condition()

SESSION_COOKIE_NAME = "cryptex-session-id"

session_key = None
master_password = None
pw_store_filename = "/home/pi/pw_store.enc"
pw_store = None


def is_session_valid(request):
    ''' Returns True if there is a current session and its session ID matches
    the session ID of the passed-in request.'''
    return does_session_match(request.get_cookie(SESSION_COOKIE_NAME))


def is_session_active():
    ''' Returns True if there is an active session.'''
    print("is_session_active: Checking session key")
    return session_key != None


def does_session_match(cookie):
    return cookie and session_key and cookie == session_key


def lock_store():
    global pw_store, master_password, session_key
    cv.acquire()
    # TODO: Save password store
    pw_store = None
    master_password = None
    session_key = None
    cv.release()
