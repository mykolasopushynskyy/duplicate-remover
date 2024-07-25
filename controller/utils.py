import functools
import os
import threading
from datetime import datetime


def get_folder_size(path):
    """
    Calculate the total size of all files in a directory and its subdirectories.
    Args:
        path (str): The path of the directory.
    Returns:
        str: The total size in a human-readable format or 'unknown' if the path is not found.
    """
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
    except FileNotFoundError as e:
        return "unknown"
    except PermissionError as e:
        return "unknown"
    return convert_size(total_size)


def convert_size(size):
    """
    Convert a size in bytes to a human-readable format.
    Args:
        size (int): The size in bytes.
    Returns:
        str: The size in a human-readable format.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


def friendly_date(timestamp, date_format="%Y-%m-%d %H:%M:%S"):
    """
    Convert a timestamp to a human-readable date format.
    Args:
        timestamp (float): The timestamp to convert.
        date_format (str): The format string to use for the date.
    Returns:
        str: The formatted date.
    """
    return datetime.fromtimestamp(timestamp).strftime(date_format)


def threaded(func):
    """Decorator to automatically launch a function in a thread"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Launch the original function in a thread
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper
