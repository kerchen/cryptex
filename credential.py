class Credential:
    def __init__(self,  username=None, password=None, url=None):
        self.username = username
        self.password = password
        self.url = url

    def get_username(self):
        return self.username

    def set_username(self, username):
        if len(username):
            self.username = username
        else:
            self.username = None

    def get_password(self):
        return self.password

    def set_password(self, password):
        if len(password):
            self.password = password
        else:
            self.password = None

    def get_url(self):
        return self.url

    def set_url(self, url):
        if len(url):
            self.url = url
        else:
            self.url = None