def simplify_path(path: str, from_separator='/', to_separator='/') -> str:
    """Returns the result of removing leading/trailing whitespace and
    consecutive separators from each segment of the given path."""
    path_parts = path.split(from_separator)
    stripped_parts = map(lambda x: x.strip(), path_parts)
    valid_parts = filter(lambda x: x, stripped_parts)
    return to_separator + to_separator.join(valid_parts)


def encode_path(path: str) -> str:
    """Converts a standard *nix/URL-style path to one which uses the '+'
    character for path separators. Before making this replacement, the path
    is simplified, using simplify_path(). For example, given the path /foo/bar/,
    this function will return +foo+bar.
    """
    return simplify_path(path, to_separator='+')


def decode_path(path: str) -> str:
    """Performs the reverse of encode_path(), namely, replacing '+' with
    '/' in the given path."""
    return simplify_path(path, from_separator='+')
