from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QSizePolicy,
    QVBoxLayout,
    QGroupBox,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
)

from model.signals import AppSignals
from view.widgets.folder_item import FolderItem


class FoldersList(QGroupBox):
    def __init__(self, signals: AppSignals, title: str):
        QGroupBox.__init__(self, title)
        self.signals = signals
        self.paths = []
        self.signals.MODEL_LOAD.connect(self.load_folders)
        self.signals.ADD_FOLDER_PRESSED.connect(self.add_folder)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.list_widget = QListWidget(self)
        self.list_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.list_widget.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.layout.addWidget(self.list_widget)

    def load_folders(self, model: dict):
        for folder in model["folders_to_scan"].values():
            self.add_folder(folder)

    def add_folder(self, folder: dict):
        # don't add folder if exist
        if folder["path"] in self.paths:
            return

        # add folder
        folder_widget = FolderItem(
            folder["path"],
            "Size: %s" % folder["size"],
            "Date: %s" % folder["date"],
            lambda: self.remove_folder(self.list_widget, folder["path"]),
        )
        folder_widget.setFixedHeight(80)

        folder_item = QListWidgetItem(self.list_widget)
        folder_item.setSizeHint(QSize(folder_widget.sizeHint().width(), 75))

        self.list_widget.addItem(folder_item)
        self.list_widget.setItemWidget(folder_item, folder_widget)
        self.paths.append(folder["path"])

    def remove_folder(self, list_widget, path):
        self.signals.REMOVE_FOLDER_PRESSED.emit(path)
        for i in range(0, list_widget.count()):
            folder_widget = list_widget.itemWidget(list_widget.item(i))
            if folder_widget is not None and folder_widget.path == path:
                list_widget.takeItem(i)
                self.paths.remove(path)
