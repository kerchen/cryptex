import illegal_chars
from bottle import (post, redirect, request, route, template)
import logging
import os

from credential import Credential
from ec_exceptions import ECException, ECDuplicateException, ECNaughtyCharacterException
from node import Node
import shared_cfg

log = logging.getLogger(__name__)


MANAGE_PASSWORDS_TEMPLATE = "manage-store.html"
CREATE_FOLDER_TEMPLATE = "create-folder.html"
EDIT_FOLDER_TEMPLATE = "edit-folder.html"
MOVE_FOLDER_TEMPLATE = "move-folder.html"
CREATE_ENTRY_TEMPLATE = "create-entry.html"
EDIT_ENTRY_TEMPLATE = "edit-entry.html"
MOVE_ENTRY_TEMPLATE = "move-entry.html"


@route('/manage<path:re:/.*>')
def manage_path(path):
    # Redirect any manage URLs that start with a forward slash so that
    # the user doesn't get a 404.
    if shared_cfg.validate_session(request):
        return redirect("/manage")
    return redirect("/")


@route('/manage')
def manage_path():
    if shared_cfg.validate_session(request):
        return template(MANAGE_PASSWORDS_TEMPLATE, status_msg=None)

    return redirect("/")


@post('/manage-command')
def handle_manage_command_post():
    log.debug("Handling management command post")
    if shared_cfg.validate_session(request):
        if request.forms.get('action') == 'show-manage':
            return redirect("/manage")
        elif request.forms.get('action') == 'create-entry':
            log.debug("Create entry button pressed")
            parent_path = request.forms.get('parent_path')
            data = dict()
            data['parent_path'] = parent_path
            return template(CREATE_ENTRY_TEMPLATE,
                            status_msg=None,
                            data=data)
        elif request.forms.get('action') == 'edit-entry':
            log.debug("Edit entry button pressed")
            entry_path = request.forms.get('entry_path')
            parent_path, _ = os.path.split(entry_path)
            entry_name, entry = shared_cfg.get_entry_by_path(entry_path)
            data = dict()
            data['parent_path'] = parent_path
            data['current_entry_name'] = entry_name
            data['entry_name'] = entry_name
            data['username'] = entry.get_username()
            data['password1'] = entry.get_password()
            data['password2'] = entry.get_password()
            data['url'] = entry.get_url()

            return template(EDIT_ENTRY_TEMPLATE,
                            status_msg=None,
                            data=data)
        elif request.forms.get('action') == 'move-entry':
            log.debug("Move entry button pressed. path = "
                      "{}".format(request.forms.get('entry_path')))
            entry_path = request.forms.get('entry_path')
            parent_path, _ = os.path.split(entry_path)
            return template(MOVE_ENTRY_TEMPLATE,
                            item_path=entry_path,
                            destination_path='/',
                            status_msg=None)
        elif request.forms.get('action') == 'create-folder':
            parent_path = request.forms.get('parent_path')
            log.debug("Create folder button pressed. path = "
                      "{}".format(parent_path))
            return template(CREATE_FOLDER_TEMPLATE,
                            parent_path=parent_path,
                            status_msg=None)
        elif request.forms.get('action') == 'move-folder':
            log.debug("Move folder button pressed. path = "
                      "{}".format(request.forms.get('folder_path')))
            folder_path = request.forms.get('folder_path')
            parent_path, _ = os.path.split(folder_path)
            return template(MOVE_FOLDER_TEMPLATE,
                            item_path=folder_path,
                            destination_path='/',
                            status_msg=None)
        elif request.forms.get('action') == 'edit-folder':
            log.debug("Edit folder button pressed")
            folder_path = request.forms.get('folder_path')
            parent_path, folder_name = os.path.split(folder_path)
            data = dict()
            data['parent_path'] = parent_path
            data['current_folder_name'] = folder_name
            data['new_folder_name'] = folder_name

            return template(EDIT_FOLDER_TEMPLATE,
                            status_msg=None,
                            data=data)
    return redirect("/")


def process_new_entry_input(template_name):
    log.debug("Checking new Entry input data.")
    parent_path = request.forms.get('parent_path')
    ent_name = request.forms.get('entry_name').strip()
    username = request.forms.get('username').strip()
    password1 = request.forms.get('password1')
    password2 = request.forms.get('password2')
    url = request.forms.get('url').strip()
    retry_data = {
        "parent_path": parent_path,
        "entry_name": ent_name,
        "username": username,
        "url": url}
    if not ent_name:
        return None, template(template_name,
                        status_msg="Entry name is required.",
                        data=retry_data)
    if password1 != password2:
        return None, template(template_name,
                        status_msg="Passwords do not match.",
                        data=retry_data)

    ent = Credential(username=username, password=password1, url=url)
    return (ent, retry_data), None


