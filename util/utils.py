import functools
import hashlib
import os
import threading
from datetime import datetime

# Define a tuple with common image file extensions
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".heic")
HOME = os.path.expanduser("~")


def short_path(abs_path: str):
    if abs_path.startswith(HOME):
        return abs_path.replace(HOME, "~", 1)
    else:
        return abs_path


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


def chunk_reader(file, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            return
        yield chunk


def get_hash(filename, quick_hash=False, chunk_size=1024, hash_alg=hashlib.sha1):
    hasher = hash_alg()
    file_object = open(filename, 'rb')

    if quick_hash:
        start_chunk = file_object.read(chunk_size)
        hasher.update(start_chunk)

        file_object.seek(-chunk_size, os.SEEK_END)
        end_chunk = file_object.read(chunk_size)
        hasher.update(end_chunk)
    else:
        for chunk in chunk_reader(file_object):
            hasher.update(chunk)

    file_object.close()
    return hasher.digest()


def is_image_file(filename):
    """
    Check if a file is an image based on its extension.
    Args:
        filename (str): The name of the file to check.
    Returns:
        bool: True if the file is an image, False otherwise.
    """
    return filename.lower().endswith(IMAGE_EXTENSIONS)
