from bottle import (get, post, redirect, request, response, template)
import logging
import os

from path_util import encode_path
import shared_cfg


log = logging.getLogger(__name__)


@get('/first-time-setup')
def first_time_setup():
    if not shared_cfg.master_store:
        if not os.path.exists(shared_cfg.pw_store_filename):
            return template("first-time.html")
    return redirect("/")


@get('/create-store')
def create_store(status_msg=None):
    if not shared_cfg.master_store:
        if not os.path.exists(shared_cfg.pw_store_filename):
            return template("create-store.html", status_msg=status_msg)
    return redirect("/")


@post('/create-store')
def create_store_post():
    password = request.forms.get('password')
    password_confirm = request.forms.get('password_confirm')
    status_msg = None
    if len(password) < 1:
        status_msg = "The master password cannot be empty. Please try again."
    elif password_confirm != password:
        status_msg = "The entered passwords do not match. Please try again."

    if status_msg:
        return create_store(status_msg)

    shared_cfg.login(password)
    return redirect("/login")


@get('/change-master-password')
def change_master_password(status_msg=None):
    if shared_cfg.validate_session(request):
        return template("change-master-password.html", status_msg=status_msg)
    return redirect("/")


@post('/change-master-password')
def change_master_password_post():
    if shared_cfg.validate_session(request):
        current_password = request.forms.get('current_password')
        new_password = request.forms.get('new_password')
        new_password_confirm = request.forms.get('new_password_confirm')
        if current_password != shared_cfg.master_password:
            log.debug("Current password doesn't match saved master password.")
            return change_master_password(
                status_msg="The entered password does not match the current "
                           "password. Please try again.")
        if len(new_password) == 0:
            log.debug("New password is empty.")
            return change_master_password(
                status_msg="The new password cannot be empty. "
                           "Please try again.")
        if new_password_confirm != new_password:
            log.debug("New passwords don't match.")
            return change_master_password(
                status_msg="The new passwords do not match. "
                           "Please try again.")
        shared_cfg.change_master_password(new_password)
        return redirect("/manage"+encode_path(shared_cfg.session.path))
    return redirect("/")


@get('/login')
def login(status_msg=None):
    if not shared_cfg.master_store:
        if not os.path.exists(shared_cfg.pw_store_filename):
            return redirect("/first-time-setup")
        log.debug("Doing normal login flow.")
        return template("login.html", status_msg=status_msg)
    elif shared_cfg.is_in_keyboard_mode():
        return template("keyboard-mode.html")
    return template("login.html", status_msg=status_msg)


@post('/login')
def login_post():
    password = request.forms.get('password')
    if shared_cfg.login(password):
        shared_cfg.new_session(response)
        return redirect("/manage")
    else:
        log.debug("Login failed. Back for another round.")
        return login(status_msg="Sorry, that password didn't work. Please "
                                "try again.")

