from datetime import datetime, timedelta
import logging
import threading
import uuid

from pw_store import save_pw_store

cv = threading.Condition()

SESSION_COOKIE_NAME = "cryptex-session-id"

session_key = None
session_last_active_time = None
session_timeout_seconds = 60
keyboard_mode = False
master_password = None
pw_store_filename = "/home/pi/pw_store.enc"
pw_store = None


log = logging.getLogger(__name__)


def new_session(response):
    """Make a new session key, add to the response a cookie with the session
    key and return the new session key"""
    global session_last_active_time

    key = str(uuid.uuid4())
    response.set_cookie(SESSION_COOKIE_NAME, key, secure=True)
    session_last_active_time = datetime.now()
    log.debug("Creating new session with key '{0}'".format(key))

    return key


def validate_session(request):
    ''' Returns True if there is a current session and its session ID matches
    the session ID of the passed-in request. If the session is valid, the
    session timeout will be reset. '''
    global session_key, session_last_active_time

    if not session_last_active_time:
        log.debug("Session invalid due to no last active time")
        return False

    if does_session_match(request.get_cookie(SESSION_COOKIE_NAME)):
        delta = datetime.now() - session_last_active_time
        if delta.total_seconds() <= session_timeout_seconds:
            log.debug("Session valid; resetting timeout")
            session_last_active_time = datetime.now()
            return True

        log.debug("Session invalid due to timeout")
        session_key = None
    else:
        log.debug("Session invalid due to cookie mismatch")

    return False


def is_session_active():
    ''' Returns True if there is an active session.'''
    return session_key is not None


def does_session_match(cookie):
    return cookie and session_key and cookie == session_key


def is_in_keyboard_mode():
    return keyboard_mode


def activate_keyboard_mode():
    global keyboard_mode, pw_store, master_password, session_key
    cv.acquire()
    if pw_store and master_password:
        save_pw_store(pw_store, master_password, pw_store_filename)
    master_password = None
    session_key = None
    keyboard_mode = True
    cv.release()


def lock_store():
    global pw_store, master_password, session_key
    cv.acquire()
    if pw_store and master_password:
        save_pw_store(pw_store, master_password, pw_store_filename)
    pw_store = None
    master_password = None
    session_key = None
    cv.release()
