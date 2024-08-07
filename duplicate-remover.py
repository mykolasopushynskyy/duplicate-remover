#!/usr/bin/env python3
import sys


from controller.controller import ApplicationController
from configs import ConfigManager
from controller.ds_service import DuplicateScanner
from model.model import ApplicationModel
from model.signals import AppSignals

from view.view import DRQApplication


class DuplicateRemover:
    def __init__(self):
        super().__init__()
        self.signals = AppSignals()
        self.config_manager = ConfigManager(self.signals)
        self.model = ApplicationModel(self.signals)
        self.view = DRQApplication(self.signals, sys.argv)
        self.service = DuplicateScanner(self.signals, self.config_manager)
        self.controller = ApplicationController(self.signals, self.model, self.service)

    def load_application_state(self):
        # publish data from settings
        self.signals.MODEL_LOAD.emit(self.config_manager.configs)

    def start(self):
        self.load_application_state()
        sys.exit(self.view.exec())


if __name__ == "__main__":
    duplicate_remover = DuplicateRemover()
    duplicate_remover.start()
