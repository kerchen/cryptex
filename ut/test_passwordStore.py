import os
from unittest import TestCase
from pw_store import Entry, EntryContainer, PasswordStore


class TestPasswordStore(TestCase):
    def setUp(self):
        self.test_xml_filename = os.path.join("ut", "store.xml")
        with open(self.test_xml_filename, "rb") as f:
            raw_xml = f.read()
        self.cut = PasswordStore(raw_xml)

    def test_get_root(self):
        root = self.cut.get_root()
        self.assertIsNotNone(root)

    ''' This test is too brittle. Need to figure out how to guarantee order
        of elements.
    def test_roundtrip_xml_serialization(self):
        serialized_xml = self.cut.serialize_to_xml()
        serialized_xml = serialized_xml.replace("\n", "")
        file_xml = ""
        with open(self.test_xml_filename, "rb") as f:
            for line in f:
                file_xml += line.strip()
        self.assertEqual(serialized_xml, file_xml)
    '''
