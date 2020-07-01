class PageNotFoundError(Exception):  # what's Exception and RuntimeError ???
    pass


class MethodNotAllowed(Exception):
    pass


class UnknownPath(Exception):
    pass


class MissingData(Exception):
    pass
