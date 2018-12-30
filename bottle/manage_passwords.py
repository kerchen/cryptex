from bottle import (post, redirect, request, route, template)
import logging

from path_util import decode_path, encode_path
import pw_store
import shared_cfg

log = logging.getLogger(__name__)


MANAGE_PASSWORDS_TEMPLATE = "manage-store.html"
NEW_CONTAINER_TEMPLATE = "create-folder.html"
CREATE_ENTRY_TEMPLATE = "create-entry.html"


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
            return template(CREATE_ENTRY_TEMPLATE,
                            path=shared_cfg.session.path,
                            status_msg=None,
                            data=None)
        elif request.forms.get('action') == 'showsessionpath':
            return manage_path(encode_path(shared_cfg.session.path))
        elif request.forms.get('action') == 'addcontainer':
            log.debug("Add container button pressed. path = "
                      "{}".format(shared_cfg.session.path))
            return template(NEW_CONTAINER_TEMPLATE,
                            path=shared_cfg.session.path,
                            status_msg=None)
    return redirect("/")


def process_entry_input(template_name):
    ent_name = request.forms.get('entryname').strip()
    username = request.forms.get('username').strip()
    password1 = request.forms.get('password1')
    password2 = request.forms.get('password2')
    url = request.forms.get('url').strip()
    retry_data = {"entryname": ent_name, "username": username, "url": url}
    log.debug("New entry confirmed")
    log.debug("Entry Name: {}".format(ent_name))
    log.debug("Username: {}".format(username))
    log.debug("Password 1: {}".format(password1))
    log.debug("Password 2: {}".format(password2))
    log.debug("URL: {}".format(url))
    if not ent_name:
        return None, template(template_name,
                        path=shared_cfg.session.path,
                        status_msg="Entry name is required.",
                        data=retry_data)
    if password1 != password2:
        return None, template(template_name,
                        path=shared_cfg.session.path,
                        status_msg="Passwords do not match.",
                        data=retry_data)

    ent = pw_store.Entry(username=username, password=password1, url=url)
    return (ent, ent_name), None


@post('/manage-new-entry')
def handle_new_entry_post():
    log.debug("Handling new entry post")
    status_msg = None
    if shared_cfg.validate_session(request):
        template_name = CREATE_ENTRY_TEMPLATE
        entry, retry_entry = process_entry_input(template_name)
        if not entry:
            return retry_entry

        retry_data = {"entryname": entry[1],
                      "username": entry[0].get_username(),
                      "url": entry[0].get_url()}
        try:
            shared_cfg.add_entry(entry[0], entry[1])
        except pw_store.ECDuplicateException:
            log.debug("Duplicate entry name {0}".format(entry[1]))
            status_msg = ("'{0}' is already in use by another "
                          "entry.".format(entry[1]))
        except pw_store.ECNaughtyCharacterException:
            log.debug("Bad character in entry name {0}".format(entry[1]))
            status_msg = ("Entry names can only contain spaces and these "
                          "characters: "
                          "{0}".format(" ".join(shared_cfg.LEGAL_NAME_CHARS)))
        except pw_store.ECException as ex:
            log.debug("Unexpected problem while adding entry "
                      "{0}".format(entry[1]))
            status_msg = "The entry could not be added. Reason: {0}".format(ex)
        finally:
            if status_msg:
                return template(template_name,
                                path=shared_cfg.session.path,
                                status_msg=status_msg,
                                data=retry_data)

        return redirect("/manage"+encode_path(shared_cfg.session.path))
    return redirect("/")


@post('/manage-update-entry')
def handle_update_entry_post():
    log.debug("Handling update entry post")
    status_msg = None
    if shared_cfg.validate_session(request):
        print("nah")
    return redirect("/")


@post('/manage-new-container')
def handle_new_container_post():
    log.debug("Handling new container post")
    if shared_cfg.validate_session(request):
        template_name = NEW_CONTAINER_TEMPLATE
        cont_name = request.forms.get('name').strip()
        log.debug("New container post for name {}".format(cont_name))
        if not cont_name:
            return template(template_name,
                            path=shared_cfg.session.path,
                            status_msg="Folder names cannot be empty. "
                                       "Please try again.")
        cont = pw_store.EntryContainer()
        status_msg = None
        try:
            shared_cfg.add_container(cont, cont_name)
        except pw_store.ECDuplicateException:
            log.debug("Duplicate container name {0}".format(cont_name))
            status_msg = ("There is already a folder with the name {0} "
                          "in the current folder. Please enter a different "
                          "name.".format(cont_name))
        except pw_store.ECNaughtyCharacterException:
            log.debug("Bad character in container name {0}".format(cont_name))
            status_msg = ("Folder names can only contain spaces and these "
                          "characters:{0}. Please enter a name "
                          "containing only those characters."
                          .format(" ".join(shared_cfg.LEGAL_NAME_CHARS)))
        except pw_store.ECException as ex:
            log.debug("Exception while adding container {0}".format(cont_name))
            status_msg = "The folder could not be added. Reason: {0}".format(ex)
        finally:
            if status_msg:
                return template(template_name,
                                path=shared_cfg.session.path,
                                status_msg=status_msg)
        return redirect("/manage{0}+{1}".format(
            encode_path(shared_cfg.session.path),
            cont_name))
    return redirect("/")
