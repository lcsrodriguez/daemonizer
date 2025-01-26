class DaemonizerBaseError(Exception):
    """DaemonizerBaseError"""

    pass


class InvalidPIDError(DaemonizerBaseError):
    """InvalidPIDError"""

    pass


class MissingPIDFileError(DaemonizerBaseError):
    """MissingPIDFileError"""

    pass


class InvalidUNIXDistroError(DaemonizerBaseError):
    """InvalidUNIXDistroError"""

    pass
