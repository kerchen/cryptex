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
    def __init__(self):
        self.containers = dict()
        self.entries = dict()

    def get_container(self, cont_name):
        if cont_name not in self.containers:
            raise ECNotFoundException(
                "Container with name '{0}' not found".format(cont_name))
        return self.containers[cont_name]

    def get_container_count(self):
        return len(self.containers)

    def get_containers(self):
        return frozenset(self.containers.items())

    def get_entry(self, entry_name):
        if entry_name not in self.entries:
            raise ECNotFoundException(
                "Entry with name '{0}' not found".format(entry_name))
        return self.entries[entry_name]

    def get_entry_count(self):
        return len(self.entries)

    def get_entries(self):
        return frozenset(self.entries.items())

    def clear(self):
        self.containers.clear()
        self.entries.clear()

    def add_container(self, cont, name):
        if name in self.containers:
            raise ECDuplicateException("Duplicate container name {0}".format(name))
        self.containers[name] = cont

    def rename_container(self, old_name, new_name):
        if old_name not in self.containers:
            raise ECNotFoundException(
                "Container with name '{0}' not found".format(old_name))
        if new_name in self.containers:
            raise ECDuplicateException(
                "Container with name '{0}' already present".format(new_name))
        cont = self.containers.pop(old_name)
        self.add_container(cont, new_name)

    def remove_container(self, name):
        if name not in self.containers:
            raise ECNotFoundException(
                "Container with name '{}' not found".format(name))
        self.containers.pop(name)

    def add_entry(self, entry, name):
        if name in self.entries:
            raise ECDuplicateException(
                "Entry with name {0} already exists".format(name))
        self.entries[name] = entry

    def rename_entry(self, old_name, new_name):
        if old_name not in self.entries:
            raise ECNotFoundException(
                "Entry with name '{0}' not found".format(old_name))
        if new_name in self.entries:
            raise ECDuplicateException(
                "Entry with name '{0}' already present".format(new_name))
        entry = self.entries.pop(old_name)
        self.add_entry(entry, new_name)

    def remove_entry(self, name):
        if name not in self.entries:
            raise ECNotFoundException(
                "Entry with name '{}' not found".format(name))
        self.entries.pop(name)


class Entry():
    def __init__(self,  username=None, password=None, url=None):
        self.username = username
        self.password = password
        self.url = url

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


ROOT_TAG="cryptex"
STORE_ROOT_TAG="store"
NAME_ATTRIBUTE="name"
CONTAINER_TAG="container"
ENTRY_TAG="entry"
USERNAME_TAG="username"
PASSWORD_TAG="password"
URL_TAG="url"


def add_children(xml_node):
    new_cont = EntryContainer()
    if NAME_ATTRIBUTE in xml_node.attrib:
        cont_name = xml_node.attrib[NAME_ATTRIBUTE]
    else:
        cont_name = None

    for el in list(xml_node):
        if el.tag == CONTAINER_TAG:
            n, c = add_children(el)
            new_cont.add_container(c, n)
        elif el.tag == ENTRY_TAG:
            new_entry = Entry()
            for en in el.iter():
                if en.tag == USERNAME_TAG:
                    new_entry.set_username(en.text)
                elif en.tag == PASSWORD_TAG:
                    new_entry.set_password(en.text)
                elif en.tag == URL_TAG:
                    new_entry.set_url(en.text)
            new_cont.add_entry(new_entry, el.attrib[NAME_ATTRIBUTE])

    return cont_name, new_cont


class PasswordStore():
    def __init__(self, serialized_data):
        # Parse serialized (XML) store data
        xml_root = ET.fromstring(serialized_data)
        store_root = xml_root.find(STORE_ROOT_TAG)
        self.root = add_children(store_root)

    def get_root(self):
        '''Returns the EntryContainer that is the root of the store.'''
        return self.root


def open_pw_store(password, pw_store_filename):
    if os.path.exists(pw_store_filename):
        pw_store_xml = encryption.decrypt_to_string(password, pw_store_filename)
        try:
            pw_store = ET.fromstring(pw_store_xml)
        except Exception:
            pw_store = None
    else:
        log.debug("Creating new password store")
        pw_store = ET.Element(ROOT_TAG)
        ET.SubElement(pw_store, STORE_ROOT_TAG)

        save_pw_store(pw_store, password, pw_store_filename)

    return pw_store


def save_pw_store(pw_store, password, pw_store_filename):
    pw_store_xml = ET.tostring(pw_store, encoding='utf8', method='xml')
    log.debug("Dump of pw store xml:")
    log.debug(pw_store_xml)
    encryption.encrypt_from_string(password, pw_store_xml, pw_store_filename)
