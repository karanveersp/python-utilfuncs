import datetime
import time


def get_timestamp(date_only=False):
    """
    Returns the timestamp string for current day
    Args:
        date_only (bool, optional): True or False
    Returns:
        Timestamp (str)
    """
    if date_only:
        return datetime.datetime.now().strftime("%Y%m%d")
    else:
        return datetime.datetime.now().strftime("%Y%m%d_%H%M")


def keep_retrying_on_specific_error(error_substr, sleep_seconds, func, *args, **kwargs):
    while True:
        try:
            func(*args, **kwargs)
            break
        except Exception as e:
            if is_substr(str(e), error_substr, ignorecase=True):
                time.sleep(sleep_seconds)
            else:
                raise


def is_substr(string, substr, ignorecase=False):
    if ignorecase:
        return substr.lower() in string.lower()
    else:
        return substr in string
