from datetime import datetime
import time


def convert_to_unix(date_str, format="%d-%m-%Y %H:%M:%S"):
    """
    Convert a datetime string to a Unix timestamp using the specified format.

    Args:
        date_str (str): Datetime string.
        format (str): Format of the datetime string (default is '%d-%m-%Y %H:%M:%S').

    Returns:
        int: Unix timestamp.
    """
    try:
        formatted_time = datetime.strptime(date_str, format)
    except ValueError:
        format_no_time = "%d-%m-%Y"
        formatted_time = datetime.strptime(date_str, format_no_time)

    unix_time = int(time.mktime(formatted_time.timetuple()))
    return unix_time