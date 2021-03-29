from ec_exceptions import ECDuplicateException, ECNotFoundException, ECNaughtyCharacterException
from illegal_chars import ILLEGAL_CHAR_RE


class Node:
    def __init__(self):
        self.containers = dict()
        self.entries = dict()

    def has_container(self, cont_name):
        return cont_name in self.containers

    def get_container(self, name):
        self.ensure_is_present(self.containers, name, 'Container')
        return self.containers[name]

    def get_container_count(self):
        return len(self.containers)

    def get_containers(self):
        return frozenset(self.containers.items())

    def has_entry(self, name):
        return name in self.entries

    def get_entry(self, name):
        self.ensure_is_present(self.entries, name, 'Credential')
        return self.entries[name]

    def get_entry_count(self):
        return len(self.entries)

    def get_entries(self):
        return frozenset(self.entries.items())

    def clear(self):
        self.containers.clear()
        self.entries.clear()

    def add_node(self, cont, name):
        self.ensure_add_is_possible(self.containers, name, 'Container')
        self.containers[name] = cont

    def rename_node(self, old_name, new_name):
        self.ensure_rename_is_possible(self.containers, old_name, new_name, 'Container')
        cont = self.containers.pop(old_name)
        self.add_node(cont, new_name)

    def remove_node(self, name):
        self.ensure_remove_is_possible(self.containers, 'Container', name)
        self.containers.pop(name)

    def add_credential(self, entry, name):
        self.ensure_add_is_possible(self.entries, name, "Credential")
        self.entries[name] = entry

    def replace_credential(self, entry, name):
        self.ensure_replace_is_possible(self.entries, name, 'Credential')
        self.entries[name] = entry

    def rename_credential(self, old_name, new_name):
        self.ensure_rename_is_possible(self.entries, old_name, new_name, 'Credential')
        entry = self.entries.pop(old_name)
        self.add_credential(entry, new_name)

    def remove_credential(self, name):
        self.ensure_remove_is_possible(self.entries, 'Credential', name)
        self.entries.pop(name)

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

