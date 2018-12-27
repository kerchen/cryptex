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
        return template("change-master-password.html", retry=False)
    return redirect("/")


@get('/change-master-password-retry')
def change_master_password_retry():
    if shared_cfg.validate_session(request):
        return template("change-master-password.html", retry=True)
    return redirect("/")


@post('/change-master-password')
def change_master_password():
    if shared_cfg.validate_session(request):
        current_password = request.forms.get('current_password')
        new_password = request.forms.get('new_password')
        if current_password != shared_cfg.master_password:
            log.debug("Current password doesn't match saved master password.")
            return redirect("/change-master-password-retry")
        shared_cfg.change_master_password(new_password)
        return template("manage-store.html",
                        path="/",
                        status_msg="Master password successfully changed.")
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
        return template("keyboard-mode.html")
    return template("login.html", retry=False)


@post('/login')
def handle_login_post():
    password = request.forms.get('password')
    if shared_cfg.login(password):
        shared_cfg.new_session(response)
        return redirect("/manage")
    else:
        return redirect("/login-retry")
