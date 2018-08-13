from bottle import (post, redirect, request, route, template)
import logging
import os

import pw_store
import shared_cfg

log = logging.getLogger(__name__)


EDIT_ENTRY_TEMPLATE = "edit_entry.tpl"


@route('/edit<path:path>')
def edit_entry(path):
    if shared_cfg.validate_session(request):
        log.debug("Routing to path '{0}' for editing".format(path))
        shared_cfg.change_session_path(path)
        return template(EDIT_ENTRY_TEMPLATE, title="Edit Entry", path=path, retry="")
    return redirect("/")


@post('/cancelupdate<path:path>')
def handle_cancel_update_post(path):
    if shared_cfg.validate_session(request):
        log.debug("Cancelling entry edit of '{0}'".format(path))
        cont_path, _ = os.path.split(path)
        return redirect("/manage{0}".format(cont_path))
    return redirect("/")


@post('/removeentry<path:path>')
def handle_remove_entry_post(path):
    if shared_cfg.validate_session(request):
        log.debug("Removing entry '{0}'".format(path))
        cont_path, _ = os.path.split(path)
        shared_cfg.remove_entry(path)
        return redirect("/manage{0}".format(cont_path))
    return redirect("/")


@post('/updateentry<path:path>')
def handle_update_entry_post(path):
    if shared_cfg.validate_session(request):
        template_name = EDIT_ENTRY_TEMPLATE
        retry_reason = None
        entry_name = request.forms.get('name').strip()
        username = request.forms.get('username').strip()
        password = request.forms.get('password')
        password2 = request.forms.get('password2')
        url = request.forms.get('url')
        retry_data = {"name": entry_name, "username": username, "url": url}
        log.debug("Entry Name: {}".format(entry_name))
        log.debug("Username: {}".format(username))
        log.debug("Password: {}".format(password))
        log.debug("Password 2: {}".format(password2))
        log.debug("URL: {}".format(url))

        if not entry_name:
            return template(template_name, retry="no_name", data=retry_data, path=path)
        if password != password2:
            return template(template_name, retry="mismatch", data=retry_data, path=path)
        updated_entry = pw_store.Entry(username=username, password=password, url=url)
        try:
            shared_cfg.update_entry(path, entry_name, updated_entry)
        except pw_store.ECDuplicateException:
            log.debug("Duplicate entry name {0}".format(entry_name))
            retry_reason = "duplicate"
        except pw_store.ECNaughtyCharacterException:
            log.debug("Bad character in entry name {0}".format(entry_name))
            retry_reason = "bad_char"
        except pw_store.ECException:
            log.debug("Exception while updating entry {0}".format(entry_name))
            retry_reason = "other_error"
        finally:
            if retry_reason:
                return template(template_name, retry=retry_reason, data=retry_data, path=path)

        cont_path, _ = os.path.split(path)
        return redirect("/manage{0}".format(cont_path))
    return redirect("/")
