import os
from parameterized import parameterized
from unittest import TestCase
from pw_store import (PasswordStore)
from credential import Credential
from ec_exceptions import ECNotFoundException, ECBadPathException
from node import Node


class TestPasswordStore(TestCase):
    def setUp(self):
        self.test_xml_filename = os.path.join("ut", "store.xml")
        with open(self.test_xml_filename, "rb") as f:
            raw_xml = f.read()
        self.password_store = PasswordStore(raw_xml)

    def test_get_root(self):
        root = self.password_store.get_root()
        self.assertIsNotNone(root)

    def test_get_root_container_by_path(self):
        container = self.set_container_hierarchy(self.password_store.get_root(), ["lvl1"])
        self.assertEqual(container, self.password_store.get_container_by_path(u"/lvl1"))

    def test_get_container_by_nested_path(self):
        container = self.set_container_hierarchy(self.password_store.get_root(), ["lvl1", "lvl2", "lvl3"])
        self.assertEqual(container, self.password_store.get_container_by_path(u"/lvl1/lvl2/lvl3"))

    @parameterized.expand([
        [["lvl1"], u"/lvl1"],
        [["lvl1", "lvl2"], u"/lvl1/lvl2"],
        [["lvl1", "lvl2", "lvl3"], u"/lvl1/lvl2/lvl3"],
    ])
    def test_valid_path(self, levels, path):
        _ = self.set_container_hierarchy(self.password_store.get_root(), levels)
        self.assertTrue(self.password_store.is_valid_path(path))

    @parameterized.expand([
        [["lvl1"], u"/l1"],
        [["lvl1", "lvl2"], u"/lvl1/l"],
        [["lvl1", "lvl2", "lvl3"], u"/lvl1/lvl2/lvl2"],
    ])
    def test_invalid_path(self, levels, path):
        self.set_container_hierarchy(self.password_store.get_root(), levels)
        self.assertFalse(self.password_store.is_valid_path(path))

    @parameterized.expand([
        [[]],
        [["lvl1", "lvl2"]],
        [["lvl1", "lvl2", "lvl3"]],
    ])
    def test_root_path_is_always_available(self, levels):
        self.set_container_hierarchy(self.password_store.get_root(), levels)
        self.assertTrue(self.password_store.is_valid_path(u"/"))

    def test_root_path_returns_root(self):
        self.assertIs(self.password_store.get_root(), self.password_store.get_container_by_path(u"/"))

    def test_nonexistent_container_path_should_raise_exception(self):
        with self.assertRaises(ECNotFoundException):
            self.password_store.get_container_by_path(u"/Something/Not/there")

    def test_get_entry_by_path(self):
        container = self.set_container_hierarchy(self.password_store.get_root(), ["A New Beginning"])
        entry = Credential()
        container.add_credential(entry, u"Entry1")
        self.assertEqual((u"Entry1", entry), self.password_store.get_entry_by_path(u"/A New Beginning/Entry1"))

    def match_entries(self, cont1, cont2):
        self.assertEqual(cont1.get_entry_count(), cont2.get_entry_count())
        for k, e1 in cont1.get_entries():
            try:
                e2 = cont2.get_entry(k)
                self.assertEqual(e1.get_username(), e2.get_username())
                self.assertEqual(e1.get_password(), e2.get_password())
                self.assertEqual(e1.get_url(), e2.get_url())
            except ECNotFoundException:
                self.fail("Credential {0} not found in both containers.".format(k))

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
        serialized_xml = self.password_store.serialize_to_xml()
        store = PasswordStore(serialized_xml)

        self.match_containers(self.password_store.get_root(), store.get_root())

    def test_update_entry_same_name(self):
        old_entry = Credential()
        old_entry.url = u"old_url"
        old_entry.password = u"old_password"
        old_entry.username = u"old_username"
        self.password_store.add_entry(old_entry, u"Old One", u"/")
        new_entry = Credential()
        new_entry.url = u"new_url"
        new_entry.password = u"new_password"
        new_entry.username = u"new_username"
        self.password_store.update_entry(u"/Old One", u"Old One", new_entry)
        ent_name, entry = self.password_store.get_entry_by_path(u"/Old One")
        self.assertEqual(ent_name, u"Old One")
        self.assertEqual(entry, new_entry)

    def test_update_entry_different_name(self):
        old_entry = Credential()
        old_entry.url = u"old_url"
        old_entry.password = u"old_password"
        old_entry.username = u"old_username"
        self.password_store.add_entry(old_entry, u"Old One", u"/")
        new_entry = Credential()
        new_entry.url = u"new_url"
        new_entry.password = u"new_password"
        new_entry.username = u"new_username"
        self.password_store.update_entry(u"/Old One", u"New One", new_entry)
        ent_name, entry = self.password_store.get_entry_by_path(u"/New One")
        self.assertEqual(ent_name, u"New One")
        self.assertEqual(entry, new_entry)

    @staticmethod
    def set_container_hierarchy(root, levels):
        current_level = root
        for level in levels:
            child = Node()
            current_level.add_node(child, level)
            current_level = child
        return current_level

