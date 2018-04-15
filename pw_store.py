from base64 import b64decode, b64encode
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


class EntryContainer:
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
            raise ECDuplicateException(
                "Duplicate container name {0}".format(name))
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


class Entry:
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


ROOT_TAG = "cryptex"
STORE_ROOT_TAG = "store"
NAME_ATTRIBUTE = "name"
CONTAINER_TAG = "container"
ENTRY_TAG = "entry"
USERNAME_TAG = "username"
PASSWORD_TAG = "password"
URL_TAG = "url"


def deserialize_xml(xml_node=None):
    """Given an XML node which represents the root of a container, creates
    an EntryContainer object and adds the entries and containers that are
    children of the node.
    :returns a tuple of the container name and object"""
    cont = EntryContainer()
    cont_name = None
    
    if not xml_node:
        return cont_name, cont

    if NAME_ATTRIBUTE in xml_node.attrib:
        cont_name = b64decode(xml_node.attrib[NAME_ATTRIBUTE])

    for el in list(xml_node):
        if el.tag == CONTAINER_TAG:
            n, c = deserialize_xml(el)
            cont.add_container(c, n)
        elif el.tag == ENTRY_TAG:
            new_entry = Entry()
            for en in el.iter():
                if en.tag == USERNAME_TAG:
                    new_entry.set_username(b64decode(en.text))
                elif en.tag == PASSWORD_TAG:
                    new_entry.set_password(b64decode(en.text))
                elif en.tag == URL_TAG:
                    new_entry.set_url(b64decode(en.text))
            cont.add_entry(new_entry, b64decode(el.attrib[NAME_ATTRIBUTE]))

    return cont_name, cont


def serialize_xml(xml_root, cont_name, cont, cont_tag=CONTAINER_TAG):
    root_element = ET.SubElement(xml_root, cont_tag)
    if cont_name:
        root_element.set(NAME_ATTRIBUTE, b64encode(cont_name))

    for k, e in cont.get_entries():
        entry_el = ET.SubElement(root_element, ENTRY_TAG)
        entry_el.set(NAME_ATTRIBUTE, b64encode(k))
        username_el = ET.SubElement(entry_el, USERNAME_TAG)
        username_el.text = b64encode(e.get_username())
        password_el = ET.SubElement(entry_el, PASSWORD_TAG)
        password_el.text = b64encode(e.get_password())
        url_el = ET.SubElement(entry_el, URL_TAG)
        url_el.text = b64encode(e.get_url())

    for k, c in cont.get_containers():
        serialize_xml(root_element, k, c)


class PasswordStore:
    def __init__(self, serialized_data):
        # Parse serialized (XML) store data
        if serialized_data:
            xml_root = ET.fromstring(serialized_data)
            store_root = xml_root.find(STORE_ROOT_TAG)
            _, self.root = deserialize_xml(store_root)
        else:
            _, self.root = deserialize_xml()

    def get_root(self):
        """Returns the EntryContainer that is the root of the store."""
        return self.root

    def serialize_to_xml(self):
        xml_root = ET.Element(ROOT_TAG)
        serialize_xml(xml_root, None, self.root, STORE_ROOT_TAG)
        return ET.tostring(xml_root, encoding='utf8', method='xml')


def open_pw_store(password, pw_store_filename):
    if os.path.exists(pw_store_filename):
        pw_store_xml = encryption.decrypt_to_string(password, pw_store_filename)
        try:
            pw_store = PasswordStore(pw_store_xml)
        except Exception:
            pw_store = None
    else:
        log.debug("Creating new password store")
        pw_store = PasswordStore(None)

        save_pw_store(pw_store, password, pw_store_filename)

    return pw_store


def save_pw_store(pw_store, password, pw_store_filename):
    pw_store_xml = pw_store.serialize_to_xml()
    log.debug("Dump of pw store xml:")
    log.debug(pw_store_xml)
    encryption.encrypt_from_string(password, pw_store_xml, pw_store_filename)
