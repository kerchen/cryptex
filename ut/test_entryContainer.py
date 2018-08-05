from unittest import TestCase
from pw_store import ECDuplicateException, ECNotFoundException, \
                     ECNaughtyCharacterException, Entry, \
                     EntryContainer


class TestEntryContainer(TestCase):
    def setUp(self):
        self.cut = EntryContainer()

    def test_clear(self):
        new_cont = EntryContainer()
        self.cut.add_container(new_cont, "Foo")
        self.assertEqual(1, self.cut.get_container_count())
        self.cut.clear()
        self.assertEqual(0, self.cut.get_container_count())

    def test_add_container(self):
        new_cont = EntryContainer()
        self.cut.add_container(new_cont, "A New Beginning")
        self.assertEqual(1, self.cut.get_container_count())

    def test_get_container(self):
        cont_name = "A New Beginning"
        new_cont = EntryContainer()
        self.cut.add_container(new_cont, cont_name)
        c = self.cut.get_container(cont_name)
        self.assertEqual(c, new_cont)

    def test_get_nonexistent_container(self):
        with self.assertRaises(ECNotFoundException):
            self.cut.get_container("Anything")

    def test_get_containers(self):
        new_cont = EntryContainer()
        self.cut.add_container(new_cont, "Confidence")
        containers = self.cut.get_containers()
        for k, c in containers:
            self.assertEqual("Confidence", k)
            self.assertEqual(new_cont, c)

    def test_rename_nonexistent_container(self):
        with self.assertRaises(ECNotFoundException):
            self.cut.rename_container("old", "new")

    def test_rename_duplicate_container(self):
        cont_name1 = "A New Beginning"
        cont_name2 = "A Newer Beginning"
        self.cut.add_container(EntryContainer(), name=cont_name1)
        self.cut.add_container(EntryContainer(), name=cont_name2)
        with self.assertRaises(ECDuplicateException):
            self.cut.rename_container(cont_name1, cont_name2)

    def test_rename_container(self):
        cont_name1 = "A New Beginning"
        cont_name2 = "A Newer Beginning"
        self.cut.add_container(EntryContainer(), cont_name1)
        self.cut.rename_container(cont_name1, cont_name2)
        with self.assertRaises(ECNotFoundException):
            self.cut.remove_container(cont_name1)
        self.cut.remove_container(cont_name2)
        self.assertEqual(0, self.cut.get_container_count())

    def test_add_and_remove_container(self):
        new_cont = EntryContainer()
        self.cut.add_container(new_cont, name="Queen")
        self.assertEqual(1, self.cut.get_container_count())
        self.cut.remove_container("Queen")
        self.assertEqual(0, self.cut.get_container_count())

    def test_add_duplicate_container(self):
        cont_name = "A New Beginning"
        self.cut.add_container(EntryContainer(), name=cont_name)
        with self.assertRaises(ECDuplicateException):
            self.cut.add_container(EntryContainer(), name=cont_name)

    def test_illegal_container_name(self):
        illegal_chars = ['\\', '/', '@', '#', '.', '?', '%']
        for cont_name in illegal_chars:
            with self.assertRaises(ECNaughtyCharacterException):
                self.cut.add_container(EntryContainer(), name=cont_name)

    def test_illegal_entry_name(self):
        illegal_chars = ['\\', '/', '@', '#', '.', '?', '%']
        for ent_name in illegal_chars:
            with self.assertRaises(ECNaughtyCharacterException):
                self.cut.add_entry(Entry(), name=ent_name)

    def test_add_entry(self):
        new_entry = Entry()
        self.cut.add_entry(new_entry, "Rogue One")
        self.assertEqual(1, self.cut.get_entry_count())

    def test_get_entry(self):
        entry_name = "Enter the Dragon"
        new_entry = Entry()
        self.cut.add_entry(new_entry, entry_name)
        e = self.cut.get_entry(entry_name)
        self.assertEqual(e, new_entry)

    def test_get_nonexistent_entry(self):
        with self.assertRaises(ECNotFoundException):
            self.cut.get_entry("Anything")

    def test_get_entries(self):
        new_entry = Entry()
        self.cut.add_entry(new_entry, name="Rogue One")
        entries = self.cut.get_entries()
        for k, e in entries:
            self.assertEqual("Rogue One", k)
            self.assertEqual(new_entry, e)

    def test_rename_nonexistent_entry(self):
        with self.assertRaises(ECNotFoundException):
            self.cut.rename_entry("old", "new")

    def test_rename_duplicate_entry(self):
        entry_name1 = "Rogue One"
        entry_name2 = "Rogue Two"
        self.cut.add_entry(Entry(), name=entry_name1)
        self.cut.add_entry(Entry(), name=entry_name2)
        with self.assertRaises(ECDuplicateException):
            self.cut.rename_entry(entry_name1, entry_name2)

    def test_rename_entry(self):
        entry_name1 = "Rogue One"
        entry_name2 = "Rogue Two"
        self.cut.add_entry(Entry(), name=entry_name1)
        self.cut.rename_entry(entry_name1, entry_name2)
        with self.assertRaises(ECNotFoundException):
            self.cut.remove_entry(entry_name1)
        self.cut.remove_entry(entry_name2)
        self.assertEqual(0, self.cut.get_entry_count())

    def test_add_and_remove_entry(self):
        new_entry = Entry()
        self.cut.add_entry(new_entry, "Rogue One")
        self.assertEqual(1, self.cut.get_entry_count())
        self.cut.remove_entry("Rogue One")
        self.assertEqual(0, self.cut.get_entry_count())

    def test_add_duplicate_entry(self):
        entry_name = "Rogue One"
        self.cut.add_entry(Entry(), entry_name)
        with self.assertRaises(ECDuplicateException):
            self.cut.add_entry(EntryContainer(), name=entry_name)
