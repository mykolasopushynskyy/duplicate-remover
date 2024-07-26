import os
import model.events as events
from controller.duplicate_scanner import DuplicateScanner
from util.utils import get_folder_size, friendly_date, threaded, short_path

from customtkinter import filedialog
from view.view import ApplicationView
from model.model import ApplicationModel, PubSubBroker


class ApplicationController:
    def __init__(
        self,
        pubsub: PubSubBroker,
        model: ApplicationModel,
        view: ApplicationView,
        service: DuplicateScanner,
    ):
        super().__init__()

        # app
        self.pubsub = pubsub
        self.model = model
        self.view = view
        self.service = service

        # subscribe to events bindings
        self.pubsub.subscribe(events.ADD_FOLDER_PRESSED, self.add_folder)
        self.pubsub.subscribe(events.REMOVE_FOLDER_PRESSED, self.remove_folder)
        self.pubsub.subscribe(events.SELECT_FOLDER_PRESSED, self.add_destination)
        self.pubsub.subscribe(events.SCAN_DUPLICATES_PRESSED, self.scan)

    @threaded
    def add_folder(self, *args):
        home = os.path.expanduser("~")
        directory = filedialog.askdirectory(initialdir=home, parent=self.view)

        if os.path.isdir(directory):
            size = get_folder_size(directory)
            date = friendly_date(os.stat(directory).st_ctime)
            directory_record = dict(path=directory, size=size, date=date)
            # TODO make sure we dont add subfolders of folder to scan
            # TODO Consider to add validators for this
            self.model.add_folder_to_scan(directory_record)
            self.pubsub.publish(
                events.FOLDERS_TO_SCAN_CHANGED, self.model.folders_to_scan
            )
            self.pubsub.publish(events.CONFIGS_CHANGE, self.model)

    def add_destination(self, *args):
        home = os.path.expanduser("~")
        directory = filedialog.askdirectory(initialdir=home, parent=self.view)
        if directory is not None and os.path.isdir(directory):
            self.model.set_merge_folder(directory)
            self.pubsub.publish(events.MERGE_FOLDER_CHANGED, directory)
            self.pubsub.publish(events.CONFIGS_CHANGE, self.model)

    def remove_folder(self, path):
        self.model.remove_folder_to_scan(path)
        self.pubsub.publish(events.FOLDERS_TO_SCAN_CHANGED, self.model.folders_to_scan)
        self.pubsub.publish(events.CONFIGS_CHANGE, self.model)

    @threaded
    def scan(self, *args):
        # TODO make sure we set everything correctly
        # TODO Consider to add validators for this
        # TODO Check if folders-to-scan are not subdirs of each other
        # TODO Skip

        self.pubsub.publish(events.SCANNING, True)
        result = self.service.scan_for_duplicates()

        # prepare view data
        duplicates = [i for i in result if len(i) > 1]
        duplicates.sort(key=len, reverse=True)
        duplicates = [[short_path(ap) for ap in entries] for entries in duplicates]

        self.pubsub.publish(events.RESULTS_ARRIVED, duplicates)
