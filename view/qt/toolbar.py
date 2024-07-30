import os

from PySide6.QtCore import Slot, QPoint, Qt, QSize, QLine
from PySide6.QtGui import QAction, QIcon, QImage, QPaintEvent, QPainter
from PySide6.QtWidgets import QMainWindow, QToolBar, QPushButton, QToolButton, QWidget, QSizePolicy, QLabel, QStyle, \
    QSplitter, QStyleOption, QStyleOptionToolBar, QFileDialog

from configs import HOME_DIR
from model.signals import AppSignals
from util import icons
from util.utils import get_folder_size, friendly_date


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

        # Add folder button
        self.add_folder = QAction(icon=icons.plus(size=20), text="Add folder")
        self.add_folder.triggered.connect(self.add_scan_folder)
        self.addAction(self.add_folder)

        # Spacer
        self.spacer = QWidget(self)
        self.spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.spacer.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.addWidget(self.spacer)

        # Select duplicates
        self.search_duplicates = QAction(icon=icons.run(size=20), text="Run search")
        self.search_duplicates.triggered.connect(lambda: print("Search duplicates"))
        self.addAction(self.search_duplicates)

        # Select folder button
        self.destination_folder = QAction(icon=icons.open_folder(size=20), text="Destination folder")
        self.destination_folder.triggered.connect(self.select_destination_folder)
        self.addAction(self.destination_folder)

        # Select folder label
        self.destination_folder_label = QLabel(text="Folder address")
        self.destination_folder_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.destination_folder_label.setFixedWidth(400)
        self.addWidget(self.destination_folder_label)

        # Settings button
        self.settings = QAction(icon=icons.configs(size=20), text="Settings")
        self.settings.triggered.connect(lambda: print("Settings"))
        self.addAction(self.settings)

    @Slot(dict)
    def merge_folder_loaded(self, configs: dict):
        self.destination_folder_label.setText(configs["merge_folder"])

    @Slot(dict)
    def merge_folder_changed(self, directory: str):
        self.destination_folder_label.setText(directory)

    @Slot(dict)
    def select_destination_folder(self):
        directory = QFileDialog.getExistingDirectory(self, caption="Select destination directory", dir=HOME_DIR)
        self.signals.MERGE_FOLDER_CHANGED.emit(directory)

    @Slot(dict)
    def add_scan_folder(self):
        directory = QFileDialog.getExistingDirectory(self, caption="Select folder to scan", dir=HOME_DIR)
        size = get_folder_size(directory)
        date = friendly_date(os.stat(directory).st_ctime)
        directory_record = dict(path=directory, size=size, date=date)

        self.signals.ADD_FOLDER.emit(directory_record)

