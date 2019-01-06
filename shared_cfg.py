from datetime import datetime, timedelta
import logging
import os
import threading
import uuid

import pw_store


HID_USB_MODE = 1    # aka 'curses/keyboard' mode
RNDIS_USB_MODE = 2  # aka 'web interface' mode


class LockWrapper:
    """Wraps a lock object to make it easier to enable/disable the lock."""
    def __init__(self, enable):
        if enable:
            self.lock = threading.RLock()
        else:
            self.lock = None

    def acquire(self, block=False):
        if self.lock:
            return self.lock.acquire(block)
        else:
            return True

    def release(self):
        if self.lock:
            self.lock.release()


config_lock = LockWrapper(True)

SESSION_COOKIE_NAME = "cryptex-session-id"
ILLEGAL_NAME_CHARS = pw_store.ILLEGAL_NAME_CHARS
BASE_URL = "https://cryptex.local"


class Session:
    def __init__(self):
        self.key = None
        self.last_active_time = None
        self.timeout_seconds = 60 * 5
        self.path = "/"


session = None

device_mode = RNDIS_USB_MODE
master_password = None
pw_store_filename = "/home/pi/master_store.enc"
master_store = None


log = logging.getLogger(__name__)


def login(password):
    global config_lock, master_store, pw_store_filename, master_password

    config_lock.acquire()
    try:
        master_store = pw_store.open_pw_store(password, pw_store_filename)
        if master_store:
            master_password = password
        else:
            master_password = None
    finally:
        config_lock.release()
    return master_password is not None


def change_master_password(password):
    global config_lock, master_password, master_store, pw_store_filename

    config_lock.acquire()
    try:
        if master_store and master_password:
            master_password = password
            master_store.save(password, pw_store_filename)
    finally:
        config_lock.release()


def new_session(response):
    """Creates a new session and adds to the response a cookie with the session
    key"""
    global config_lock, session

    config_lock.acquire()
    try:
        session = Session()

        session.key = str(uuid.uuid4())
        response.set_cookie(SESSION_COOKIE_NAME, session.key, secure=True)
        session.last_active_time = datetime.now()
    finally:
        config_lock.release()

    log.debug("Creating new session with key '{0}'".format(session.key))


def validate_session(request):
    """ Returns True if there is a current session and its session ID matches
    the session ID of the passed-in request. If the session is valid, the
    session timeout will be reset. """
    global config_lock, session

    if not session:
        log.debug("Session invalid due to no session object")
        return False

    if not session.last_active_time:
        log.debug("Session invalid due to no last active time")
        return False

    if does_session_match(request.get_cookie(SESSION_COOKIE_NAME)):
        delta = datetime.now() - session.last_active_time
        log.debug("Session timeout delta: {0}".format(delta.total_seconds()))
        if delta.total_seconds() <= session.timeout_seconds:
            log.debug("Session valid; resetting timeout")
            config_lock.acquire()
            session.last_active_time = datetime.now()
            config_lock.release()
            return True

        log.debug("Session invalid due to timeout")
        config_lock.acquire()
        session = None
        config_lock.release()
    else:
        log.debug("Session invalid due to cookie mismatch")

    return False


def is_session_active():
    """ Returns True if there is an active session."""
    global session

    return session is not None


def does_session_match(cookie):
    global session

    return cookie and session and session.key and cookie == session.key


def is_in_keyboard_mode():
    global device_mode

    return device_mode == HID_USB_MODE


def add_entry(ent, ent_name, parent_path):
    global config_lock, master_store, pw_store_filename, master_password

    config_lock.acquire()
    try:
        if master_store and master_password:
            master_store.add_entry(ent, ent_name, parent_path)
            master_store.save(master_password, pw_store_filename)
    finally:
        config_lock.release()


def update_entry(entry_path, updated_name, updated_entry):
    global config_lock, master_store, pw_store_filename, master_password

    config_lock.acquire()
    try:
        if master_store and master_password:
            master_store.update_entry(entry_path, updated_name, updated_entry)
            master_store.save(master_password, pw_store_filename)
    finally:
        config_lock.release()


def move_entry(entry_path, new_parent_path):
    global config_lock, master_store, pw_store_filename, master_password

    config_lock.acquire()
    try:
        if master_store and master_password:
            parent_path, _ = os.path.split(entry_path)
            parent_container = master_store.get_container_by_path(parent_path)
            entry_name, entry = master_store.get_entry_by_path(entry_path)
            new_parent_container = master_store. \
                get_container_by_path(new_parent_path)
            if new_parent_container.has_entry(entry_name):
                ex_text = ("Destination folder already has an entry with "
                           "the name {0} in it.".format(entry_name))
                raise pw_store.ECDuplicateException(ex_text)
            # If this raises an exception, the entry hasn't been removed
            # from the old parent yet, so we shouldn't lose it.
            new_parent_container.add_entry(entry, entry_name)
            parent_container.remove_entry(entry_name)
            master_store.save(master_password, pw_store_filename)
    finally:
        config_lock.release()


