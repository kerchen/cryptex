from bottle import (get, post, route, response, run, redirect, request,
                    static_file, ServerAdapter, default_app)
import os

import db_setup
import shared_cfg


def confirm_password_form(retry):
    form = '<form action="/first-time-setup" method="post">'
    if retry:
        form += "Entered passwords did not match. Please try again.</br>"
    form += '''
                Password database does not exist. Creating new one.</br>
                Password: <input name="password" type="password"/> </br>
                Re-enter Password: <input name="password2" type="password" />
                <input value="Create" type="submit" />
                </form>
            '''
    return form


@get('/first-time-setup')
def first_time_setup(retry=""):
    if not shared_cfg.db_conn:
        if not os.path.exists(shared_cfg.encrypted_db_filename):
            return confirm_password_form(False)
    redirect("/")


@get('/first-time-setup-retry')
def first_time_setup_retry():
    if not shared_cfg.db_conn:
        if not os.path.exists(shared_cfg.encrypted_db_filename):
            return confirm_password_form(True)
    redirect("/")


@post('/first-time-setup')
def do_first_time_setup():
    print("In do_first_time_setup()")
    password = request.forms.get('password')
    password2 = request.forms.get('password2')
    if password == password2:
        shared_cfg.cv.acquire()
        shared_cfg.db_conn = db_setup.open_encrypted_db(password)
        shared_cfg.cv.release()
        redirect("/")
    else:
        redirect("/first-time-setup-retry")


def enter_password_form(retry):
    form = '<form action="/login" method="post">'
    if retry:
        form += "Entered password didn't work. Please try again.</br>"
    form += '''
                Password: <input name="password" type="password" />
                <input value="Login" type="submit" />
                </form>
            '''
    return form


@get('/login-retry')
def login_retry():
    if not shared_cfg.db_conn:
        if not os.path.exists(shared_cfg.encrypted_db_filename):
            redirect("/first-time-setup")
            return ''
        return enter_password_form(True)
    redirect("/")


@get('/login')
def login():
    if not shared_cfg.db_conn:
        if not os.path.exists(shared_cfg.encrypted_db_filename):
            redirect("/first-time-setup")
            return ''
        return enter_password_form(False)
    redirect("/")


@post('/login')
def do_login():
    password = request.forms.get('password')
    shared_cfg.cv.acquire()
    shared_cfg.db_conn = db_setup.open_encrypted_db(password)
    shared_cfg.cv.release()
    if not shared_cfg.db_conn:
        redirect("/login-retry")
    else:
        redirect("/")
