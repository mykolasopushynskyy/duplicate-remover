from PySide6.QtCore import Slot

from model.signals import AppSignals


class ApplicationModel:

    def __init__(self, signals: AppSignals):
        # model data
        self.merge_folder = ""
        self.folders_to_scan = {}
        self.duplicates = None
        # TODO Add folders to skip in search
        # TODO Add some predefined folders to skip like system dirs, etc.

        # subscribe for config change
        signals.MODEL_LOAD.connect(self.from_configs)

    @Slot(dict)
    def from_configs(self, configs: dict):
        self.merge_folder = configs["merge_folder"]
        self.folders_to_scan = configs["folders_to_scan"]

    def to_configs(self):
        return dict(
            merge_folder=self.merge_folder, folders_to_scan=self.folders_to_scan
        )

    def set_merge_folder(self, path):
        self.merge_folder = path

    def add_folder_to_scan(self, record: dict):
        self.folders_to_scan[record["path"]] = record

    def remove_folder_to_scan(self, path):
        self.folders_to_scan.pop(path)

    def set_duplicates(self, duplicates):
        self.duplicates = duplicates
