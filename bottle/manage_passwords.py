from bottle import (post, redirect, request, route, template)
import logging

from path_util import decode_path, encode_path
import pw_store
import shared_cfg

log = logging.getLogger(__name__)


MANAGE_PASSWORDS_TEMPLATE = "manage-store.html"
NEW_CONTAINER_TEMPLATE = "create-folder.html"
EDIT_FOLDER_TEMPLATE = "edit-folder.html"
MOVE_FOLDER_TEMPLATE = "move-folder.html"
DELETE_FOLDER_TEMPLATE = "delete-folder.html"
CREATE_ENTRY_TEMPLATE = "create-entry.html"
EDIT_ENTRY_TEMPLATE = "edit-entry.html"
DELETE_ENTRY_TEMPLATE = "delete-entry.html"


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


@post('/manage-command')
def handle_manage_command_post():
    log.debug("Handling management command post")
    if shared_cfg.validate_session(request):
        if request.forms.get('action') == 'create-entry':
            log.debug("Create entry button pressed")
            return template(CREATE_ENTRY_TEMPLATE,
                            path=shared_cfg.session.path,
                            status_msg=None,
                            data=None)
        elif request.forms.get('action') == 'edit-entry':
            log.debug("Edit entry button pressed")
            entry_path = decode_path(request.forms.get('encoded_path'))
            entry_name, entry = shared_cfg.get_entry_by_path(entry_path)
            data = dict()
            data['current_entry_name'] = entry_name
            data['entryname'] = entry_name
            data['username'] = entry.get_username()
            data['password1'] = entry.get_password()
            data['password2'] = entry.get_password()
            data['url'] = entry.get_url()

            return template(EDIT_ENTRY_TEMPLATE,
                            path=shared_cfg.session.path,
                            status_msg=None,
                            data=data)
        elif request.forms.get('action') == 'delete-entry':
            log.debug("Delete entry button pressed")
            return template(DELETE_ENTRY_TEMPLATE,
                            path=decode_path(
                                request.forms.get('encoded_path')))
        elif request.forms.get('action') == 'show-session-path':
            return manage_path(encode_path(shared_cfg.session.path))
        elif request.forms.get('action') == 'create-folder':
            log.debug("Create folder button pressed. path = "
                      "{}".format(shared_cfg.session.path))
            return template(NEW_CONTAINER_TEMPLATE,
                            path=shared_cfg.session.path,
                            status_msg=None)
        elif request.forms.get('action') == 'move-folder':
            log.debug("Move folder button pressed. path = "
                      "{}".format(request.forms.get('encoded_path')))
            return template(MOVE_FOLDER_TEMPLATE,
                            item_path=decode_path(
                                request.forms.get('encoded_path')),
                            destination_path='/',
                            status_msg=None)
        elif request.forms.get('action') == 'edit-folder':
            log.debug("Edit folder button pressed")
            folder_path = decode_path(request.forms.get('encoded_path'))
            folder_name = shared_cfg.get_container_name_from_path(folder_path)
            data = dict()
            data['current_folder_name'] = folder_name
            data['new_folder_name'] = folder_name

            return template(EDIT_FOLDER_TEMPLATE,
                            path=shared_cfg.session.path,
                            status_msg=None,
                            data=data)
        elif request.forms.get('action') == 'delete-folder':
            log.debug("Delete folder button pressed")
            return template(DELETE_FOLDER_TEMPLATE,
                            path=decode_path(
                                request.forms.get('encoded_path')))
    return redirect("/")


def process_new_entry_input(template_name):
    log.debug("Checking new Entry input data.")
    ent_name = request.forms.get('entryname').strip()
    username = request.forms.get('username').strip()
    password1 = request.forms.get('password1')
    password2 = request.forms.get('password2')
    url = request.forms.get('url').strip()
    retry_data = {"entryname": ent_name, "username": username, "url": url}
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


@post('/manage-create-entry')
def handle_create_entry_post():
    log.debug("Handling create entry post")
    status_msg = None
    if shared_cfg.validate_session(request):
        template_name = CREATE_ENTRY_TEMPLATE
        entry, retry_entry = process_new_entry_input(template_name)
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


