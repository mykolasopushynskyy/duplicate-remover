import os
import shutil


from model.model import ApplicationModel
from model.signals import AppSignals
from util.utils import get_hash, convert_size, get_min_image_date
from timeit import default_timer as timer
from pillow_heif import register_heif_opener

register_heif_opener()


class DuplicateScanner:
    def __init__(self, signals: AppSignals, model: ApplicationModel):
        self.signals = signals
        self.model = model

    # TODO Implement proper error handling for file scanning
    def scan_for_duplicates(self):
        results = []

        hash_lvl_1 = {}
        hash_lvl_2 = {}
        hash_lvl_3 = {}

        files_scanned = 0
        files_scanned_size = 0
        files_checked_v2 = 0
        files_checked_v3 = 0

        # excluded folders
        folders_to_exclude = [
            path
            for path, record in self.model.folders_to_scan().items()
            if record.get("exclude")
        ]
        folders_to_exclude.extend(self.model.get_system_folders_to_skip())
        folders_to_exclude.append(self.model.merge_folder())

        folders_to_scan = [
            path
            for path, record in self.model.folders_to_scan().items()
            if (not record.get("exclude"))
        ]

        start = timer()
        # form level one dict with keys of file size
        for directory in folders_to_scan:
            for root, dirs, files in os.walk(directory):
                if root in folders_to_exclude:
                    continue

                files = [
                    os.path.abspath(os.path.join(root, file))
                    for file in files
                    if file.lower().endswith(self.model.extensions_to_scan())
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

    def merge_results(self):
        parse_filename = self.model.pase_filename()
        actions = sum([1 + len(files) for files in self.model.duplicates])
        action = 0
        for i, files in enumerate(self.model.duplicates):
            old_file_path = str(min([file for file in files], key=len))
            old_file_dir, file_name = os.path.split(old_file_path)

            creation_date = get_min_image_date(files, parse_filename)

            new_file_dir = os.path.abspath(
                os.path.join(self.model.merge_folder(), str(creation_date.year))
            )
            new_file_path = os.path.abspath(os.path.join(new_file_dir, file_name))

            os.makedirs(new_file_dir, exist_ok=True)

            shutil.copy2(old_file_path, new_file_path)

            action += 1
            self.update_merge_status(new_file_path, "created", action, actions)

            if self.model.delete_originals():
                for file in files:
                    try:
                        os.remove(old_file_path)
                        action += 1
                        self.update_merge_status(file, "deleted", action, actions)
                    except OSError as e:
                        # If it fails, inform the user.
                        print("Error: %s - %s." % (e.filename, e.strerror))
                        continue

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
