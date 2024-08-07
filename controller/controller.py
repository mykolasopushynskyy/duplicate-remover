from PySide6.QtCore import Slot

from configs import FOLDERS_TO_SCAN
from controller.ds_service import DuplicateScanner
from model.signals import AppSignals
from util.utils import short_path, threaded

from model.model import ApplicationModel


class ApplicationController:
    def __init__(
        self,
        signals: AppSignals,
        model: ApplicationModel,
        service: DuplicateScanner,
    ):
        super().__init__()

        # app
        self.signals = signals
        self.model = model
        self.service = service

        # subscribe to events bindings
        self.signals.ADD_FOLDER_PRESSED.connect(self.add_folder)
        self.signals.REMOVE_FOLDER_PRESSED.connect(self.remove_folder)
        self.signals.SCAN_PRESSED.connect(self.scan)
        self.signals.MERGE_PRESSED.connect(self.merge_images)

    @Slot(None)
    def add_folder(self, record):
        # TODO make sure we dont add subfolders of folder to scan
        # TODO Consider to add validators for this
        folders = self.model.folders_to_scan()
        folders[record["path"]] = record
        self.signals.CONFIGS_CHANGE.emit({FOLDERS_TO_SCAN: folders})

    @Slot(str)
    def remove_folder(self, path):
        folders = self.model.folders_to_scan()
        folders.pop(path)
        self.signals.CONFIGS_CHANGE.emit({FOLDERS_TO_SCAN: folders})

    # @threaded
    @Slot(None)
    @threaded
    def scan(self):
        # TODO make sure we set everything correctly
        # TODO Consider to add validators for this
        # TODO Check if folders-to-scan are not sub-dirs of each other
        # TODO Skip
        self.model.set_duplicates(None)
        self.signals.SCANNING.emit(True)
        result = self.service.scan_for_duplicates()

        # prepare view data
        duplicates = [i for i in result]
        duplicates.sort(key=len, reverse=True)
        duplicates = [[short_path(ap) for ap in entries] for entries in duplicates]

        self.model.set_duplicates(result)
        self.signals.RESULTS_ARRIVED.emit(duplicates)

    @Slot(None)
    @threaded
    def merge_images(self):
        # TODO make sure we set everything correctly
        # TODO Consider to add validators for this
        # TODO Check if folders-to-scan are not subdirs of each other
        # TODO Skip
        if len(self.model.duplicates) == 0:
            return

        self.service.merge_results()
