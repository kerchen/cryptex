from base64 import b64decode, b64encode
import logging
import os
import xml.etree.cElementTree as ET

import encryption
from credential import Credential
from ec_exceptions import ECException, ECNotFoundException
from node import Node
from path_util import simplify_path


log = logging.getLogger(__name__)

ROOT_TAG = u"cryptex"
STORE_ROOT_TAG = u"store"
NAME_ATTRIBUTE = u"name"
CONTAINER_TAG = u"container"
ENTRY_TAG = u"entry"
USERNAME_TAG = u"username"
PASSWORD_TAG = u"password"
URL_TAG = u"url"


def deserialize_xml(xml_node=None):
    """Given an XML node which represents the root of a container, creates
    an Node object and adds the entries and containers that are
    children of the node.
    :returns a tuple of the container name and object"""
    cont = Node()
    cont_name = None
    
    if xml_node is None:
        return cont_name, cont

    if NAME_ATTRIBUTE in xml_node.attrib:
        cont_name = b64decode(xml_node.attrib[NAME_ATTRIBUTE]).decode('utf-8')

    for el in list(xml_node):
        if el.tag == CONTAINER_TAG:
            n, c = deserialize_xml(el)
            cont.add_node(c, n)
        elif el.tag == ENTRY_TAG:
            new_entry = Credential()
            for en in el.iter():
                if en.tag == USERNAME_TAG:
                    new_entry.set_username(b64decode(en.text).decode('utf-8'))
                elif en.tag == PASSWORD_TAG:
                    new_entry.set_password(b64decode(en.text).decode('utf-8'))
                elif en.tag == URL_TAG:
                    new_entry.set_url(b64decode(en.text).decode('utf-8'))
            cont.add_credential(new_entry, b64decode(el.attrib[NAME_ATTRIBUTE]).decode('utf-8'))

    return cont_name, cont


def serialize_xml(xml_root, cont_name, cont, cont_tag=CONTAINER_TAG):
    """Given an XML root node, serializes to XML the Node 'cont' with
    the name 'cont_name'."""
    root_element = ET.SubElement(xml_root, cont_tag)
    if cont_name:
        root_element.set(NAME_ATTRIBUTE, b64encode(cont_name.encode()).decode('utf-8'))

    for k, e in cont.credentials:
        entry_el = ET.SubElement(root_element, ENTRY_TAG)
        entry_el.set(NAME_ATTRIBUTE, b64encode(k.encode()).decode('utf-8'))
        if e.get_username():
            username_el = ET.SubElement(entry_el, USERNAME_TAG)
            username_el.text = b64encode(e.get_username().encode()).decode('utf-8')
        if e.get_password():
            password_el = ET.SubElement(entry_el, PASSWORD_TAG)
            password_el.text = b64encode(e.get_password().encode()).decode('utf-8')
        if e.get_url():
            url_el = ET.SubElement(entry_el, URL_TAG)
            url_el.text = b64encode(e.get_url().encode()).decode('utf-8')

    for k, c in cont.nodes:
        serialize_xml(root_element, k, c)


class PasswordStore:
    def __init__(self, serialized_data):
        # Parse serialized (XML) store data
        if serialized_data:
            try:
                xml_root = ET.fromstring(serialized_data)
                store_root = xml_root.find(STORE_ROOT_TAG)
                _, self.root = deserialize_xml(store_root)
            except ET.ParseError as ex:
                raise ECException("Failed to open store: {0}".format(ex))
        else:
            _, self.root = deserialize_xml()

    def get_root(self):
        """Returns the Node that is the root of the store."""
        return self.root

    def is_empty(self):
        """Returns True if the store has no containers nor entries."""
        return self.root.get_node_count() == 0 and self.root.get_credential_count() == 0

    def is_valid_path(self, path):
        """Returns true if the given path is valid (i.e., is a path to a
        container or entry in the store)."""
        dest_cont = self.root
        cont_chain = list(filter(None, simplify_path(path).split("/")))
        cc_count = len(cont_chain)
        for c in cont_chain:
            cc_count -= 1
            try:
                if cc_count > 0:
                    dest_cont = dest_cont.get_node(c)
                else:
                    if not dest_cont.has_node(c):
                        if not dest_cont.has_credential(c):
                            return False
            except ECNotFoundException:
                return False
            except ECException as ex:
                log.warning("Unexpected exception: {0}".format(ex))
                return False
        return True

    def get_container_by_path(self, path):
        dest_cont = self.root
        cont_chain = simplify_path(path).split("/")
        for c in cont_chain:
            if len(c):
                dest_cont = dest_cont.get_node(c)
        return dest_cont

    def add_entry(self, entry, entry_name, path):
        if not entry:
            raise ECException("Invalid entry")
        if not entry_name or len(entry_name) == 0:
            raise ECException("Invalid entry name")
        dest_cont = self.get_container_by_path(simplify_path(path))
        dest_cont.add_credential(entry, entry_name)

    def update_entry(self, path, updated_name, updated_entry):
        if not updated_entry:
            raise ECException("Invalid entry")
        if not updated_name or len(updated_name) == 0:
            raise ECException("Invalid entry name")
        cont_path, current_name = os.path.split(path)
        cont = self.get_container_by_path(simplify_path(cont_path))
        if updated_name != current_name:
            cont.rename_credential(current_name, updated_name)
        cont.replace_credential(updated_entry, updated_name)

    def get_entry_by_path(self, path):
        cont_path, ent_name = os.path.split(simplify_path(path))
        cont = self.get_container_by_path(cont_path)
        return ent_name, cont.get_credential(ent_name)

    def get_entry_count_by_path(self, path):
        cont = self.get_container_by_path(simplify_path(path))
        return len(cont.credentials)

    def get_entries_by_path(self, path):
        cont = self.get_container_by_path(simplify_path(path))
        return cont.credentials

    def add_container(self, cont, cont_name, path):
        if not cont:
            raise ECException("Invalid container")
        if not cont_name or len(cont_name) == 0:
            raise ECException("Invalid container name")
        dest_cont = self.get_container_by_path(simplify_path(path))
        dest_cont.add_node(cont, cont_name)

    def get_container_count_by_path(self, path):
        cont = self.get_container_by_path(simplify_path(path))
        return len(cont.nodes)

    def get_containers_by_path(self, path):
        cont = self.get_container_by_path(simplify_path(path))
        return cont.nodes

    def serialize_to_xml(self):
        xml_root = ET.Element(ROOT_TAG)
        serialize_xml(xml_root, None, self.root, STORE_ROOT_TAG)
        xml_str = ET.tostring(xml_root, encoding='utf-8', method='xml')
        return xml_str

    def save(self, password, filename):
        pw_store_xml = self.serialize_to_xml()
        encryption.encrypt_from_string(password, pw_store_xml, filename)


def open_pw_store(password, pw_store_filename):
    if os.path.exists(pw_store_filename):
        pw_store_xml = encryption.decrypt_to_string(password, pw_store_filename)
        try:
            store = PasswordStore(pw_store_xml)
        except ECException as ex:
            log.error("Failed to open password store: {0}".format(ex))
            store = None
    else:
        log.debug("Creating new password store")
        store = PasswordStore(None)

        store.save(password, pw_store_filename)

    return store


