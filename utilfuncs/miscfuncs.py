import datetime


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

