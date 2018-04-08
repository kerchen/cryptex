from unittest import TestCase
from pw_store import ECDuplicateException, ECNotFoundException, EntryContainer


CONTAINER_NAME = "Super Container!"


class TestEntryContainer(TestCase):
    def setUp(self):
        self.cut = EntryContainer(name=CONTAINER_NAME)

    def test_get_name(self):
        self.assertEqual(CONTAINER_NAME, self.cut.get_name())

    def test_set_name(self):
        new_name = CONTAINER_NAME + "1"
        self.cut.set_name(new_name)
        self.assertEqual(new_name, self.cut.get_name())

    def test_add_container(self):
        new_cont = EntryContainer(name="A New Beginning")
        self.cut.add_container(new_cont)
        self.assertEqual(1, self.cut.get_container_count())

    def test_clear(self):
        new_cont = EntryContainer(name="A New Beginning")
        self.cut.add_container(new_cont)
        self.assertEqual(1, self.cut.get_container_count())
        self.cut.clear()
        self.assertEqual(0, self.cut.get_container_count())

    def test_rename_nonexistent_container(self):
        with self.assertRaises(ECNotFoundException):
            self.cut.rename_container("old", "new")

    def test_rename_duplicate_container(self):
        cont_name1 = "A New Beginning"
        cont_name2 = "A Newer Beginning"
        self.cut.add_container(EntryContainer(name=cont_name1))
        self.cut.add_container(EntryContainer(name=cont_name2))
        with self.assertRaises(ECDuplicateException):
            self.cut.rename_container(cont_name1, cont_name2)

    def test_rename_container(self):
        cont_name1 = "A New Beginning"
        cont_name2 = "A Newer Beginning"
        self.cut.add_container(EntryContainer(name=cont_name1))
        self.cut.rename_container(cont_name1, cont_name2)
        with self.assertRaises(ECNotFoundException):
            self.cut.remove_container(cont_name1)
        self.cut.remove_container(cont_name2)
        self.assertEqual(0, self.cut.get_container_count())

    def test_add_and_remove_container(self):
        new_cont = EntryContainer(name="A New Beginning")
        self.cut.add_container(new_cont)
        self.assertEqual(1, self.cut.get_container_count())
        self.cut.remove_container(new_cont.get_name())
        self.assertEqual(0, self.cut.get_container_count())

    def test_add_duplicate_container(self):
        cont_name = "A New Beginning"
        self.cut.add_container(EntryContainer(name=cont_name))
        with self.assertRaises(ECDuplicateException):
            self.cut.add_container(EntryContainer(name=cont_name))

    def test_add_entry(self):
        self.fail()
