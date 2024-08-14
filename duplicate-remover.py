#!/usr/bin/env python3
import sys

from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QStyleFactory

from controller.controller import ApplicationController
from controller.ds_service import DuplicateScanner
from model.model import ApplicationModel
from model.signals import AppSignals

from view.view import DRQApplication
import sys


class DuplicateRemover:
    def __init__(self):
        super().__init__()
        self.signals = AppSignals()
        self.model = ApplicationModel(self.signals)
        self.app = DRQApplication(self.signals, sys.argv)
        self.service = DuplicateScanner(self.signals, self.model)
        self.controller = ApplicationController(self.signals, self.model, self.service)

    def load_application_state(self):
        # publish data from settings
        self.signals.CONFIGS_LOAD.emit(self.model.configs)
        self.signals.PROCESSING.emit(False)
        self.signals.RESULTS_ARRIVED.emit([])

    def start(self):
        self.load_application_state()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    duplicate_remover = DuplicateRemover()
    duplicate_remover.start()
