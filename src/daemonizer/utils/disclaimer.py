"""Logic to define and get daemonizer disclaimer"""

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
