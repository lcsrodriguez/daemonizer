"""Custom exceptions"""


class DaemonizerBaseError(Exception):
    """DaemonizerBaseError"""

    pass


class InvalidPIDError(DaemonizerBaseError):
    """InvalidPIDError"""

    pass


class InvalidPIDFileError(DaemonizerBaseError):
    """InvalidPIDFileError"""

    pass


class MissingPIDFileError(DaemonizerBaseError):
    """MissingPIDFileError"""

    pass


class AlreadyExistingPIDFileError(DaemonizerBaseError):
    """AlreadyExistingPIDFileError"""

    pass


class InvalidUNIXDistroError(DaemonizerBaseError):
    """InvalidUNIXDistroError"""

    pass
