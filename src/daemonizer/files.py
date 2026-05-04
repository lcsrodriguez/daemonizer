"""Generic path names defined to be used in the entire project"""

from pathlib import Path

from platformdirs import user_cache_path, user_data_path, user_log_path

from daemonizer.constants import APP_NAME, APP_VERSION

CACHE_DIR: Path = user_cache_path(appname=APP_NAME, version=APP_VERSION)
LOG_DIR: Path = user_log_path(appname=APP_NAME, version=APP_VERSION)
DATA_DIR: Path = user_data_path(appname=APP_NAME, version=APP_VERSION)
