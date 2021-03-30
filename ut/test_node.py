from unittest import TestCase

from parameterized import parameterized

from credential import Credential
from ec_exceptions import ECDuplicateException, ECNotFoundException, ECNaughtyCharacterException
from illegal_chars import ILLEGAL_NAME_CHARS
from node import Node


class NodeTestBase(TestCase):
    def setUp(self):
        self.root = Node()

    def add_new_node(self, name):
        node = Node()
        self.root.add_node(node, name=name)
        return node

    def add_new_credential(self, name):
        credential = Credential()
        self.root.add_credential(credential, name=name)
        return credential

    def assertRaiseNaughtyCharacterException(self, function, parameter, name):
        with self.assertRaises(ECNaughtyCharacterException):
            function(parameter, name)


class TestNodeDefaults(NodeTestBase):
    def test_has_no_nodes(self):
        self.assertSetEqual(set(), self.root.nodes)

    def test_has_node_count_of_zero(self):
        self.assertEqual(0, self.root.get_node_count())

    def test_has_no_credentials(self):
        self.assertSetEqual(set(), self.root.credentials)

    def test_has_credential_count_of_zero(self):
        self.assertEqual(0, self.root.get_credential_count())

    def test_is_empty(self):
        self.assertTrue(self.root.is_empty())

class TestNodeAddNode(NodeTestBase):
    def test_has_node(self):
        self.assertFalse(self.root.has_node('node'))
        self.add_new_node('node')
        self.assertTrue(self.root.has_node('node'))

    @parameterized.expand([(['a'], 1),
                           (['a', 'b','c'], 3)])
    def test_increases_node_count(self, node_names, expected_node_count):
        for node_name in node_names:
            self.add_new_node(node_name)

        self.assertEqual(expected_node_count, self.root.get_node_count())

    def test_results_in_nodes_having_it(self):
        node = self.add_new_node('node')
        self.assertEqual({('node', node)}, self.root.nodes)

    def test_results_in_not_being_empty(self):
        self.add_new_node('node')
        self.assertFalse(self.root.is_empty())

    def test_raises_duplicate_exception_for_existing_name(self):
        node_name = 'node'
        self.add_new_node(node_name)
        with self.assertRaises(ECDuplicateException) as context:
            self.add_new_node(node_name)
        self.assertEqual(f"Container with name {node_name} already exists", str(context.exception))

    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_character_at_start_of_node_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.root.add_node, Node(), f"{c}after")


    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_character_in_middle_of_node_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.root.add_node, Node(), f"before{c}after")


    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_character_at_end_of_node_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.root.add_node, Node(), f"before{c}")


class TestNodeRemoveNode(NodeTestBase):
    def test_results_in_not_having_the_node(self):
        self.add_new_node('foo')
        self.add_new_node('bar')
        self.add_new_node('baz')

        self.root.remove_node('bar')

        self.assertFalse(self.root.has_node('bar'))

    def test_results_in_decreased_node_count(self):
        self.add_new_node('foo')
        self.add_new_node('bar')
        self.add_new_node('baz')

        self.root.remove_node('bar')

        self.assertEqual(2, self.root.get_node_count())

    def test_results_in_removed_node(self):
        foo = self.add_new_node('foo')
        self.add_new_node('bar')
        baz = self.add_new_node('baz')

        self.root.remove_node('bar')

        self.assertEqual({('foo', foo), ('baz', baz)}, self.root.nodes)


class TestNodeClear(NodeTestBase):
    def test_resets_node_count(self):
        self.add_new_node('foo')
        self.add_new_node('bar')
        self.root.clear()
        self.assertEqual(0, self.root.get_node_count())

    def test_results_in_empty_nodes(self):
        self.add_new_node('foo')
        self.add_new_node('bar')
        self.root.clear()
        self.assertSetEqual(set(), self.root.nodes)

    def test_resets_credential_count(self):
        self.add_new_credential('foo')
        self.add_new_credential('bar')
        self.root.clear()
        self.assertEqual(0, self.root.get_credential_count())

    def test_results_in_empty_credentials(self):
        self.add_new_credential('foo')
        self.add_new_credential('bar')
        self.root.clear()
        self.assertEqual(set(), self.root.credentials)


class TestGetNode(NodeTestBase):
    def test_returns_correct_node(self):
        node = self.add_new_node('foo')
        self.add_new_node('bar')
        c = self.root.get_node('foo')
        self.assertIs(c, node)

    def test_throws_exceptions_when_accessing_nonexistent_node(self):
        self.add_new_node('node')
        with self.assertRaises(ECNotFoundException):
            self.root.get_node('non_existing_node')


class TestGetNodes(NodeTestBase):
    def test_get_nodes(self):
        new_cont = self.add_new_node('node')
        containers = self.root.nodes
        self.assertEqual({('node', new_cont)}, containers)


class TestRenameNode(NodeTestBase):
    def test_should_throw_not_found_exception_for_nonexistent_nodes(self):
        self.add_new_node('node')
        with self.assertRaises(ECNotFoundException):
            self.root.rename_node('non_existing_node', 'new_name')

    def test_should_throw_duplicate_exception_for_existing_nodes(self):
        self.add_new_node('old')
        self.add_new_node('new')
        with self.assertRaises(ECDuplicateException):
            self.root.rename_node('old', 'new')

    def test_keeps_new_name(self):
        self.add_new_node('old')
        self.root.rename_node('old', 'new')
        self.assertTrue(self.root.has_node('new'))

    def test_loses_old_name(self):
        self.add_new_node('old')
        self.root.rename_node('old', 'new')
        self.assertFalse(self.root.has_node('old'))


class TestCredential(NodeTestBase):
    def test_add_credential(self):
        self.add_new_credential("Rogue One")
        self.assertTrue(self.root.has_credential("Rogue One"))

    def test_add_results_in_not_being_empty(self):
        self.add_new_credential('credential')
        self.assertFalse(self.root.is_empty())

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

    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_character_at_start_of_credential_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.root.add_credential, Credential(), f"{c}after")


    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_in_middle_of_credential_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.root.add_credential, Credential(), f"before{c}after")


    @parameterized.expand(ILLEGAL_NAME_CHARS)
    def test_illegal_character_at_end_of_credential_name(self, c):
        self.assertRaiseNaughtyCharacterException(self.root.add_credential, Credential(), "before" + c)


