from bottle import (post, redirect, request, route, static_file)
import logging

import shared_cfg

log = logging.getLogger(__name__)


@route('/lock')
def lock():
    if shared_cfg.validate_session(request):
        log.debug("Locking the whole thing down")
        shared_cfg.lock_store()
        return static_file("/lock.html", root="web-root")
    return redirect("/")


@route('/activate')
def activate():
    if shared_cfg.validate_session(request):
        log.debug("Activating the device")
        shared_cfg.activate_keyboard_mode()
        return static_file("/activate.html", root="web-root")
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
        return redirect("/manage.html")
    return redirect("/")


@post('/main_menu')
def do_main_menu():
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


