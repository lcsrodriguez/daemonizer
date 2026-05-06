"""Utils to check OS processes"""

from psutil import pid_exists


def check_process_status(pid_: int) -> bool:
    """
    Function to check if the process exists
    :param pid_: PID of the process
    :type pid_: int
    :return: True if exists, False if not
    :rtype: bool
    """
    return pid_exists(pid=pid_)


def is_active_process(pid_: int) -> bool:
    """
    Function to check if the process exists
    :param pid_: PID of the process
    :type pid_: int
    :return: True if exists, False otherwise
    :rtype: bool
    """
    return check_process_status(pid_=pid_)
