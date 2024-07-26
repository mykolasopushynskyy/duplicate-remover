import os

from controller.duplicate_scanner import DuplicateScanner
from controller.utils import get_folder_size, friendly_date, threaded

from configs import ConfigManager
from customtkinter import filedialog
from view.view import ApplicationView
from model.model import ApplicationModel, Topic, PubSubBroker


class ApplicationController:
    def __init__(self,
                 pubsub: PubSubBroker,
                 config: ConfigManager,
                 model: ApplicationModel,
                 view: ApplicationView,
                 service: DuplicateScanner
                 ):
        super().__init__()

        # app
        self.pubsub = pubsub
        self.config = config
        self.model = model
        self.view = view
        self.service = service

        # subscribe to events bindings
        self.pubsub.subscribe(Topic.ADD_FOLDER_PRESSED, self.browse_directory_to_scan)
        self.pubsub.subscribe(Topic.SELECT_FOLDER_PRESSED, self.browse_destination_directory)
        self.pubsub.subscribe(Topic.SCAN_DUPLICATES_PRESSED, self.scan_for_duplicates)
        self.pubsub.subscribe(Topic.REMOVE_FOLDER_PRESSED, self.remove_directory_to_scan)

        # restore state
        self.update_model()

    @threaded
    def update_model(self):
        # restore state
        self.model.update_model(config_manager=self.config)

    @threaded
    def browse_directory_to_scan(self, *args):
        home = os.path.expanduser("~")
        directory = filedialog.askdirectory(initialdir=home, parent=self.view)

        if os.path.isdir(directory):
            size = get_folder_size(directory)
            date = friendly_date(os.stat(directory).st_ctime)
            directory_record = dict(path=directory,
                                    size=size,
                                    date=date)
            # TODO make sure we dont add subfolders of folder to scan
            # TODO Consider to add validators for this
            self.model.add_folder_to_scan(directory_record)

    def browse_destination_directory(self, *args):
        home = os.path.expanduser("~")
        directory = filedialog.askdirectory(initialdir=home, parent=self.view)
        if directory is not None and os.path.isdir(directory):
            self.model.set_merge_folder(directory)

    def remove_directory_to_scan(self, path):
        self.model.remove_folder_to_scan(path)

    @threaded
    def scan_for_duplicates(self, *args):
        # TODO make sure we set everything correctly
        # TODO Consider to add validators for this
        # TODO Check if folders-to-scan are not subdirs of each other
        # TODO Skip
        duplicates = self.service.scan_for_duplicates()
        self.model.show_results(duplicates)
