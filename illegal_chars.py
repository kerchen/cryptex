import re

ILLEGAL_NAME_CHARS = [u"'", u"\\\\", u"/"]
ILLEGAL_CHAR_RE = re.compile("[" +u"".join(ILLEGAL_NAME_CHARS) + "]")