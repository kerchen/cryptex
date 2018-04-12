import os
from unittest import TestCase
from pw_store import Entry, EntryContainer, PasswordStore

class TestPasswordStore(TestCase):
    def setUp(self):
        with open(os.path.join("ut", "store.xml"), "rb") as f:
            raw_xml = f.read()
        self.cut = PasswordStore(raw_xml)

    def test_get_root(self):
        root = self.cut.get_root()
        self.assertIsNotNone(root)
