from bottle import (post, redirect, request, route, template)
import logging

from path_util import decode_path
import pw_store
import shared_cfg

log = logging.getLogger(__name__)


MANAGE_PASSWORDS_TEMPLATE = "manage-store.html"
NEW_CONTAINER_TEMPLATE = "new_container.tpl"
NEW_ENTRY_TEMPLATE = "new_entry.tpl"


@route('/manage<path:re:/.*>')
def manage_path(path):
    # Redirect any manage URLs that start with a forward slash so that
    # the user doesn't get a 404.
    if shared_cfg.validate_session(request):
        return redirect("/manage")
    return redirect("/")


@route('/manage<path:re:\+.*>')
def manage_path(path):
    if shared_cfg.validate_session(request):
        # If this function is invoked with any forward slashes, redirect to
        # the root of the store. If we don't do this, the resource URIs in the
        # generated web page (which have relative paths) will fail. Internally,
        # we always prefix paths with '+' and use '+' for path separators,
        # so this should only happen if the user tries to go directly to
        # an entry or container by typing its path directly in the browser.
        if path.find('/') > -1:
            return redirect("/manage")

        path = decode_path(path)
        log.debug("Routing to path {0}".format(path))
        if shared_cfg.change_session_path(path):
            return template(MANAGE_PASSWORDS_TEMPLATE,
                            path=shared_cfg.session.path,
                            status_msg=None)
        else:
            return redirect("/manage")

    return redirect("/")


@post('/manage')
def handle_manage_post():
    log.debug("Handling management post")
    if shared_cfg.validate_session(request):
        if request.forms.get('action') == 'addentry':
            log.debug("Add entry button pressed")
            return template(NEW_ENTRY_TEMPLATE, retry="")
        elif request.forms.get('action') == 'addcontainer':
            log.debug("Add container button pressed. path = "
                      "{}".format(shared_cfg.session.path))
            return template(NEW_CONTAINER_TEMPLATE, retry="")
        #elif request.forms.get("renamecontainer"):
            #log.debug("Rename container button pressed. path = "
                      #"{}".format(shared_cfg.session.path))
            #return template(RENAME_CONTAINER_TEMPLATE, retry="")
        #elif request.forms.get("removecontainer"):
            #log.debug("Remove container button pressed. path = "
                      #"{}".format(shared_cfg.session.path))
            #return template(REMOVE_CONTAINER_TEMPLATE, retry="")
    return redirect("/")


@post('/manage-new-entry')
def handle_new_entry_post():
    log.debug("Handling new entry post")
    if shared_cfg.validate_session(request):
        if request.forms.get("create"):
            templ_name = NEW_ENTRY_TEMPLATE
            retry_reason = None
            ent_name = request.forms.get('name').strip()
            username = request.forms.get('username').strip()
            password = request.forms.get('password')
            password2 = request.forms.get('password2')
            url = request.forms.get('url').strip()
            retry_data = {"name": ent_name, "username": username, "url": url}
            log.debug("New entry confirmed")
            log.debug("Entry Name: {}".format(ent_name))
            log.debug("Username: {}".format(username))
            log.debug("Password: {}".format(password))
            log.debug("Password 2: {}".format(password2))
            log.debug("URL: {}".format(url))
            if not ent_name:
                return template(templ_name, retry="no_name", data=retry_data)
            if password != password2:
                return template(templ_name, retry="mismatch", data=retry_data)
            ent = pw_store.Entry(username=username, password=password, url=url)
            try:
                shared_cfg.add_entry(ent, ent_name)
            except pw_store.ECDuplicateException:
                log.debug("Duplicate entry name {0}".format(ent_name))
                retry_reason = "duplicate"
            except pw_store.ECNaughtyCharacterException:
                log.debug("Bad character in entry name {0}".format(ent_name))
                retry_reason = "bad_char"
            except pw_store.ECException:
                log.debug("Exception while adding entry {0}".format(ent_name))
                retry_reason = "other_error"
            finally:
                if retry_reason:
                    return template(templ_name, retry=retry_reason, data=retry_data)

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
            templ_name = NEW_CONTAINER_TEMPLATE
            retry_reason = None
            cont_name = request.forms.get('name').strip()
            log.debug("New container confirmed")
            log.debug("Name: {}".format(cont_name))
            if not cont_name:
                return template(templ_name, retry="no_name",
                                data={"name": cont_name})
            cont = pw_store.EntryContainer()
            try:
                shared_cfg.add_container(cont, cont_name)
            except pw_store.ECDuplicateException:
                log.debug("Duplicate container name {0}".format(cont_name))
                retry_reason = "duplicate"
            except pw_store.ECNaughtyCharacterException:
                log.debug("Bad character in container name {0}".format(cont_name))
                retry_reason = "bad_char"
            except pw_store.ECException:
                log.debug("Exception while adding container {0}".format(cont_name))
                retry_reason = "other_error"
            finally:
                if retry_reason:
                    return template(templ_name, retry=retry_reason,
                                    data={"name": cont_name})
            return redirect("/manage"+shared_cfg.session.path+"/"+cont_name)
        elif request.forms.get("cancel"):
            log.debug("New container cancelled")
            return redirect("/manage"+shared_cfg.session.path)
    return redirect("/")
