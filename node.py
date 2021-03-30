from ec_exceptions import ECDuplicateException, ECNotFoundException, ECNaughtyCharacterException
from illegal_chars import ILLEGAL_CHAR_RE


class Node:
    def __init__(self):
        self.__nodes = dict()
        self.__credentials = dict()

    def has_node(self, cont_name):
        return cont_name in self.__nodes

    def get_node(self, name):
        self.ensure_is_present(self.__nodes, name, 'Container')
        return self.__nodes[name]

    def get_node_count(self):
        return len(self.__nodes)

    def is_empty(self):
        return not (self.__nodes and self.__credentials)

    @property
    def nodes(self):
        return frozenset(self.__nodes.items())

    def has_credential(self, name):
        return name in self.__credentials

    def get_credential(self, name):
        self.ensure_is_present(self.__credentials, name, 'Credential')
        return self.__credentials[name]

    def get_credential_count(self):
        return len(self.__credentials)

    @property
    def credentials(self):
        return frozenset(self.__credentials.items())

    def clear(self):
        self.__nodes.clear()
        self.__credentials.clear()

    def add_node(self, node, name):
        self.ensure_add_is_possible(self.__nodes, name, 'Container')
        self.__nodes[name] = node

    def rename_node(self, old_name, new_name):
        self.ensure_rename_is_possible(self.__nodes, old_name, new_name, 'Container')
        cont = self.__nodes.pop(old_name)
        self.add_node(cont, new_name)

    def remove_node(self, name):
        self.ensure_remove_is_possible(self.__nodes, 'Container', name)
        self.__nodes.pop(name)

    def add_credential(self, credential, name):
        self.ensure_add_is_possible(self.__credentials, name, "Credential")
        self.__credentials[name] = credential

    def replace_credential(self, entry, name):
        self.ensure_replace_is_possible(self.__credentials, name, 'Credential')
        self.__credentials[name] = entry

    def rename_credential(self, old_name, new_name):
        self.ensure_rename_is_possible(self.__credentials, old_name, new_name, 'Credential')
        entry = self.__credentials.pop(old_name)
        self.add_credential(entry, new_name)

    def remove_credential(self, name):
        self.ensure_remove_is_possible(self.__credentials, 'Credential', name)
        self.__credentials.pop(name)

    def ensure_add_is_possible(self, containers, name, description):
        self.ensure_not_present(containers, name, description)
        self.ensure_legal_characters(name)

    def ensure_rename_is_possible(self, containers, old_name, new_name, description):
        self.ensure_is_present(containers, old_name, description)
        self.ensure_not_present(containers, new_name, description)
        self.ensure_legal_characters(new_name)

    def ensure_remove_is_possible(self, containers, description, name):
        self.ensure_is_present(containers, name, description)

    def ensure_replace_is_possible(self, containers, name, description):
        self.ensure_is_present(containers, name, description)

    def ensure_is_present(self, containers, name, description):
        if name not in containers:
            raise ECNotFoundException(
                f"{description} with name '{name}' not found")

    def ensure_not_present(self, containers, name, description):
        if name in containers:
            raise ECDuplicateException(f"{description} with name {name} already exists")

    def ensure_legal_characters(self, name):
        if name and ILLEGAL_CHAR_RE.search(name):
            raise ECNaughtyCharacterException(f"Illegal character used in name {name}")