@post('/manage-create-entry')
def handle_create_entry_post():
    log.debug("Handling create entry post")
    status_msg = None
    if shared_cfg.validate_session(request):
        template_name = CREATE_ENTRY_TEMPLATE
        entry_data, retry_entry = process_new_entry_input(template_name)
        if not entry_data:
            return retry_entry

        new_entry = entry_data[0]
        retry_data = entry_data[1]
        try:
            shared_cfg.add_entry(new_entry,
                                 retry_data["entry_name"],
                                 retry_data["parent_path"])
        except ECDuplicateException:
            log.debug("Duplicate entry name {0}".format(retry_data["entry_name"]))
            status_msg = ("'{0}' is already the name of another entry in "
                          "the parent folder.".format(retry_data["entry_name"]))
        except ECNaughtyCharacterException:
            log.debug("Bad character in entry name {0}"
                      .format(retry_data["entry_name"]))
            status_msg = ("Entry names cannot contain any of these "
                          "characters: {0}"
                          .format(" ".join(illegal_chars.ILLEGAL_NAME_CHARS)))
        except ECException as ex:
            log.debug("Unexpected problem while adding entry "
                      "{0}".format(retry_data["entry_name"]))
            status_msg = "The entry could not be added. Reason: {0}".format(ex)
        finally:
            if status_msg:
                return template(template_name,
                                status_msg=status_msg,
                                data=retry_data)

        return redirect("/manage")
    return redirect("/")


@post('/manage-edit-entry')
def handle_edit_entry_post():
    log.debug("Handling edit entry post")
    if shared_cfg.validate_session(request):
        template_name = EDIT_ENTRY_TEMPLATE
        parent_path = request.forms.get('parent_path')
        current_entry_name = request.forms.get('current_entry_name')
        entry_name = request.forms.get('entry_name').strip()
        username = request.forms.get('username').strip()
        password1 = request.forms.get('password1')
        password2 = request.forms.get('password2')
        url = request.forms.get('url').strip()
        retry_data = {
            "parent_path": parent_path,
            "current_entry_name": current_entry_name,
            "entry_name": entry_name,
            "username": username,
            "password1": password1,
            "password2": password2,
            "url": url
        }

        status_msg = None
        if not entry_name:
            status_msg = "Entry name cannot be empty. Please try again."

        if password1 != password2:
            retry_data["password1"] = ""
            retry_data["password2"] = ""
            status_msg = "The entered passwords do not match. Please try again."

        if status_msg:
            return template(template_name,
                            status_msg=status_msg,
                            data=retry_data)

        updated_entry = Credential(username=username,
                                   password=password1,
                                   url=url)
        entry_path = parent_path + '/' + current_entry_name
        try:
            shared_cfg.update_entry(entry_path, entry_name, updated_entry)
        except ECDuplicateException:
            log.debug("Duplicate entry name {0}".format(entry_name))
            status_msg = ("'{0}' is already the name of another "
                          "entry in the current folder. Please try again."
                          .format(entry_name))
        except ECNaughtyCharacterException:
            log.debug("Bad character in entry name {0}".format(entry_name))
            status_msg = ("Entry names cannot contain these "
                          "characters: {0}. Please try again."
                          .format(" ".join(illegal_chars.ILLEGAL_NAME_CHARS)))
        except ECException as ex:
            log.debug("Unexpected problem while updating entry "
                      "{0}:{1}".format(current_entry_name, ex))
            status_msg = "The entry could not be updated. Reason: {0}".format(ex)
        finally:
            if status_msg:
                return template(template_name,
                                status_msg=status_msg,
                                data=retry_data)

        return redirect("/manage")
    return redirect("/")


@post('/manage-move-entry')
def handle_move_entry_post():
    log.debug("Handling move entry post")
    if shared_cfg.validate_session(request):
        item_path = request.forms.get('item_path')
        destination_path = request.forms.get('destination_path')
        status_msg = None
        try:
            shared_cfg.move_entry(item_path, destination_path)
        except ECDuplicateException:
            log.debug("Destination folder {0} already has an entry with the "
                      "same name as the entry being moved there "
                      "({1}).".format(destination_path, item_path))
            status_msg = ("The destination folder {0} already has an entry "
                          "with the same name as the one you're trying to "
                          "move there. You'll need to rename one of those "
                          "entries.".format(destination_path))
        except ECException as ex:
            log.debug("Unexpected problem while moving entry "
                      "{0}: {1}".format(item_path, ex))
            status_msg = ("An unexpected error occurred while trying to "
                          "move {0} to {1}. The entry was not moved."
                          .format(item_path, destination_path))
        finally:
            if status_msg:
                return template(MOVE_ENTRY_TEMPLATE,
                                item_path=item_path,
                                destination_path=destination_path,
                                status_msg=status_msg)

        return redirect("/manage")
    return redirect("/")


