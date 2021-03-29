from ec_exceptions import ECDuplicateException, ECNotFoundException, ECNaughtyCharacterException
from illegal_chars import ILLEGAL_CHAR_RE


class Node:
    def __init__(self):
        self.nodes = dict()
        self.credentials = dict()

    def has_container(self, cont_name):
        return cont_name in self.nodes

    def get_node(self, name):
        self.ensure_is_present(self.nodes, name, 'Container')
        return self.nodes[name]

    def get_node_count(self):
        return len(self.nodes)

    def get_nodes(self):
        return frozenset(self.nodes.items())

    def has_credential(self, name):
        return name in self.credentials

    def get_credential(self, name):
        self.ensure_is_present(self.credentials, name, 'Credential')
        return self.credentials[name]

    def get_credential_count(self):
        return len(self.credentials)

    def get_credentials(self):
        return frozenset(self.credentials.items())

    def clear(self):
        self.nodes.clear()
        self.credentials.clear()

    def add_node(self, node, name):
        self.ensure_add_is_possible(self.nodes, name, 'Container')
        self.nodes[name] = node

    def rename_node(self, old_name, new_name):
        self.ensure_rename_is_possible(self.nodes, old_name, new_name, 'Container')
        cont = self.nodes.pop(old_name)
        self.add_node(cont, new_name)

    def remove_node(self, name):
        self.ensure_remove_is_possible(self.nodes, 'Container', name)
        self.nodes.pop(name)

    def add_credential(self, credential, name):
        self.ensure_add_is_possible(self.credentials, name, "Credential")
        self.credentials[name] = credential

    def replace_credential(self, entry, name):
        self.ensure_replace_is_possible(self.credentials, name, 'Credential')
        self.credentials[name] = entry

    def rename_credential(self, old_name, new_name):
        self.ensure_rename_is_possible(self.credentials, old_name, new_name, 'Credential')
        entry = self.credentials.pop(old_name)
        self.add_credential(entry, new_name)

    def remove_credential(self, name):
        self.ensure_remove_is_possible(self.credentials, 'Credential', name)
        self.credentials.pop(name)

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

