import functools
import hashlib
import os
import re
import threading
from datetime import datetime

import PIL
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

# Define a tuple with common image file extensions
HOME = os.path.expanduser("~")
EXIF_TAG = 0x8769
EXIF_GENERATION_DATE_TAG = 0x9003
EXIF_CREATION_DATE_TAG = 0x0132
EXIF_DATE_FORMAT = "%Y:%m:%d %H:%M:%S"
CAMERAS_FILE_NAMING_PATTERNS = (
    # IMG_YYYYMMDD_HHMMSS.jpg or PANO_YYYYMMDD_HHMMSS.jpg or YYYYMMDD_HHMMSS.jpg
    (
        r"(\d{8})_(\d{6})",
        ["%Y%m%d%H%M%S", "%m%d%Y%H%M%S"],
    ),  # Common in smartphones and digital cameras
    # IMG_YYYYMMDD_HHMM.jpg or PANO_YYYYMMDD_HHMM.jpg or YYYYMMDD_HHMM.jpg (without seconds)
    (r"(\d{8})_(\d{4})", ["%Y%m%d%H%M"]),
    # YYYY_MM_DD_HH_MM_SS_mmm.jpg (some smartphones, action cameras)
    (r"(\d{4})_(\d{2})_(\d{2})_(\d{2})_(\d{2})_(\d{2})", ["%Y%m%d%H%M%S"]),
    # WP_YYYYMMDD_HHMMSS_Pro.jpg (Windows Phone)
    (r"(\d{8})_(\d{2})_(\d{2})_(\d{2})", ["%Y%m%d%H%M%S"]),
    # MMDDYYYYHHMMSS.jpg (some specialized cameras)
    (r"(\d{14})", ["%Y%m%d%H%M%S", "%m%d%Y%H%M%S"]),
    # YYYYMMDDHHMMSS.jpg (various digital cameras)
    (r"(\d{12})", ["%Y%m%d%H%M", "%m%d%Y%H%M"]),
    # YYYY-MM-DD description.jpg (some digital cameras, software)
    (r"(\d{4})-(\d{2})-(\d{2})", ["%Y%m%d"]),
    # MMDDYY_HHMM.jpg (some specialized cameras)
    (r"(\d{6})_(\d{4})", ["%m%d%y%H%M"]),
)


def short_path(abs_path: str):
    if abs_path is not None and abs_path.startswith(HOME):
        return abs_path.replace(HOME, "~", 1)
    else:
        return abs_path


def get_folder_size(path):
    """
    Calculate the total size of all files in a directory and its subdirectories.
    Args:
        path (str): The path of the directory.
    Returns:
        str: The total size in a human-readable format or "unknown" if the path is not found.
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
    file_size = os.path.getsize(filename)

    if quick_hash:
        start_chunk = file_object.read(chunk_size)
        hasher.update(start_chunk)

        if file_size > chunk_size:
            file_object.seek(-chunk_size, os.SEEK_END)
            end_chunk = file_object.read(chunk_size)
            hasher.update(end_chunk)
    else:
        for chunk in chunk_reader(file_object, chunk_size):
            hasher.update(chunk)

    file_object.close()
    return hasher.digest()


def get_exif_data(img_file: str):
    try:
        with Image.open(img_file) as im:
            exif = im.getexif()

            exif_dict = dict(exif)
            exif_dict.update(dict(exif.get_ifd(EXIF_TAG)))

            return exif_dict
    except PIL.UnidentifiedImageError:
        return None


def read_exif_date(exif: dict, date_key: int, default_value: datetime = None):
    if exif is None:
        return default_value

    date = str(exif.get(date_key))

    try:
        return datetime.strptime(date, EXIF_DATE_FORMAT)
    except ValueError as e:
        return default_value
    except TypeError as e:
        return default_value


def get_min_image_date(files, parse_filename=True):
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

    file_name_dt = (
        None if parse_filename is False else extract_datetime_from_filename(file)
    )
    file_st_a_dt = datetime.fromtimestamp(os_stat.st_atime)
    file_st_m_dt = datetime.fromtimestamp(os_stat.st_mtime)
    file_st_c_dt = datetime.fromtimestamp(os_stat.st_ctime)
    file_st_b_dt = datetime.fromtimestamp(os_stat.st_birthtime)
    exif_creation_date = read_exif_date(exif_data, EXIF_CREATION_DATE_TAG)
    exif_generation_date = read_exif_date(exif_data, EXIF_GENERATION_DATE_TAG)

    return min(
        [
            date
            for date in (
                file_name_dt,
                file_st_a_dt,
                file_st_m_dt,
                file_st_c_dt,
                file_st_b_dt,
                exif_creation_date,
                exif_generation_date,
            )
            if (date is not None)
        ],
        key=lambda d: d.year,
    )


def extract_datetime_from_filename(filename):
    for pattern, date_formats in CAMERAS_FILE_NAMING_PATTERNS:
        match = re.search(pattern, filename)
        if match is None:
            continue

        datetime_str = "".join(match.groups())

        for date_format in date_formats:
            try:
                parsed_datetime = datetime.strptime(datetime_str, date_format)
                if 1970 <= parsed_datetime.year <= datetime.now().year:
                    return parsed_datetime
                continue
            except ValueError:
                continue  # Continue to the next pattern if the current one fails to parse

    return None