@post('/manage-delete-entry')
def handle_delete_entry_post():
    log.debug("Handling delete entry post")
    if shared_cfg.validate_session(request):
        entry_path = request.forms.get('entry_path')
        try:
            shared_cfg.remove_entry(entry_path)
        except ECException as ex:
            log.debug("Unexpected problem while deleting entry "
                      "{0}:{1}".format(entry_path, ex))
        return redirect("/manage")
    return redirect("/")


@post('/manage-create-folder')
def handle_create_folder_post():
    log.debug("Handling create folder post")
    if shared_cfg.validate_session(request):
        template_name = CREATE_FOLDER_TEMPLATE
        parent_path = request.forms.get('parent_path')
        folder_name = request.forms.get('name').strip()
        log.debug("Create folder post for name {}".format(folder_name))
        if not folder_name:
            return template(template_name,
                            parent_path=parent_path,
                            status_msg="Folder names cannot be empty. "
                                       "Please try again.")
        folder = Node()
        status_msg = None
        try:
            shared_cfg.add_container(folder, folder_name, parent_path)
        except ECDuplicateException:
            log.debug("Duplicate container name {0}".format(folder_name))
            status_msg = ("There is already a folder with the name {0} "
                          "in the parent folder. Please enter a different "
                          "name.".format(folder_name))
        except ECNaughtyCharacterException:
            log.debug("Bad character in container name {0}".format(folder_name))
            status_msg = ("Folder names cannot contain these "
                          "characters:{0}. Please enter a name "
                          "which does not use any of those characters."
                          .format(" ".join(illegal_chars.ILLEGAL_NAME_CHARS)))
        except ECException as ex:
            log.debug("Exception while adding container {0}".format(folder_name))
            status_msg = "The folder could not be added. Reason: {0}".format(ex)
        finally:
            if status_msg:
                return template(template_name,
                                parent_path=parent_path,
                                status_msg=status_msg)
        return redirect("/manage")
    return redirect("/")


@post('/manage-edit-folder')
def handle_edit_folder_post():
    log.debug("Handling edit folder post")
    if shared_cfg.validate_session(request):
        template_name = EDIT_FOLDER_TEMPLATE
        parent_path = request.forms.get('parent_path')
        current_folder_name = request.forms.get('current_folder_name')
        new_folder_name = request.forms.get('new_folder_name').strip()
        retry_data = {
            "parent_path": parent_path,
            "current_folder_name": current_folder_name,
            "new_folder_name": new_folder_name
        }

        if not new_folder_name:
            return template(template_name,
                            status_msg=("Folder names cannot be empty. Please "
                                        "try again."),
                            data=retry_data)
        container_path = parent_path + "/" + current_folder_name
        status_msg = None
        try:
            shared_cfg.rename_container(container_path, new_folder_name)
        except ECDuplicateException:
            log.debug("Duplicate folder name {0}".format(new_folder_name))
            status_msg = ("'{0}' is already the name of another "
                          "folder in the parent folder. Please try again."
                          .format(new_folder_name))
        except ECNaughtyCharacterException:
            log.debug("Bad character in folder name {0}".format(new_folder_name))
            status_msg = ("Folder names cannot contain any of these "
                          "characters: {0}. Please try again."
                          .format(" ".join(illegal_chars.ILLEGAL_NAME_CHARS)))
        except ECException as ex:
            log.debug("Unexpected problem while updating folder "
                      "{0}:{1}".format(current_folder_name, ex))
            status_msg = "The folder could not be updated. Reason: {0}".format(ex)
        finally:
            if status_msg:
                return template(template_name,
                                status_msg=status_msg,
                                data=retry_data)

        return redirect("/manage")
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
        except ECDuplicateException:
            log.debug("Destination folder {0} already has a folder with the "
                      "same name as the one being moved there "
                      "({1}).".format(destination_path, item_path))
            status_msg = ("The destination folder {0} already has a folder "
                          "with the same name as the one you're trying to "
                          "move there. You'll need to rename one of those "
                          "folders.".format(destination_path))
        except ECException as ex:
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

        return redirect("/manage")
    return redirect("/")


@post('/manage-delete-folder')
def handle_delete_folder_post():
    log.debug("Handling delete folder post")
    if shared_cfg.validate_session(request):
        folder_path = request.forms.get('folder_path')
        try:
            shared_cfg.remove_container(folder_path)
        except ECException as ex:
            log.debug("Unexpected problem while deleting folder "
                      "{0}:{1}".format(folder_path, ex))
        return redirect("/manage")
    return redirect("/")


