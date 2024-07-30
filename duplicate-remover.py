import sys

from controller.controller import ApplicationController
from configs import ConfigManager
from controller.duplicate_scanner import DuplicateScanner
from model.model import ApplicationModel
from model.signals import AppSignals

from view.application import DRQApplication


class DuplicateRemover:
    def __init__(self):
        super().__init__()

        self.signals = AppSignals()
        self.model = ApplicationModel(self.signals)
        self.config = ConfigManager(self.signals)
        self.view = DRQApplication(self.signals, sys.argv)
        self.service = DuplicateScanner(self.signals, self.model)
        self.controller = ApplicationController(self.signals, self.model, self.service)

        self.load_application_state()

    def load_application_state(self):
        # publish data from settings
        self.signals.MODEL_LOAD.emit(
            dict(
                merge_folder=self.config.get("merge_folder", default=""),
                folders_to_scan=self.config.get("folders_to_scan", default={}),
            )
        )

    def start(self):
        # self.load_application_state()
        sys.exit(self.view.exec())


if __name__ == "__main__":
    duplicate_remover = DuplicateRemover()
    duplicate_remover.start()
