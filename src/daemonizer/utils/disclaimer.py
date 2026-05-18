"""Logic to define and get daemonizer disclaimer"""

from daemonizer.constants import DAEMONIZER_DISCLAIMER_ENV_VAR
from daemonizer.utils.environ import get_env_var
from daemonizer.utils.logs import get_logger

logger = get_logger(__name__)


DISCLAIMER: str = """Running a daemon from unknown source or with undisclosed code base is NOT recommended.
Always ensure the running daemons can be trusted on your machine.
daemonizer does NOT check beforehand whether the daemon's logic is safe or not.
"""


def get_disclaimer() -> str:
    """
    Return the disclaimer string
    :return: Entire disclaimer
    :rtype: str
    """
    return DISCLAIMER


def handle_disclaimer(user_input: bool = True) -> bool:
    """
    Function to handle disclaimer display on SDK or CLI
    :param user_input: User input (boolean): True -> disclaimer displayed
    :type user_input: bool
    :return: True if disclaimer must be displayed, False otherwise
    :rtype: bool
    """

    # Handling environment variable input
    try:
        env_input: bool | None = bool(int(get_env_var(DAEMONIZER_DISCLAIMER_ENV_VAR)))
    except (KeyError, Exception):
        # logger.error(exc_)
        env_input = None  # default value set to True

    if (
        env_input is None
    ):  # The env input is the strongest choice here. It overrides everything
        return user_input
    else:
        return env_input
    # return False
