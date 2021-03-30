from unittest import TestCase
from parameterized import parameterized, parameterized_class

from credential import Credential
from illegal_chars import ILLEGAL_NAME_CHARS
from ec_exceptions import ECDuplicateException, ECNotFoundException, ECNaughtyCharacterException
from node import Node

class TestNodeDefaults(TestCase):
    def setUp(self):
        self.root = Node()

    def test_has_no_nodes(self):
        self.assertSetEqual(set(), self.root.nodes)

    def test_has_node_count_of_zero(self):
        self.assertEqual(0, self.root.get_node_count())

    def test_has_no_credentials(self):
        self.assertSetEqual(set(), self.root.credentials)

    def test_has_credential_count_of_zero(self):
        self.assertEqual(0, self.root.get_credential_count())


class TestNodeAdding(TestCase):
    def setUp(self):
        self.root = Node()

    def test_makes_node_available(self):
        new_cont = Node()
        self.root.add_node(new_cont, "A New Beginning")
        self.assertTrue(self.root.has_node("A New Beginning"))


class TestNodeAdding(TestCase):
    def setUp(self):
        self.root = Node()

    def test_clear(self):
        new_cont = Node()
        self.root.add_node(new_cont, "Foo")
        self.assertEqual(1, self.root.get_node_count())
        self.root.clear()
        self.assertEqual(0, self.root.get_node_count())

    def test_get_node(self):
        new_cont = self.add_new_node('node_name')
        c = self.root.get_node('node_name')
        self.assertIs(c, new_cont)

    def test_get_nonexistent_node(self):
        with self.assertRaises(ECNotFoundException):
            self.root.get_node("Anything")

    def test_get_nodes(self):
        new_cont = self.add_new_node('Confidence')
        containers = self.root.nodes
        self.assertEqual({('Confidence', new_cont)}, containers)

    def test_rename_nonexistent_node(self):
        with self.assertRaises(ECNotFoundException):
            self.root.rename_node('old_name', 'new_name')

    def test_rename_duplicate_node(self):
        self.add_new_node('old_name')
        self.add_new_node('new_name')
        with self.assertRaises(ECDuplicateException):
            self.root.rename_node('old_name', 'new_name')

    def add_new_node(self, cont_name2):
        node = Node()
        self.root.add_node(node, name=cont_name2)
        return node

    def test_rename_node(self):
        cont_name1 = "A New Beginning"
        cont_name2 = "A Newer Beginning"
        self.root.add_node(Node(), cont_name1)
        self.root.rename_node(cont_name1, cont_name2)
        with self.assertRaises(ECNotFoundException):
            self.root.remove_node(cont_name1)
        self.root.remove_node(cont_name2)
        self.assertEqual(0, self.root.get_node_count())

    def test_add_and_remove_node(self):
        new_cont = Node()
        self.root.add_node(new_cont, name="Queen")
        self.assertEqual(1, self.root.get_node_count())
        self.root.remove_node("Queen")
        self.assertEqual(0, self.root.get_node_count())

    def test_add_duplicate_node(self):
        cont_name = "A New Beginning"
        self.root.add_node(Node(), name=cont_name)
        with self.assertRaises(ECDuplicateException) as context:
            self.root.add_node(Node(), name=cont_name)
        self.assertEqual(f"Container with name {cont_name} already exists", str(context.exception))

    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_character_at_start_of_node_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.root.add_node, Node(), f"{c}after")

    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_character_in_middle_of_node_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.root.add_node, Node(), f"before{c}after")

    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_character_at_end_of_node_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.root.add_node, Node(), f"before{c}")

    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_character_at_start_of_credential_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.root.add_credential, Credential(), f"{c}after")

    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_in_middle_of_credential_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.root.add_credential, Credential(), f"before{c}after")

    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_character_at_end_of_credential_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.root.add_credential, Credential(), "before" + c)

    def test_add_credential(self):
        new_credential = Credential()
        self.root.add_credential(new_credential, "Rogue One")
        self.assertTrue(self.root.has_credential("Rogue One"))

    def test_replace_credential(self):
        old_credential = Credential()
        self.root.add_credential(old_credential, "Old One")
        new_credential = Credential()
        self.root.replace_credential(new_credential, "Old One")
        entry = self.root.get_credential("Old One")
        self.assertEqual(new_credential, entry)

    def test_get_credential(self):
        entry_name = "Enter the Dragon"
        new_credential = Credential()
        self.root.add_credential(new_credential, entry_name)
        entry = self.root.get_credential(entry_name)
        self.assertEqual(new_credential, entry)

    def test_get_nonexistent_credential(self):
        with self.assertRaises(ECNotFoundException):
            self.root.get_credential("Anything")

    def test_get_entries(self):
        new_credential = Credential()
        self.root.add_credential(new_credential, name="Rogue One")
        entries = self.root.credentials
        for k, e in entries:
            self.assertEqual("Rogue One", k)
            self.assertEqual(new_credential, e)

    def test_rename_nonexistent_credential(self):
        with self.assertRaises(ECNotFoundException):
            self.root.rename_credential("old", "new")

    def test_rename_duplicate_credential(self):
        entry_name1 = "Rogue One"
        entry_name2 = "Rogue Two"
        self.root.add_credential(Credential(), name=entry_name1)
        self.root.add_credential(Credential(), name=entry_name2)
        with self.assertRaises(ECDuplicateException):
            self.root.rename_credential(entry_name1, entry_name2)

    def test_rename_credential(self):
        entry_name1 = "Rogue One"
        entry_name2 = "Rogue Two"
        self.root.add_credential(Credential(), name=entry_name1)
        self.root.rename_credential(entry_name1, entry_name2)
        with self.assertRaises(ECNotFoundException):
            self.root.remove_credential(entry_name1)
        self.root.remove_credential(entry_name2)
        self.assertEqual(0, self.root.get_credential_count())

    def test_add_and_remove_credential(self):
        new_credential = Credential()
        self.root.add_credential(new_credential, "~ Rogue-1")
        self.assertEqual(1, self.root.get_credential_count())
        self.root.remove_credential("~ Rogue-1")
        self.assertEqual(0, self.root.get_credential_count())

    def test_add_duplicate_credential(self):
        entry_name = "Rogue One"
        self.root.add_credential(Credential(), entry_name)
        with self.assertRaises(ECDuplicateException) as context:
            self.root.add_credential(Node(), name=entry_name)
        self.assertEqual(f"Credential with name {entry_name} already exists", str(context.exception))

    def assertRaiseNaughtyCharacterException(self, function, parameter, name):
        with self.assertRaises(ECNaughtyCharacterException):
            function(parameter, name)
