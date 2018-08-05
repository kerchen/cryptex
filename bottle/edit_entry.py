from bottle import (post, redirect, request, route, template)
import logging
import os


import shared_cfg

log = logging.getLogger(__name__)


EDIT_ENTRY_TEMPLATE = "edit_entry.tpl"


@route('/edit<path:path>')
def edit_entry(path):
    if shared_cfg.validate_session(request):
        log.debug("Routing to path '{0}' for editing".format(path))
        shared_cfg.change_session_path(path)
        return template(EDIT_ENTRY_TEMPLATE, title="Edit Entry", path=path)
    return redirect("/")

@post('/removeentry<path:path>')
def handle_remove_entry_post(path):
    if shared_cfg.validate_session(request):
        log.debug("Removing entry '{0}'".format(path))
        cont_path, _ = os.path.split(path)
        shared_cfg.remove_entry(path)
        return redirect("/manage{0}".format(cont_path))
    return redirect("/")
