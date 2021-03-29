import datetime
import time
from types import FunctionType
from typing import Any, Callable, Sequence


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


def keep_retrying_on_specific_error(error_substr: str, sleep_seconds: int, func: Callable, *args, **kwargs) -> Any:
    """
    Calls the provided func with its args and kwargs as long as an exception is
    raised containing the error_substr.
    Sleeps for the specified number of seconds between each call.
    If an error occurs and the error_substr is not part of the error message, it
    is allowed to raise.

    Args:
        error_substr: Specific error string on which to retry 
        sleep_seconds: Number of seconds to sleep between invocations
        func: Function to invoke with args and kwargs. Its return values will be fowarded to the caller.
    
    Returns:
        Whatever the provided function ought to return.
    """
    while True:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if is_substr(str(e), error_substr, ignorecase=True):
                time.sleep(sleep_seconds)
            else:
                raise


def is_substr(string: str, substr: str, ignorecase=False) -> bool:
    """
    Tests whether a string has a given substring. Ignore case parameter
    for flexibility.

    Args:
        string: Full string
        substr: string segment
        ignorecase (bool, optional): Whether to ignore case. Defaults to False.

    Returns:
        True or False
    """
    if ignorecase:
        return substr.lower() in string.lower()
    else:
        return substr in string


def filter_by_glob(collection: Sequence[Any], pattern: str) -> Sequence[Any]:
    """
    Returns a filtered collection based on which
    items match the provided string pattern.

    Args:
        collection: Sequence to filter on
        pattern: String, optionally containing a wildcard '*' character

    Returns:
        Subset of items in the collection that match the glob pattern
    """
    parts = pattern.split("*")
    beginning = parts[0]
    ending = parts[1]

    new_list = []

    for item in collection:
        item_as_str = str(item)
        if item_as_str.startswith(beginning) and item_as_str.endswith(ending):
            new_list.append(item)
    return new_list