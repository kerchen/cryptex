from bottle import (post, redirect, request, route, template)
import logging

import pw_store
import shared_cfg

log = logging.getLogger(__name__)


@route('/manage<path:path>')
def manage_path(path):
    if shared_cfg.validate_session(request):
        log.debug("Routing to path {0}".format(path))
        shared_cfg.session.path = path
        return template("manage_passwords.tpl", title="Manage Passwords", path=path)
    return redirect("/")


@post('/manage')
def handle_manage_post():
    log.debug("Handling management post")
    if shared_cfg.validate_session(request):
        if request.forms.get("addentry"):
            log.debug("Add entry button pressed")
            return template("new_entry.tpl", retry=False)
        elif request.forms.get("addcontainer"):
            log.debug("Add container button pressed. path = {}".format(shared_cfg.session.path))
            return template("new_container.tpl", retry=False)
    return redirect("/")


@post('/manage-new-entry')
def handle_new_entry_post():
    log.debug("Handling new entry post")
    if shared_cfg.validate_session(request):
        if request.forms.get("create"):
            ent_name = request.forms.get('name').strip()
            username = request.forms.get('username').strip()
            password = request.forms.get('password')
            password2 = request.forms.get('password2')
            url = request.forms.get('url').strip()
            log.debug("New entry confirmed")
            log.debug("Entry Name: {}".format(ent_name))
            log.debug("Username: {}".format(username))
            log.debug("Password: {}".format(password))
            log.debug("Password 2: {}".format(password2))
            log.debug("URL: {}".format(url))
            if password != password2:
                return redirect("/master-new-entry-password-retry-mismatch")
            ent = pw_store.Entry(username=username, password=password, url=url)
            shared_cfg.pw_store.add_entry(ent, ent_name, shared_cfg.session.path)
            return redirect("/manage"+shared_cfg.session.path)
        elif request.forms.get("cancel"):
            log.debug("New entry cancelled")
            return redirect("/manage"+shared_cfg.session.path)
    return redirect("/")


@post('/manage-new-container')
def handle_new_container_post():
    log.debug("Handling new container post")
    if shared_cfg.validate_session(request):
        if request.forms.get("create"):
            cont_name = request.forms.get('name').strip()
            log.debug("New container confirmed")
            log.debug("Name: {}".format(cont_name))
            cont = pw_store.EntryContainer()
            shared_cfg.pw_store.add_container(cont, cont_name, shared_cfg.session.path)
            return redirect("/manage"+shared_cfg.session.path+"/"+cont_name)
        elif request.forms.get("cancel"):
            log.debug("New container cancelled")
            return redirect("/manage"+shared_cfg.session.path)
    return redirect("/")
