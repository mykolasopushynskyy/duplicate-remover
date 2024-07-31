from PySide6.QtCore import Slot

from controller.duplicate_scanner import DuplicateScanner
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

        self.signals.ADD_FOLDER.connect(self.add_folder)
        self.signals.REMOVE_FOLDER.connect(self.remove_folder)
        self.signals.SCAN_PRESSED.connect(self.scan)

    # @threaded
    @Slot(None)
    def add_folder(self, directory_record):

        # TODO make sure we dont add subfolders of folder to scan
        # TODO Consider to add validators for this
        self.model.add_folder_to_scan(directory_record)
        self.signals.FOLDERS_TO_SCAN_CHANGED.emit(self.model.folders_to_scan)
        self.signals.CONFIGS_CHANGE.emit(self.model.folders_to_scan)

    @Slot(str)
    def remove_folder(self, path):
        self.model.remove_folder_to_scan(path)
        self.signals.FOLDERS_TO_SCAN_CHANGED.emit(self.model.folders_to_scan)
        self.signals.CONFIGS_CHANGE.emit(self.model.folders_to_scan)

    # @threaded
    @Slot(None)
    @threaded
    def scan(self):
        # TODO make sure we set everything correctly
        # TODO Consider to add validators for this
        # TODO Check if folders-to-scan are not subdirs of each other
        # TODO Skip
        self.model.set_duplicates(None)
        self.signals.SCANNING.emit(True)
        result = self.service.scan_for_duplicates()

        # prepare view data
        duplicates = [i for i in result if len(i) > 1]
        duplicates.sort(key=len, reverse=True)
        duplicates = [[short_path(ap) for ap in entries] for entries in duplicates]

        self.signals.RESULTS_ARRIVED.emit(duplicates)