def remove_entry(entry_path):
    global config_lock, master_store, pw_store_filename, master_password

    config_lock.acquire()
    try:
        if master_store and master_password:
            try:
                cont_path, entry_name = os.path.split(entry_path)
                cont = master_store.get_container_by_path(cont_path)
                cont.remove_entry(entry_name)
                master_store.save(master_password, pw_store_filename)
            finally:
                pass
    finally:
        config_lock.release()


def add_container(cont, cont_name):
    global config_lock, master_store, pw_store_filename, master_password, session

    config_lock.acquire()
    try:
        if master_store and master_password and session:
            master_store.add_container(cont, cont_name, session.path)
            master_store.save(master_password, pw_store_filename)
    finally:
        config_lock.release()


def rename_container(container_path, updated_name):
    global config_lock, master_store, pw_store_filename, master_password

    config_lock.acquire()
    try:
        if master_store and master_password:
            parent_path, current_name = os.path.split(container_path)
            parent_container = master_store.get_container_by_path(parent_path)
            parent_container.rename_container(current_name, updated_name)
            master_store.save(master_password, pw_store_filename)
    finally:
        config_lock.release()


def move_container(container_path, new_parent_path):
    global config_lock, master_store, pw_store_filename, master_password

    config_lock.acquire()
    try:
        if master_store and master_password:
            parent_path, container_name = os.path.split(container_path)
            parent_container = master_store.get_container_by_path(parent_path)
            moving_container = master_store.get_container_by_path(container_path)
            new_parent_container = master_store.\
                get_container_by_path(new_parent_path)
            if new_parent_container.has_container(container_name):
                ex_text = ("Destination folder already has a folder with "
                           "the name {0} in it.".format(container_name))
                raise pw_store.ECDuplicateException(ex_text)
            # If this raises an exception, the container hasn't been removed
            # from the old parent yet, so we shouldn't lose the container.
            new_parent_container.add_container(moving_container, container_name)
            parent_container.remove_container(container_name)
            master_store.save(master_password, pw_store_filename)
    finally:
        config_lock.release()


def remove_container(container_path):
    global config_lock, master_store, pw_store_filename, master_password

    config_lock.acquire()
    try:
        if master_store and master_password:
            try:
                parent_container, container_name = os.path.split(container_path)
                parent_container = master_store.get_container_by_path(parent_container)
                parent_container.remove_container(container_name)
                master_store.save(master_password, pw_store_filename)
            finally:
                pass
    finally:
        config_lock.release()


def change_session_path(path):
    global config_lock, master_store, session
    success = False
    config_lock.acquire()
    simp_path = pw_store.simplify_path(path)
    if session and master_store and master_store.is_valid_path(simp_path):
        log.debug("Changing session path to {0}".format(simp_path))
        session.path = simp_path
        success = True
    config_lock.release()
    return success


def get_entry_by_path(path):
    global master_store

    if master_store:
        return master_store.get_entry_by_path(path)

    return None


def get_entry_count_by_path(path):
    global master_store

    if master_store:
        return master_store.get_entry_count_by_path(path)

    return 0


def get_entries_by_path(path, reverse=False):
    global master_store

    if master_store:
        return sorted(master_store.get_entries_by_path(path),
                      key=lambda entry: str.lower(entry[0]),
                      reverse=reverse)

    return []


def get_container_name_from_path(path):
    global master_store

    if master_store:
        _, container_name = os.path.split(path)
        return container_name

    return None


def get_container_count_by_path(path):
    global master_store

    if master_store:
        return master_store.get_container_count_by_path(path)

    return 0


def get_containers_by_path(path, reverse=False):
    global master_store

    if master_store:
        return sorted(master_store.get_containers_by_path(path),
                      key=lambda cont: str.lower(cont[0]),
                      reverse=reverse)

    return []


def save_pw_store():
    global config_lock, master_store, pw_store_filename, master_password

    config_lock.acquire()
    try:
        if master_store and master_password:
            master_store.save(master_password, pw_store_filename)
    finally:
        config_lock.release()


def activate_keyboard_mode():
    global config_lock, device_mode, master_store, master_password, session

    config_lock.acquire()
    save_pw_store()
    master_password = None
    session = None
    device_mode = HID_USB_MODE
    config_lock.release()


def activate_web_mode():
    global config_lock, device_mode, master_store, master_password, session

    config_lock.acquire()
    save_pw_store()
    device_mode = RNDIS_USB_MODE
    config_lock.release()


def lock_store():
    global config_lock, master_store, master_password, session

    config_lock.acquire()
    try:
        save_pw_store()
        master_store = None
        master_password = None
        if session:
            session.key = None
        activate_web_mode()
    finally:
        config_lock.release()
