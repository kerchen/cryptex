import logging
import os
import xml.etree.cElementTree as ET

import encryption


log = logging.getLogger(__name__)


class ECException(Exception):
    pass


class ECDuplicateException(ECException):
    pass


class ECNotFoundException(ECException):
    pass


class EntryContainer():
    def __init__(self, name):
        self.name = name
        self.containers = dict()
        self.entries = dict()

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_container_count(self):
        return len(self.containers)

    def get_entry_count(self):
        return len(self.entries)

    def clear(self):
        self.containers.clear()
        self.entries.clear()

    def add_container(self, cont):
        if cont.get_name() in self.containers:
            raise ECDuplicateException("Duplicate container name")
        self.containers[cont.get_name()] = cont

    def rename_container(self, old_name, new_name):
        if old_name not in self.containers:
            raise ECNotFoundException("Container with name '{0}' not found".format(old_name))
        if new_name in self.containers:
            raise ECDuplicateException("Container with name '{0}' already present".format(new_name))
        cont = self.containers.pop(old_name)
        cont.set_name(new_name)
        #try:
            #self.add_container(cont)
        #except ECDuplicateException as ex:

    def remove_container(self, name):
        if name not in self.containers:
            raise ECNotFoundException("Container with name '{}' not found".format(name))
        self.containers.pop(name)

    def add_entry(self, entry):
        if entry.get_name() in self.entries:
            raise ECException("Duplicate entry name")
        self.entries[entry.get_name()] = entry


class Entry():
    def __init__(self, name, username, password, url):
        self.name = name
        self.username = username
        self.password = password
        self.url = url

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url


class PasswordStore():
    def __init__(self, serialized_data):
        self.root = EntryContainer(name=None)


def open_pw_store(password, pw_store_filename):
    if os.path.exists(pw_store_filename):
        pw_store_xml = encryption.decrypt_to_string(password, pw_store_filename)
        try:
            pw_store = ET.fromstring(pw_store_xml)
        except Exception:
            pw_store = None
    else:
        log.debug("Creating new password store")
        pw_store = ET.Element("cryptex_pw_store")
        ET.SubElement(pw_store, "passwords")

        save_pw_store(pw_store, password, pw_store_filename)

    return pw_store


def save_pw_store(pw_store, password, pw_store_filename):
    pw_store_xml = ET.tostring(pw_store, encoding='utf8', method='xml')
    log.debug("Dump of pw store xml:")
    log.debug(pw_store_xml)
    encryption.encrypt_from_string(password, pw_store_xml, pw_store_filename)
