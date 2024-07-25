import os

from controller.duplicate_scanner import DuplicateScanner
from controller.utils import get_folder_size, friendly_date, threaded

from configs import ConfigManager
from customtkinter import filedialog
from view.view import ApplicationView
from model.model import ApplicationModel, STATUS_MESSAGE_CHANGED, MERGE_FOLDER_CHANGE, CONFIGS_CHANGE, \
    FOLDERS_TO_SCAN_CHANGED, RESULTS_ARRIVED


class ApplicationController:
    def __init__(self,
                 config: ConfigManager,
                 model: ApplicationModel,
                 view: ApplicationView,
                 service: DuplicateScanner
                 ):
        super().__init__()

        self.config = config
        self.model = model
        self.view = view
        self.service = service

        toolbar = self.view.root.toolbar_panel
        status = self.view.root.status_panel
        folders = self.view.root.folders_to_scan
        results = self.view.root.results_panel

        # commands bindings
        toolbar.add_button.configure(command=self.browse_directory_to_scan)
        toolbar.select_folder_button.configure(command=self.browse_destination_directory)
        toolbar.scan_button.configure(command=self.scan_for_duplicates)
        folders.configure(remove_item_callback=self.remove_directory)

        # event bindings
        self.model.subscribe(STATUS_MESSAGE_CHANGED, status.set_message)
        self.model.subscribe(MERGE_FOLDER_CHANGE, toolbar.set_destination_directory)
        self.model.subscribe(FOLDERS_TO_SCAN_CHANGED, folders.update_folders)
        self.model.subscribe(RESULTS_ARRIVED, results.show_final_result)
        self.model.subscribe(CONFIGS_CHANGE, self.config.update_configs)
        self.model.subscribe(CONFIGS_CHANGE, self.config.update_configs)
        self.model.subscribe(CONFIGS_CHANGE, self.config.update_configs)
        # TODO Add event to update scan and scan status
        # TODO Add event to update scan results

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

    def remove_directory(self, path):
        self.model.remove_folder_to_scan(path)

    @threaded
    def scan_for_duplicates(self, *args):
        # TODO make sure we set everything correctly
        # TODO Consider to add validators for this
        # TODO Check if folders-to-scan are not subdirs of each other
        # TODO Skip
        duplicates = self.service.scan_for_duplicates()
        self.model.show_results(duplicates)
