from unittest import TestCase
from credential import Credential

USERNAME="UserName"
PASSWORD="P@55werd"
URL="https//www.example.com"


class TestCredential(TestCase):
    def setUp(self):
        self.credential = Credential(username=USERNAME,
                                     password=PASSWORD, url=URL)

    def test_get_username(self):
        self.assertEqual(USERNAME, self.credential.get_username())

    def test_set_username(self):
        new_username = self.create_different_data(USERNAME)
        self.credential.set_username(new_username)
        self.assertEqual(new_username, self.credential.get_username())

    def test_get_password(self):
        self.assertEqual(PASSWORD, self.credential.get_password())

    def test_set_password(self):
        new_password = self.create_different_data(PASSWORD)
        self.credential.set_password(new_password)
        self.assertEqual(new_password, self.credential.get_password())

    def test_get_url(self):
        self.assertEqual(URL, self.credential.get_url())

    def test_set_url(self):
        new_url = self.create_different_data(URL)
        self.credential.set_url(new_url)
        self.assertEqual(new_url, self.credential.get_url())

    @staticmethod
    def create_different_data(name):
        return name + "1"


