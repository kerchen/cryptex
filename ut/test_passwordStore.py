import os
from unittest import TestCase
from pw_store import (ECBadPathException, ECNotFoundException, Entry,
                      EntryContainer, PasswordStore)


class TestPasswordStore(TestCase):
    def setUp(self):
        self.test_xml_filename = os.path.join("ut", "store.xml")
        with open(self.test_xml_filename, "rb") as f:
            raw_xml = f.read()
        self.cut = PasswordStore(raw_xml)

    def test_get_root(self):
        root = self.cut.get_root()
        self.assertIsNotNone(root)

    def test_get_container_by_path(self):
        root = self.cut.get_root()
        lvl1 = EntryContainer()
        lvl2 = EntryContainer()
        lvl3 = EntryContainer()
        lvl2.add_container(lvl3, u"lvl3")
        lvl1.add_container(lvl2, u"lvl2")
        root.add_container(lvl1, u"lvl1")
        self.assertEqual(lvl1, self.cut.get_container_by_path(u"/lvl1"))
        self.assertEqual(lvl2, self.cut.get_container_by_path(u"/lvl1/lvl2"))
        self.assertEqual(lvl3, self.cut.get_container_by_path(u"/lvl1/lvl2/lvl3"))

    def test_valid_path(self):
        root = self.cut.get_root()
        lvl1 = EntryContainer()
        lvl2 = EntryContainer()
        lvl1.add_container(lvl2, u"lvl2")
        root.add_container(lvl1, u"lvl1")
        self.assertTrue(self.cut.is_valid_path(u"/lvl1"))
        self.assertTrue(self.cut.is_valid_path(u"/lvl1/lvl2"))
        self.assertFalse(self.cut.is_valid_path(u"lvl2"))

    def test_invalid_container_path(self):
        with self.assertRaises(ECNotFoundException):
            self.cut.get_container_by_path(u"/Something/Not/there")

    def test_get_entry_by_path(self):
        new_cont = EntryContainer()
        entry = Entry()
        new_cont.add_entry(entry, u"Entry1")
        self.cut.add_container(new_cont, u"A New Beginning", u"/")
        self.assertEqual((u"Entry1", entry), self.cut.get_entry_by_path(u"/A New Beginning/Entry1"))

    def match_entries(self, cont1, cont2):
        self.assertEqual(cont1.get_entry_count(), cont2.get_entry_count())
        for k, e1 in cont1.get_entries():
            try:
                e2 = cont2.get_entry(k)
                self.assertEqual(e1.get_username(), e2.get_username())
                self.assertEqual(e1.get_password(), e2.get_password())
                self.assertEqual(e1.get_url(), e2.get_url())
            except ECNotFoundException:
                self.fail("Entry {0} not found in both containers.".format(k))

    def match_containers(self, cont1, cont2):
        self.assertEqual(cont1.get_container_count(),
                         cont2.get_container_count())
        self.match_entries(cont1, cont2)
        for k, c1 in cont1.get_containers():
            try:
                c2 = cont2.get_container(k)
                self.match_containers(c1, c2)
            except ECNotFoundException:
                self.fail("Container {0} not found in both containers.".format(k))

    def test_roundtrip_xml_serialization(self):
        serialized_xml = self.cut.serialize_to_xml()
        store = PasswordStore(serialized_xml)

        self.match_containers(self.cut.get_root(), store.get_root())

    def test_update_entry_same_name(self):
        old_entry = Entry()
        old_entry.url = u"old_url"
        old_entry.password = u"old_password"
        old_entry.username = u"old_username"
        self.cut.add_entry(old_entry, u"Old One", u"/")
        new_entry = Entry()
        new_entry.url = u"new_url"
        new_entry.password = u"new_password"
        new_entry.username = u"new_username"
        self.cut.update_entry(u"/Old One", u"Old One", new_entry)
        ent_name, entry = self.cut.get_entry_by_path(u"/Old One")
        self.assertEqual(ent_name, u"Old One")
        self.assertEqual(entry, new_entry)

    def test_update_entry_different_name(self):
        old_entry = Entry()
        old_entry.url = u"old_url"
        old_entry.password = u"old_password"
        old_entry.username = u"old_username"
        self.cut.add_entry(old_entry, u"Old One", u"/")
        new_entry = Entry()
        new_entry.url = u"new_url"
        new_entry.password = u"new_password"
        new_entry.username = u"new_username"
        self.cut.update_entry(u"/Old One", u"New One", new_entry)
        ent_name, entry = self.cut.get_entry_by_path(u"/New One")
        self.assertEqual(ent_name, u"New One")
        self.assertEqual(entry, new_entry)
