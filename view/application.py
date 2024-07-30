from typing import Sequence

from PySide6.QtWidgets import QApplication

import configs
from model.signals import AppSignals
from view.main_window import DRQMainWindow


class DRQApplication(QApplication):
    def __init__(self, signals: AppSignals, args: Sequence[str]):
        super().__init__(args)
        self.setApplicationName(configs.APP_NAME)

        # Window creation
        self.window = DRQMainWindow(signals)
        self.window.show()
