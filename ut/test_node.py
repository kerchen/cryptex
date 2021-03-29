from unittest import TestCase
from parameterized import parameterized, parameterized_class

from credential import Credential
from illegal_chars import ILLEGAL_NAME_CHARS
from ec_exceptions import ECDuplicateException, ECNotFoundException, ECNaughtyCharacterException
from node import Node


class TestNode(TestCase):
    def setUp(self):
        self.cut = Node()

    def test_clear(self):
        new_cont = Node()
        self.cut.add_node(new_cont, "Foo")
        self.assertEqual(1, self.cut.get_container_count())
        self.cut.clear()
        self.assertEqual(0, self.cut.get_container_count())

    def test_add_container(self):
        new_cont = Node()
        self.cut.add_node(new_cont, "A New Beginning")
        self.assertTrue(self.cut.has_container("A New Beginning"))

    def test_get_container(self):
        cont_name = "A New Beginning"
        new_cont = Node()
        self.cut.add_node(new_cont, cont_name)
        c = self.cut.get_container(cont_name)
        self.assertEqual(c, new_cont)

    def test_get_nonexistent_container(self):
        with self.assertRaises(ECNotFoundException):
            self.cut.get_container("Anything")

    def test_get_containers(self):
        new_cont = Node()
        self.cut.add_node(new_cont, "Confidence")
        containers = self.cut.get_containers()
        for k, c in containers:
            self.assertEqual("Confidence", k)
            self.assertEqual(new_cont, c)

    def test_rename_nonexistent_container(self):
        with self.assertRaises(ECNotFoundException):
            self.cut.rename_node("old", "new")

    def test_rename_duplicate_container(self):
        cont_name1 = "A New Beginning"
        cont_name2 = "A Newer Beginning"
        self.cut.add_node(Node(), name=cont_name1)
        self.cut.add_node(Node(), name=cont_name2)
        with self.assertRaises(ECDuplicateException):
            self.cut.rename_node(cont_name1, cont_name2)

    def test_rename_container(self):
        cont_name1 = "A New Beginning"
        cont_name2 = "A Newer Beginning"
        self.cut.add_node(Node(), cont_name1)
        self.cut.rename_node(cont_name1, cont_name2)
        with self.assertRaises(ECNotFoundException):
            self.cut.remove_node(cont_name1)
        self.cut.remove_node(cont_name2)
        self.assertEqual(0, self.cut.get_container_count())

    def test_add_and_remove_container(self):
        new_cont = Node()
        self.cut.add_node(new_cont, name="Queen")
        self.assertEqual(1, self.cut.get_container_count())
        self.cut.remove_node("Queen")
        self.assertEqual(0, self.cut.get_container_count())

    def test_add_duplicate_container(self):
        cont_name = "A New Beginning"
        self.cut.add_node(Node(), name=cont_name)
        with self.assertRaises(ECDuplicateException) as context:
            self.cut.add_node(Node(), name=cont_name)
        self.assertEqual(f"Container with name {cont_name} already exists", str(context.exception))

    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_character_at_start_of_node_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.cut.add_node, Node(), f"{c}after")

    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_character_in_middle_of_container_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.cut.add_node, Node(), f"before{c}after")

    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_character_at_end_of_container_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.cut.add_node, Node(), f"before{c}")

    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_character_at_start_of_credential_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.cut.add_credential, Credential(), f"{c}after")

    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_in_middle_of_credential_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.cut.add_credential, Credential(), f"before{c}after")

    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_character_at_end_of_credential_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.cut.add_credential, Credential(), "before" + c)

    def test_add_entry(self):
        new_entry = Credential()
        self.cut.add_credential(new_entry, "Rogue One")
        self.assertTrue(self.cut.has_entry("Rogue One"))

    def test_replace_entry(self):
        old_entry = Credential()
        self.cut.add_credential(old_entry, "Old One")
        new_entry = Credential()
        self.cut.replace_credential(new_entry, "Old One")
        entry = self.cut.get_entry("Old One")
        self.assertEqual(new_entry, entry)

    def test_get_entry(self):
        entry_name = "Enter the Dragon"
        new_entry = Credential()
        self.cut.add_credential(new_entry, entry_name)
        entry = self.cut.get_entry(entry_name)
        self.assertEqual(new_entry, entry)

    def test_get_nonexistent_entry(self):
        with self.assertRaises(ECNotFoundException):
            self.cut.get_entry("Anything")

    def test_get_entries(self):
        new_entry = Credential()
        self.cut.add_credential(new_entry, name="Rogue One")
        entries = self.cut.get_entries()
        for k, e in entries:
            self.assertEqual("Rogue One", k)
            self.assertEqual(new_entry, e)

    def test_rename_nonexistent_entry(self):
        with self.assertRaises(ECNotFoundException):
            self.cut.rename_credential("old", "new")

    def test_rename_duplicate_entry(self):
        entry_name1 = "Rogue One"
        entry_name2 = "Rogue Two"
        self.cut.add_credential(Credential(), name=entry_name1)
        self.cut.add_credential(Credential(), name=entry_name2)
        with self.assertRaises(ECDuplicateException):
            self.cut.rename_credential(entry_name1, entry_name2)

    def test_rename_entry(self):
        entry_name1 = "Rogue One"
        entry_name2 = "Rogue Two"
        self.cut.add_credential(Credential(), name=entry_name1)
        self.cut.rename_credential(entry_name1, entry_name2)
        with self.assertRaises(ECNotFoundException):
            self.cut.remove_credential(entry_name1)
        self.cut.remove_credential(entry_name2)
        self.assertEqual(0, self.cut.get_entry_count())

    def test_add_and_remove_entry(self):
        new_entry = Credential()
        self.cut.add_credential(new_entry, "~ Rogue-1")
        self.assertEqual(1, self.cut.get_entry_count())
        self.cut.remove_credential("~ Rogue-1")
        self.assertEqual(0, self.cut.get_entry_count())

    def test_add_duplicate_entry(self):
        entry_name = "Rogue One"
        self.cut.add_credential(Credential(), entry_name)
        with self.assertRaises(ECDuplicateException) as context:
            self.cut.add_credential(Node(), name=entry_name)
        self.assertEqual(f"Credential with name {entry_name} already exists", str(context.exception))

    def assertRaiseNaughtyCharacterException(self, function, parameter, name):
        with self.assertRaises(ECNaughtyCharacterException):
            function(parameter, name)
