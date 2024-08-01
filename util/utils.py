import functools
import hashlib
import os
import threading
from datetime import datetime

import PIL
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()


# Define a tuple with common image file extensions
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".heic")
HOME = os.path.expanduser("~")
EXIF_TAG = 0x8769
EXIF_GENERATION_DATE_TAG = 0x9003
EXIF_CREATION_DATE_TAG = 0x0132
EXIF_DATE_FORMAT = "%Y:%m:%d %H:%M:%S"


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
        for dir_path, dir_names, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dir_path, f)
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
    for unit in ["B", "KB", "MB", "GB", "TB"]:
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
    file_object = open(filename, "rb")

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


def get_exif_data(img_file: str):
    try:
        with Image.open(img_file) as im:
            exif = im.getexif()

            exif_dict = dict(exif)
            exif_dict.update(dict(exif.get_ifd(EXIF_TAG)))

            return exif_dict
    except PIL.UnidentifiedImageError:
        return None


def read_exif_date(exif: dict, key: int, default_value: datetime = None):
    if exif is None:
        return default_value

    date = str(exif.get(key))

    try:
        return datetime.strptime(date, EXIF_DATE_FORMAT)
    except ValueError as e:
        return default_value
    except TypeError as e:
        return default_value


def get_min_creation_date(files):
    # get created year
    file = str(
        min(
            [file for file in files],
            key=len,
        )
    )

    # get all file dates
    exif_data = get_exif_data(file)
    os_stat = os.stat(file)

    file_st_a_time = datetime.fromtimestamp(os_stat.st_atime)
    file_st_m_time = datetime.fromtimestamp(os_stat.st_mtime)
    file_st_c_time = datetime.fromtimestamp(os_stat.st_ctime)
    file_st_b_time = datetime.fromtimestamp(os_stat.st_birthtime)
    exif_creation_date = read_exif_date(exif_data, EXIF_CREATION_DATE_TAG)
    exif_generation_date = read_exif_date(exif_data, EXIF_GENERATION_DATE_TAG)

    return min(
        [
            date
            for date in (
                file_st_a_time,
                file_st_m_time,
                file_st_c_time,
                file_st_b_time,
                exif_creation_date,
                exif_generation_date,
            )
            if (date is not None)
        ],
        key=lambda d: d.year,
    )
