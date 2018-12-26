from bottle import (get, post, redirect, request, response, template)
import logging
import os

import shared_cfg


log = logging.getLogger(__name__)


@get('/first-time-setup')
def first_time_setup():
    if not shared_cfg.master_store:
        if not os.path.exists(shared_cfg.pw_store_filename):
            return template("first-time.html")
    return redirect("/")


@get('/create-store')
def create_store():
    if not shared_cfg.master_store:
        if not os.path.exists(shared_cfg.pw_store_filename):
            return template("create-store.html")
    return redirect("/")


@post('/create-store')
def do_create_store():
    password = request.forms.get('password')
    shared_cfg.login(password)
    return redirect("/login")


@get('/change-master-password')
def change_master_password():
    if shared_cfg.validate_session(request):
        return template("change-master-password.html", bad_master=False, mismatch=False)
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
            shared_cfg.change_master_password(new_password)
            return template("index.tpl",
                            status_msg="Master password successfully changed.")
        return template("index.tpl", status_msg="Master password unchanged.")
    return redirect("/")


@get('/login-retry')
def login_retry():
    if not shared_cfg.master_store:
        if not os.path.exists(shared_cfg.pw_store_filename):
            return redirect("/first-time-setup")
        return template("login.html", retry=True)
    return redirect("/")


@get('/login')
def login():
    if not shared_cfg.master_store:
        if not os.path.exists(shared_cfg.pw_store_filename):
            return redirect("/first-time-setup")
        return template("login.html", retry=False)
    elif shared_cfg.is_in_keyboard_mode():
        return template("activate_keyboard_mode.tpl", title="Keyboard Mode")
    return template("login.html", retry=False)


@post('/login')
def handle_login_post():
    password = request.forms.get('password')
    if shared_cfg.login(password):
        shared_cfg.new_session(response)
        return redirect("/manage")
    else:
        return redirect("/login-retry")
