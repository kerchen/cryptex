from bottle import (post, redirect, request, route, template)
import logging

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
