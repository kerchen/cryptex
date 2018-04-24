from bottle import (post, redirect, request, route, template)
import logging

import manage_passwords
import shared_cfg

log = logging.getLogger(__name__)


@route('/lock')
def lock():
    if shared_cfg.validate_session(request):
        log.debug("Locking the whole thing down")
        shared_cfg.lock_store()
        return template("lock.tpl", title="Cryptex Locked")
    return redirect("/")


@route('/activate')
def activate():
    if shared_cfg.validate_session(request):
        log.debug("Activating the device")
        shared_cfg.activate_keyboard_mode()
        return template("activate_keyboard_mode.tpl", title="Keyboard Mode")
    return redirect("/")


@route('/master-pass')
def master_pass():
    if shared_cfg.validate_session(request):
        log.debug("Changing master password")
        return redirect("/change-master-password")
    return redirect("/")


@route('/manage')
def manage():
    if shared_cfg.validate_session(request):
        log.debug("Managing passwords")
        return template("manage_passwords.tpl", title="Manage Passwords", path="/")
    return redirect("/")


@post('/footer')
def handle_main_menu_post():
    log.debug("Handling main menu post")
    if shared_cfg.validate_session(request):
        if request.forms.get("lock"):
            return redirect("/lock")
        elif request.forms.get("activate"):
            return redirect("/activate")
        elif request.forms.get("master_pass"):
            return redirect("/master-pass")
        elif request.forms.get("manage"):
            return redirect("/manage")
    return redirect("/")


