from bottle import (get, post, redirect, request, response, template)
import logging
import os

import pw_store
import shared_cfg


log = logging.getLogger(__name__)


@get('/first-time-setup')
def first_time_setup(retry=""):
    if not shared_cfg.pw_store:
        if not os.path.exists(shared_cfg.pw_store_filename):
            return template("first_time_setup.tpl", retry=False)
    return redirect("/")


@get('/first-time-setup-retry')
def first_time_setup_retry():
    if not shared_cfg.pw_store:
        if not os.path.exists(shared_cfg.pw_store_filename):
            return template("first_time_setup.tpl", retry=True)
    return redirect("/")


@post('/first-time-setup')
def do_first_time_setup():
    password = request.forms.get('password')
    password2 = request.forms.get('password2')
    if password == password2:
        shared_cfg.cv.acquire()
        shared_cfg.pw_store = pw_store.open_pw_store(password, shared_cfg.pw_store_filename)
        if shared_cfg.pw_store:
            shared_cfg.master_password = password
            shared_cfg.new_session(response)
        else:
            shared_cfg.master_password = None
        shared_cfg.cv.release()
        return redirect("/")
    else:
        return redirect("/first-time-setup-retry")


@get('/change-master-password')
def change_master_password():
    if shared_cfg.validate_session(request):
        return template("change_master_password.tpl", bad_master=False, mismatch=False)
    return redirect("/")


@get('/change-master-password-retry-bad-master')
def change_master_password_retry_bad_master():
    if shared_cfg.validate_session(request):
        return template("change_master_password.tpl", bad_master=True, mismatch=False)
    return redirect("/")


@get('/change-master-password-retry-mismatch')
def change_master_password_retry_mismatch():
    if shared_cfg.validate_session(request):
        return template("change_master_password.tpl", bad_master=False, mismatch=True)
    return redirect("/")


@post('/change-master-password')
def change_master_password():
    if shared_cfg.validate_session(request):
        if request.forms.get("change"):
            existing_password = request.forms.get('existing_password')
            new_password = request.forms.get('new_password')
            new_password_confirm = request.forms.get('new_password_confirm')
            if existing_password != shared_cfg.master_password:
                return redirect("/change-master-password-retry-bad-master")
            if new_password != new_password_confirm:
                return redirect("/change-master-password-retry-mismatch")
            shared_cfg.cv.acquire()
            shared_cfg.master_password = new_password
            pw_store.save_pw_store(shared_cfg.pw_store, new_password, shared_cfg.pw_store_filename)
            shared_cfg.cv.release()
            return template("index.tpl", status_msg="Master password successfully changed.")
        return template("index.tpl", status_msg="Master password unchanged.")
    return redirect("/")


@get('/login-retry')
def login_retry():
    if not shared_cfg.pw_store:
        if not os.path.exists(shared_cfg.pw_store_filename):
            return redirect("/first-time-setup")
        return template("login.tpl", retry=True)
    return redirect("/")


@get('/login')
def login():
    if not shared_cfg.pw_store:
        if not os.path.exists(shared_cfg.pw_store_filename):
            return redirect("/first-time-setup")
        return template("login.tpl", retry=False)
    elif shared_cfg.is_in_keyboard_mode():
        # We're in keyboard mode. TODO: How to get back to web interface mode?
        log.warn("Uhh, what now? Device handshake or just slam back into web mode?")
        return template("activate_keyboard_mode.tpl", title="Keyboard Mode")
    return template("login.tpl", retry=False)


@post('/login')
def handle_login_post():
    password = request.forms.get('password')
    shared_cfg.cv.acquire()
    shared_cfg.pw_store = pw_store.open_pw_store(password, shared_cfg.pw_store_filename)
    if shared_cfg.pw_store:
        shared_cfg.master_password = password
        shared_cfg.new_session(response)
    else:
        shared_cfg.master_password = None
    shared_cfg.cv.release()
    if not shared_cfg.pw_store:
        return redirect("/login-retry")
    else:
        return template("index.tpl", status_msg="")
