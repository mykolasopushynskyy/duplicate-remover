import operator
import os
import shutil
from datetime import datetime, time

import PIL
from PIL import Image, ExifTags
from model.model import ApplicationModel
from model.signals import AppSignals
from util.utils import get_hash, is_image_file, convert_size
from timeit import default_timer as timer
from pillow_heif import register_heif_opener

register_heif_opener()

EXIF_TAG = 0x8769
EXIF_GENERATION_DATE_TAG = 0x9003
EXIF_CREATION_DATE_TAG = 0x0132


def get_exif_data(img_file: str):
    with Image.open(img_file) as im:
        exif = im.getexif()

        exif_dict = dict(exif)
        exif_dict.update(dict(exif.get_ifd(EXIF_TAG)))

        return exif_dict


def get_creation_year_exif(files):
    # get created year
    created_year, file = min(
        [
            (datetime.fromtimestamp(os.path.getctime(file)).year, file)
            for file in files
        ],
        key=operator.itemgetter(1),
    )

    # get exif year
    try:
        exif_data = get_exif_data(file)
        creation_time = exif_data.get(EXIF_CREATION_DATE_TAG, created_year)
        generation_time = exif_data.get(EXIF_GENERATION_DATE_TAG, creation_time)
        image_generation_time = str(generation_time)
        return image_generation_time[0:4] if len(image_generation_time) > 4 else creation_time
    except PIL.UnidentifiedImageError:
        return created_year


class DuplicateScanner:
    def __init__(self, signals: AppSignals):
        self.signals = signals

    # TODO Implement proper error handling for file scanning
    def scan_for_duplicates(self, model: ApplicationModel):
        results = []

        hash_lvl_1 = {}
        hash_lvl_2 = {}
        hash_lvl_3 = {}

        files_scanned = 0
        files_scanned_size = 0
        files_checked_v2 = 0
        files_checked_v3 = 0

        skip_dir = model.merge_folder

        start = timer()
        # form level one dict with keys of file size
        for directory in model.folders_to_scan.keys():
            for root, dirs, files in os.walk(directory):
                if root == skip_dir:
                    continue

                files = [
                    os.path.abspath(os.path.join(root, file))
                    for file in files
                    if is_image_file(file)
                ]

                for file in files:
                    file_size = os.path.getsize(file)

                    # show program progress
                    files_scanned += 1
                    files_scanned_size += file_size
                    self.update_scan_status(
                        files_scanned,
                        files_scanned_size,
                        files_checked_v3,
                        files_checked_v2,
                    )

                    if file_size not in hash_lvl_1:
                        hash_lvl_1[file_size] = [file]
                    else:
                        hash_lvl_1[file_size].append(file)

        # form level two dict with keys of 1024 bytes hash and file size
        possible_max = sum(
            [len(files) for _, files in hash_lvl_1.items() if len(files) > 1]
        )
        for i, (size, files) in enumerate(hash_lvl_1.items()):
            # single file - no duplicates
            if len(files) == 1:
                results.append(files)
                continue

            for file in files:

                # show program progress
                files_checked_v2 += 1
                self.update_scan_status(
                    files_scanned, files_scanned_size, files_checked_v2, possible_max
                )

                small_hash = get_hash(file, quick_hash=True)
                if (small_hash, size) not in hash_lvl_2:
                    hash_lvl_2[(small_hash, size)] = [file]
                else:
                    hash_lvl_2[(small_hash, size)].append(file)

        # form level three dict with keys of 1024 bytes hash and file size and full hash
        for _, files in hash_lvl_2.items():
            # single file - no duplicates
            if len(files) == 1:
                results.append(files)
                continue

            for file in files:

                # show program progress
                files_checked_v3 += 1
                self.update_scan_status(
                    files_scanned,
                    files_scanned_size,
                    files_checked_v3,
                    files_checked_v2,
                )

                full_hash = get_hash(file, quick_hash=False)
                if full_hash not in hash_lvl_3:
                    hash_lvl_3[full_hash] = [file]
                else:
                    hash_lvl_3[full_hash].append(file)

        # add all duplicates to the result
        for _, files in hash_lvl_3.items():
            results.append(files)

        end = timer()
        num_od_duplicates = sum([(len(i) - 1) for i in results if len(i) > 1])
        size_to_save = sum(
            [os.path.getsize(i[0]) * (len(i) - 1) for i in results if len(i) > 1]
        )

        message = (
            f"Scanned {convert_size(files_scanned_size)} {files_scanned} files, "
            f"{num_od_duplicates} flies duplicated, "
            f"{convert_size(size_to_save)} can be saved, "
            f"{end - start:.2f}s passed"
        )
        self.signals.STATUS_MESSAGE_SET.emit(message, None)

        return results

    def merge_results(self, model: ApplicationModel):
        actions = sum([1 + len(files) for files in model.duplicates])
        action = 0
        for i, files in enumerate(model.duplicates):
            old_file_path = str(min([file for file in files], key=len))
            old_file_dir, file_name = os.path.split(old_file_path)

            creation_year = str(get_creation_year_exif(files))

            new_file_dir = os.path.abspath(
                os.path.join(model.merge_folder, creation_year)
            )
            new_file_path = os.path.abspath(os.path.join(new_file_dir, file_name))

            os.makedirs(new_file_dir, exist_ok=True)
            shutil.copy(old_file_path, new_file_path)
            action += 1
            self.update_merge_status(new_file_path, "created", action, actions)

            for file in files:
                print(f"delete {file}\n")
                action += 1
                self.update_merge_status(file, "deleted", action, actions)
        print("\n")
        self.signals.STATUS_MESSAGE_SET.emit("", None)

    def update_scan_status(self, files_scanned, files_scanned_size, value, max_value):
        message = (
            f"Scanned {convert_size(files_scanned_size)} {files_scanned} files, "
            f"checking {value} of {max_value}"
        )

        progress = 0 if (value == 0 or max_value == 0) else int(value / max_value * 100)
        self.signals.STATUS_MESSAGE_SET.emit(message, progress)

    def update_merge_status(self, file, action, value, max_value):
        message = f"File {file} {action}."

        progress = 0 if (value == 0 or max_value == 0) else int(value / max_value * 100)
        self.signals.STATUS_MESSAGE_SET.emit(message, progress)


if __name__ == "__main__":
    # get created year

    # filename = ["test.jpg", "test1.jpg", "test2.jpg", "test3.jpg", "test4.jpg", "test5.jpg", "test6.jpg", "test7.jpg"]
    filename = ["test10.heic"]
    for file in filename:
        created_year = datetime.fromtimestamp(os.stat(file).st_atime).year
        exif_data = get_exif_data(file)
        exif_date = str(exif_data.get(EXIF_CREATION_DATE_TAG, created_year))[0:4]
        print(f"{file} {exif_date}")
