from datetime import datetime, timedelta
import logging
import threading
import uuid

from pw_store import save_pw_store

cv = threading.Condition()

SESSION_COOKIE_NAME = "cryptex-session-id"


class Session:
    def __init__(self):
        self.key = None
        self.last_active_time = None
        self.timeout_seconds = 60
        self.path = "/"


session = None

keyboard_mode = False
master_password = None
pw_store_filename = "/home/pi/pw_store.enc"
pw_store = None


log = logging.getLogger(__name__)


def new_session(response):
    """Creates a new session and adds to the response a cookie with the session
    key"""
    global session

    session = Session()

    session.key = str(uuid.uuid4())
    response.set_cookie(SESSION_COOKIE_NAME, session.key, secure=True)
    session.last_active_time = datetime.now()
    log.debug("Creating new session with key '{0}'".format(session.key))


def validate_session(request):
    ''' Returns True if there is a current session and its session ID matches
    the session ID of the passed-in request. If the session is valid, the
    session timeout will be reset. '''
    global session

    if not session:
        log.debug("Session invalid due to no session object")
        return False

    if not session.last_active_time:
        log.debug("Session invalid due to no last active time")
        return False

    if does_session_match(request.get_cookie(SESSION_COOKIE_NAME)):
        delta = datetime.now() - session.last_active_time
        if delta.total_seconds() <= session.timeout_seconds:
            log.debug("Session valid; resetting timeout")
            session.last_active_time = datetime.now()
            return True

        log.debug("Session invalid due to timeout")
        session = None
    else:
        log.debug("Session invalid due to cookie mismatch")

    return False


def is_session_active():
    ''' Returns True if there is an active session.'''
    return session is not None


def does_session_match(cookie):
    return cookie and session and session.key and cookie == session.key


def is_in_keyboard_mode():
    return keyboard_mode


def activate_keyboard_mode():
    global keyboard_mode, pw_store, master_password, session
    cv.acquire()
    if pw_store and master_password:
        save_pw_store(pw_store, master_password, pw_store_filename)
    master_password = None
    session = None
    keyboard_mode = True
    cv.release()


def lock_store():
    global pw_store, master_password, session
    cv.acquire()
    if pw_store and master_password:
        save_pw_store(pw_store, master_password, pw_store_filename)
    pw_store = None
    master_password = None
    session.key = None
    cv.release()
