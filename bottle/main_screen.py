from bottle import (post, redirect, request, route, static_file)

import shared_cfg


@route('/lock')
def lock():
    if shared_cfg.is_session_valid(request):
        print("Locking the whole thing down")
        shared_cfg.lock_store()
        return static_file("/lock.html", root="web-root")
    return redirect("/")


@route('/activate')
def activate():
    if shared_cfg.is_session_valid(request):
        print("Activating the device")
        return redirect("/activate.html")
    return redirect("/")


@route('/master-pass')
def master_pass():
    if shared_cfg.is_session_valid(request):
        print("Changing master password")
        return redirect("/master-pass.html")
    return redirect("/")


@route('/manage')
def manage():
    if shared_cfg.is_session_valid(request):
        print("Managing passwords")
        return redirect("/manage.html")
    return redirect("/")


@post('/main_menu')
def do_main_menu():
    if shared_cfg.is_session_valid(request):
        if request.forms.get("lock"):
            return redirect("/lock")
        elif request.forms.get("activate"):
            return redirect("/activate")
        elif request.forms.get("master_pass"):
            return redirect("/master-pass")
        elif request.forms.get("manage"):
            return redirect("/manage")
    return redirect("/")


