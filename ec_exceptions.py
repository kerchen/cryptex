class ECException(Exception):
    pass


class ECDuplicateException(ECException):
    pass


class ECNotFoundException(ECException):
    pass


class ECNaughtyCharacterException(ECException):
    pass


class ECBadPathException(ECException):
    pass