@post('/manage-edit-entry')
def handle_edit_entry_post():
    log.debug("Handling edit entry post")
    status_msg = None
    if shared_cfg.validate_session(request):
        template_name = EDIT_ENTRY_TEMPLATE
        current_entry_name = request.forms.get('current_entry_name')
        entry_name = request.forms.get('entryname').strip()
        username = request.forms.get('username').strip()
        password1 = request.forms.get('password1')
        password2 = request.forms.get('password2')
        url = request.forms.get('url').strip()
        retry_data = {
            "current_entry_name": current_entry_name,
            "entryname": entry_name,
            "username": username,
            "password1": password1,
            "password2": password2,
            "url": url
        }

        if not entry_name:
            return template(template_name,
                            path=shared_cfg.session.path,
                            status_msg=("Entry name cannot be empty. Please "
                                        "try again."),
                            data=retry_data)

        if password1 != password2:
            retry_data["password1"] = ""
            retry_data["password2"] = ""
            return template(template_name,
                            path=shared_cfg.session.path,
                            status_msg=("The entered passwords do not match. "
                                        "Please try again"),
                            data=retry_data)

        updated_entry = pw_store.Entry(username=username,
                                       password=password1,
                                       url=url)
        entry_path = shared_cfg.session.path + '/' + current_entry_name
        try:
            shared_cfg.update_entry(entry_path, entry_name, updated_entry)
        except pw_store.ECDuplicateException:
            log.debug("Duplicate entry name {0}".format(entry_name))
            status_msg = ("'{0}' is already the name of another "
                          "entry in the current folder. Please try again."
                          .format(entry_name))
        except pw_store.ECNaughtyCharacterException:
            log.debug("Bad character in entry name {0}".format(entry_name))
            status_msg = ("Entry names can only contain spaces and these "
                          "characters: "
                          "{0}. Please try again."
                          .format(" ".join(shared_cfg.LEGAL_NAME_CHARS)))
        except pw_store.ECException as ex:
            log.debug("Unexpected problem while updating entry "
                      "{0}:{1}".format(current_entry_name, ex))
            status_msg = "The entry could not be updated. Reason: {0}".format(ex)
        finally:
            if status_msg:
                return template(template_name,
                                path=shared_cfg.session.path,
                                status_msg=status_msg,
                                data=retry_data)

        return redirect("/manage"+encode_path(shared_cfg.session.path))
    return redirect("/")


@post('/manage-delete-entry')
def handle_delete_entry_post():
    log.debug("Handling delete entry post")
    if shared_cfg.validate_session(request):
        entry_path = request.forms.get('entry_path')
        try:
            shared_cfg.remove_entry(entry_path)
        except pw_store.ECException as ex:
            log.debug("Unexpected problem while deleting entry "
                      "{0}:{1}".format(entry_path, ex))
        return redirect("/manage"+encode_path(shared_cfg.session.path))
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


@post('/manage-edit-folder')
def handle_edit_folder_post():
    log.debug("Handling edit folder post")
    status_msg = None
    if shared_cfg.validate_session(request):
        template_name = EDIT_FOLDER_TEMPLATE
        current_folder_name = request.forms.get('current_folder_name')
        new_folder_name = request.forms.get('new_folder_name').strip()
        retry_data = {
            "current_folder_name": current_folder_name,
            "new_folder_name": new_folder_name
        }

        if not new_folder_name:
            return template(template_name,
                            path=shared_cfg.session.path,
                            status_msg=("Folder names cannot be empty. Please "
                                        "try again."),
                            data=retry_data)
        container_path = shared_cfg.session.path + "/" + current_folder_name
        try:
            shared_cfg.rename_container(container_path, new_folder_name)
        except pw_store.ECDuplicateException:
            log.debug("Duplicate folder name {0}".format(new_folder_name))
            status_msg = ("'{0}' is already the name of another "
                          "folder in the current folder. Please try again."
                          .format(new_folder_name))
        except pw_store.ECNaughtyCharacterException:
            log.debug("Bad character in folder name {0}".format(new_folder_name))
            status_msg = ("Folder names can only contain spaces and these "
                          "characters: "
                          "{0}. Please try again."
                          .format(" ".join(shared_cfg.LEGAL_NAME_CHARS)))
        except pw_store.ECException as ex:
            log.debug("Unexpected problem while updating folder "
                      "{0}:{1}".format(current_folder_name, ex))
            status_msg = "The folder could not be updated. Reason: {0}".format(ex)
        finally:
            if status_msg:
                return template(template_name,
                                path=shared_cfg.session.path,
                                status_msg=status_msg,
                                data=retry_data)

        return redirect("/manage"+encode_path(shared_cfg.session.path))
    return redirect("/")


@post('/manage-move-folder')
def handle_move_folder_post():
    log.debug("Handling move folder post")
    if shared_cfg.validate_session(request):
        item_path = request.forms.get('item_path')
        destination_path = request.forms.get('destination_path')
        status_msg = None
        try:
            shared_cfg.move_container(item_path, destination_path)
        except pw_store.ECDuplicateException:
            log.debug("Destination folder {0} already has a folder with the "
                      "same name as the one being moved there "
                      "({1}).".format(destination_path, item_path))
            status_msg = ("The destination folder {0} already has a folder "
                          "with the same name as the one you're trying to "
                          "move there. You'll need to rename one of those "
                          "folders.".format(destination_path))
        except pw_store.ECException as ex:
            log.debug("Unexpected problem while moving folder "
                      "{0}: {1}".format(item_path, ex))
            status_msg = ("An unexpected error occurred while trying to "
                          "move {0} to {1}. The folder was not moved."
                          .format(item_path, destination_path))
        finally:
            if status_msg:
                return template(MOVE_FOLDER_TEMPLATE,
                                item_path=item_path,
                                destination_path=destination_path,
                                status_msg=status_msg)

        return redirect("/manage"+encode_path(shared_cfg.session.path))
    return redirect("/")


@post('/manage-delete-folder')
def handle_delete_folder_post():
    log.debug("Handling delete folder post")
    if shared_cfg.validate_session(request):
        folder_path = request.forms.get('folder_path')
        try:
            shared_cfg.remove_container(folder_path)
        except pw_store.ECException as ex:
            log.debug("Unexpected problem while deleting folder "
                      "{0}:{1}".format(folder_path, ex))
        return redirect("/manage"+encode_path(shared_cfg.session.path))
    return redirect("/")


