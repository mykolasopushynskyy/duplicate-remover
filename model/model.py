import os
import platform

from configs import (
    ConfigManager,
    CONFIG_FILE_NAME,
    SYSTEM_FOLDERS_TO_SKIP,
    MERGE_FOLDER,
    FOLDERS_TO_SCAN,
    EXTENSIONS_TO_SCAN,
    PARSE_DATE_FROM_FILENAME,
    DELETE_ORIGINAL_FILES, IMAGE_FILENAME_FORMAT,
)
from model.signals import AppSignals


class ApplicationModel(ConfigManager):

    def __init__(self, signals: AppSignals, config_file: str = CONFIG_FILE_NAME):
        ConfigManager.__init__(self, signals, config_file)
        # model data
        self.duplicates = []

    def set_duplicates(self, duplicates):
        self.duplicates = duplicates

    def delete_originals(self):
        return self.get(DELETE_ORIGINAL_FILES)

    def folders_to_scan(self):
        return self.get(FOLDERS_TO_SCAN)

    def merge_folder(self):
        return self.get(MERGE_FOLDER)

    def extensions_to_scan(self):
        return tuple(self.get(EXTENSIONS_TO_SCAN).split(" "))

    def pase_filename(self):
        return self.get(PARSE_DATE_FROM_FILENAME)

    def image_filename_format(self):
        return self.get(IMAGE_FILENAME_FORMAT)

    def get_system_folders_to_skip(self):
        system = platform.system()
        if platform == "Windows":
            sys_drive = os.getenv("SystemDrive")
            return [
                sys_drive + value for value in self.get(SYSTEM_FOLDERS_TO_SKIP)[system]
            ]
        else:
            return self.get(SYSTEM_FOLDERS_TO_SKIP)[system]
