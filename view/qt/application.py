from typing import Sequence

from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QApplication, QVBoxLayout, QLineEdit, QPushButton, QMainWindow

import configs
from model.signals import AppSignals
from view.qt.main_window import DRQMainWindow


class DRQApplication(QApplication):
    def __init__(self, signals: AppSignals, args: Sequence[str]):
        super().__init__(args)
        self.setApplicationName(configs.APP_NAME)

        # Window creation
        self.window = DRQMainWindow(signals)
        self.window.show()
