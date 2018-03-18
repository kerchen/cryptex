import hashlib
import os
import xml.etree.cElementTree as ET

import encryption


def open_pw_store(password, pw_store_filename):
    key = hashlib.sha256(password).digest()
    if os.path.exists(pw_store_filename):
        pw_store_xml = encryption.decrypt_to_string(key, pw_store_filename)
        try:
            pw_store = ET.fromstring(pw_store_xml)
        except Exception:
            pw_store = None
    else:
        print("Creating new password store")
        pw_store = ET.Element("cryptex_pw_store")
        ET.SubElement(pw_store, "passwords")

        pw_store_xml = ET.tostring(pw_store, encoding='utf8', method='xml')
        print(pw_store_xml)
        encryption.encrypt_from_string(key, pw_store_xml, pw_store_filename)

    return pw_store
