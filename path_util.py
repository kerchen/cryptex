
def simplify_path(path):
    """Returns the result of removing leading/trailing whitespace and
    consecutive separators from each segment of the given path."""
    path_parts = path.split('/')
    simple_path = ''
    for part in path_parts:
        c = part.strip()
        if len(c):
            simple_path += '/' + c

    if not simple_path and path.find('/') > -1:
        simple_path = '/'
    return simple_path


def encode_path(path):
    """Converts a standard *nix/URL-style path to one which uses the '+'
    character for path separators. Before making this replacement, the path
    is simplified, using simplify_path(). For example, given the path /foo/bar/,
    this function will return +foo+bar.
    """
    simp_path = simplify_path(path)
    return simp_path.replace('/', '+')

def decode_path(path):
    """Performs the reverse of encode_path(), namely, replacing '+' with
    '/' in the given path."""
    return simplify_path(path.replace('+', '/'))
