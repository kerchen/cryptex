from unittest import TestCase
from pw_store import Entry


ENTRY_NAME="EntryName"
USERNAME="UserName"
PASSWORD="P@55werd"
URL="https//www.example.com"


class TestEntry(TestCase):
    def setUp(self):
        self.cut = Entry(name=ENTRY_NAME, username=USERNAME,
                         password=PASSWORD, url=URL)

    def test_get_name(self):
        self.assertEqual(ENTRY_NAME, self.cut.get_name())

    def test_set_name(self):
        new_name = ENTRY_NAME + "1"
        self.cut.set_name(new_name)
        self.assertEqual(new_name, self.cut.get_name())

    def test_get_username(self):
        self.assertEqual(USERNAME, self.cut.get_username())

    def test_set_username(self):
        new_username = USERNAME + "1"
        self.cut.set_username(new_username)
        self.assertEqual(new_username, self.cut.get_username())

    def test_get_password(self):
        self.assertEqual(PASSWORD, self.cut.get_password())

    def test_set_password(self):
        new_password = PASSWORD + "1"
        self.cut.set_password(new_password)
        self.assertEqual(new_password, self.cut.get_password())

    def test_get_url(self):
        self.assertEqual(URL, self.cut.get_url())

    def test_set_url(self):
        new_url = URL + "1"
        self.cut.set_url(new_url)
        self.assertEqual(new_url, self.cut.get_url())


