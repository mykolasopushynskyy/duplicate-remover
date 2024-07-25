import os

from controller.utils import get_folder_size, friendly_date
from parallel import threaded

from configs import ConfigManager
from customtkinter import filedialog
from view.view import ApplicationView
from model.model import ApplicationModel, STATUS_MESSAGE_CHANGED, MERGE_FOLDER_CHANGE, CONFIGS_CHANGE, \
    FOLDERS_TO_SCAN_CHANGED


class ApplicationController:
    def __init__(self, config: ConfigManager, model: ApplicationModel, view: ApplicationView):
        super().__init__()

        self.config = config
        self.model = model
        self.view = view

        toolbar = self.view.root.toolbar_panel
        status = self.view.root.status_panel
        folders = self.view.root.folders_to_scan

        # commands bindings
        toolbar.add_button.configure(command=self.browse_directory_to_scan)
        toolbar.select_folder_button.configure(command=self.browse_destination_directory)
        folders.configure(remove_item_callback=self.remove_directory)

        # event bindings
        self.model.add_event_listener(STATUS_MESSAGE_CHANGED, status.set_message)
        self.model.add_event_listener(MERGE_FOLDER_CHANGE, toolbar.set_destination_directory)
        self.model.add_event_listener(FOLDERS_TO_SCAN_CHANGED, folders.update_folders)
        self.model.add_event_listener(CONFIGS_CHANGE, self.config.update_configs)

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
            self.model.add_folder_to_scan(directory_record)

    @threaded
    def browse_destination_directory(self, *args):
        home = os.path.expanduser("~")
        directory = filedialog.askdirectory(initialdir=home, parent=self.view)
        if directory is not None and os.path.isdir(directory):
            self.model.set_merge_folder(directory)

    @threaded
    def remove_directory(self, path):
        self.model.remove_folder_to_scan(path)
