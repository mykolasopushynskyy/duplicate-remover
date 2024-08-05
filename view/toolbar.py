import os

from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QToolBar,
    QWidget,
    QSizePolicy,
    QLabel,
    QFileDialog,
)

from configs import HOME_DIR
from model.signals import AppSignals
from util import icons
from util.utils import get_folder_size, friendly_date
from view.settings_window import SettingsWindow


class DRToolbar(QToolBar):
    def __init__(self, signals: AppSignals):
        QToolBar.__init__(self)
        self.signals = signals
        self.signals.MODEL_LOAD.connect(self.merge_folder_loaded)
        self.signals.MERGE_FOLDER_CHANGED.connect(self.merge_folder_changed)

        # Toolbar properties
        self.setMovable(False)
        self.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)

        # settings window
        self.settings = SettingsWindow(self.signals)

        # Add folder button
        self.add_folder_btn = QAction(icon=icons.plus(size=20), text="Add folder")
        self.add_folder_btn.triggered.connect(self.add_scan_folder)
        self.addAction(self.add_folder_btn)

        # Spacer
        self.spacer_1 = QWidget(self)
        self.spacer_1.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        self.spacer_1.setFixedWidth(370)
        self.spacer_1.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.addWidget(self.spacer_1)

        # Search duplicates
        self.search_duplicates_btn = QAction(icon=icons.search(size=20), text="Run search")
        self.search_duplicates_btn.triggered.connect(self.scan_pressed)
        self.addAction(self.search_duplicates_btn)

        # Merge duplicates
        self.merge_duplicates_btn = QAction(
            icon=icons.merge(size=20), text="Merge duplicates"
        )
        self.merge_duplicates_btn.triggered.connect(self.merge_pressed)
        self.addAction(self.merge_duplicates_btn)

        # Select folder button
        self.destination_folder_btn = QAction(
            icon=icons.open_folder(size=20), text="Destination folder"
        )
        self.destination_folder_btn.triggered.connect(self.select_destination_folder)
        self.addAction(self.destination_folder_btn)

        # Select folder label
        self.destination_folder_label = QLabel(text="Folder address")
        self.destination_folder_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        self.destination_folder_label.setFixedWidth(350)
        self.addWidget(self.destination_folder_label)

        # Spacer
        self.spacer_2 = QWidget(self)
        self.spacer_2.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.spacer_2.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.addWidget(self.spacer_2)

        # Settings button
        self.settings_btn = QAction(icon=icons.configs(size=20), text="Settings")
        self.settings_btn.triggered.connect(self.settings_pressed)
        self.addAction(self.settings_btn)

    @Slot(dict)
    def merge_folder_loaded(self, configs: dict):
        self.destination_folder_label.setText(configs["merge_folder"])

    @Slot(dict)
    def merge_folder_changed(self, directory: str):
        self.destination_folder_label.setText(directory)

    @Slot(dict)
    def select_destination_folder(self):
        directory = QFileDialog.getExistingDirectory(
            self, caption="Select destination directory", dir=HOME_DIR
        )
        self.signals.MERGE_FOLDER_CHANGED.emit(directory)

    @Slot(dict)
    def add_scan_folder(self):
        directory = QFileDialog.getExistingDirectory(
            self, caption="Select folder to scan", dir=HOME_DIR
        )
        if directory is not None and len(directory) > 0:
            size = get_folder_size(directory)
            date = friendly_date(os.stat(directory).st_ctime)
            directory_record = dict(path=directory, size=size, date=date)

            self.signals.ADD_FOLDER.emit(directory_record)

    @Slot()
    def scan_pressed(self):
        self.signals.SCAN_PRESSED.emit()

    @Slot()
    def merge_pressed(self):
        self.signals.MERGE_PRESSED.emit()

    @Slot()
    def settings_pressed(self):
        if self.settings.isVisible():
            self.settings.hide()
        else:
            self.settings.show()
