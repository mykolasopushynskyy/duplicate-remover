import os

from controller.utils import get_hash, is_image_file, convert_size
from model.model import ApplicationModel


class DuplicateScanner:
    def __init__(self, model: ApplicationModel):
        self.model = model

    def scan_for_duplicates(self):
        results = []

        hash_lvl_1 = {}
        hash_lvl_2 = {}
        hash_lvl_3 = {}

        files_scanned = 0
        files_scanned_size = 0
        files_checked_v2 = 0
        files_checked_v3 = 0

        skip_dir = self.model.merge_folder

        # form level one dict with keys of file size
        for directory in self.model.folders_to_scan.keys():
            for root, dirs, files in os.walk(directory):
                if root == skip_dir:
                    continue

                files = [os.path.abspath(os.path.join(root, file)) for file in files if is_image_file(file)]

                for file in files:
                    file_size = os.path.getsize(file)

                    # show program progress
                    files_scanned += 1
                    files_scanned_size += file_size
                    self.update_status(files_checked_v2, files_checked_v3, files_scanned, files_scanned_size)

                    if file_size not in hash_lvl_1:
                        hash_lvl_1[file_size] = [file]
                    else:
                        hash_lvl_1[file_size].append(file)

        # form level two dict with keys of 1024 bytes hash and file size
        for size, files in hash_lvl_1.items():
            # single file - no duplicates
            if len(files) == 1:
                results.append(files)
                continue

            for file in files:

                # show program progress
                files_checked_v2 += 1
                self.update_status(files_checked_v2, files_checked_v3, files_scanned, files_scanned_size)

                small_hash = get_hash(file, first_chunk_only=True)
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
                self.update_status(files_checked_v2, files_checked_v3, files_scanned, files_scanned_size)

                full_hash = get_hash(file, first_chunk_only=False)
                if full_hash not in hash_lvl_3:
                    hash_lvl_3[full_hash] = [file]
                else:
                    hash_lvl_3[full_hash].append(file)

        # add all duplicates to the result
        for _, files in hash_lvl_3.items():
            results.append(files)

        size_to_save = sum([os.path.getsize(i[0]) * (len(i) - 1) for i in results if len(i) > 1])

        self.model.set_status(f"Scanned {convert_size(files_scanned_size)} {files_scanned} files, {convert_size(size_to_save)} can be saved")

        return results

    def update_status(self, files_checked_v2, files_checked_v3, files_scanned, files_scanned_size):
        self.model.set_status(
            f"Scanned {convert_size(files_scanned_size)} {files_scanned} files, checking {files_checked_v2}, additional check {files_checked_v3}")
