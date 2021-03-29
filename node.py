from illegal_chars import ILLEGAL_CHAR_RE
from ec_exceptions import ECDuplicateException, ECNotFoundException, ECNaughtyCharacterException


class Node:
    def __init__(self):
        self.containers = dict()
        self.entries = dict()

    def has_container(self, cont_name):
        return cont_name in self.containers

    def get_container(self, cont_name):
        if cont_name not in self.containers:
            raise ECNotFoundException(
                "Container with name '{0}' not found".format(cont_name))
        return self.containers[cont_name]

    def get_container_count(self):
        return len(self.containers)

    def get_containers(self):
        return frozenset(self.containers.items())

    def has_entry(self, entry_name):
        return entry_name in self.entries

    def get_entry(self, entry_name):
        if entry_name not in self.entries:
            raise ECNotFoundException(
                "Credential with name '{0}' not found".format(entry_name))
        return self.entries[entry_name]

    def get_entry_count(self):
        return len(self.entries)

    def get_entries(self):
        return frozenset(self.entries.items())

    def clear(self):
        self.containers.clear()
        self.entries.clear()

    def add_node(self, cont, name):
        self.ensure_add_is_possible('container', self.containers, name)
        self.containers[name] = cont

    def ensure_add_is_possible(self, container, containers, name):
        if name in containers:
            raise ECDuplicateException(f"Duplicate {container} name {name}")
        if name and ILLEGAL_CHAR_RE.search(name):
            raise ECNaughtyCharacterException(
                "Illegal character used in name {0}".format(name))

    def rename_node(self, old_name, new_name):
        if old_name not in self.containers:
            raise ECNotFoundException(
                "Container with name '{0}' not found".format(old_name))
        if new_name in self.containers:
            raise ECDuplicateException(
                "Container with name '{0}' already present".format(new_name))
        if ILLEGAL_CHAR_RE.search(new_name):
            raise ECNaughtyCharacterException(
                "Illegal character used in new name {0}".format(new_name))
        cont = self.containers.pop(old_name)
        self.add_node(cont, new_name)

    def remove_node(self, name):
        if name not in self.containers:
            raise ECNotFoundException(
                "Container with name '{}' not found".format(name))
        self.containers.pop(name)

    def add_credential(self, entry, name):
        if name in self.entries:
            raise ECDuplicateException(
                "Credential with name {0} already exists".format(name))
        if ILLEGAL_CHAR_RE.search(name):
            raise ECNaughtyCharacterException(
                "Illegal character used in name {0}".format(name))
        self.entries[name] = entry

    def replace_credential(self, entry, name):
        if name not in self.entries:
            raise ECNotFoundException(
                "Credential with name '{0}' not found".format(name))
        self.entries[name] = entry

    def rename_credential(self, old_name, new_name):
        if old_name not in self.entries:
            raise ECNotFoundException(
                "Credential with name '{0}' not found".format(old_name))
        if new_name in self.entries:
            raise ECDuplicateException(
                "Credential with name '{0}' already present".format(new_name))
        if ILLEGAL_CHAR_RE.search(new_name):
            raise ECNaughtyCharacterException(
                "Illegal character used in new name {0}".format(new_name))
        entry = self.entries.pop(old_name)
        self.add_credential(entry, new_name)

    def remove_credential(self, name):
        if name not in self.entries:
            raise ECNotFoundException(
                "Credential with name '{}' not found".format(name))
        self.entries.pop(name)