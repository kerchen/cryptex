import logging
import os
import xml.etree.cElementTree as ET

import encryption


log = logging.getLogger(__name__)


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
