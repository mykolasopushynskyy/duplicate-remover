from PySide6 import QtGui
from PySide6.QtCore import Slot, QPoint, Qt, QSize, QFile
from PySide6.QtGui import QAction, QIcon, QImage
from PySide6.QtWidgets import QMainWindow, QToolBar, QPushButton, QToolButton, QWidget, QSizePolicy, QLabel, QStyle, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox, QScrollArea, QListWidget, QListWidgetItem, QAbstractItemView

import configs
from model.signals import AppSignals
from util import icons, utils
from view.qt.toolbar import DRToolbar

DEFAULT_STATUS_TEXT = "···"


class FolderItem(QWidget):
    def __init__(self, path: str, size: str, date: str, on_remove: callable = None, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.path = path
        self.size = size
        self.date = date
        self.on_remove = on_remove

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.h_layout = QHBoxLayout()
        self.setLayout(self.h_layout)

        self.v_icon_layout = QVBoxLayout()
        self.v_label_layout = QVBoxLayout()
        self.v_btn_layout = QVBoxLayout()

        self.image = QLabel()
        folder = icons.folder(size=40, color=(244, 191, 79))
        self.image.setProperty("qss", "file_icon")
        self.image.setPixmap(folder.pixmap(folder.availableSizes()[0]))
        self.image.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.v_icon_layout.addWidget(self.image)

        self.h_layout.addLayout(self.v_icon_layout, 0)

        self.path_label = QLabel(text=f"Path: {utils.short_path(self.path)}")
        self.path_label.setProperty("qss", "file_label")
        self.v_label_layout.addWidget(self.path_label, 0, Qt.AlignmentFlag.AlignLeft)

        self.size_label = QLabel(text=self.size)
        self.size_label.setProperty("qss", "file_size")
        self.v_label_layout.addWidget(self.size_label, 0, Qt.AlignmentFlag.AlignLeft)

        self.date_label = QLabel(text=self.date)
        self.date_label.setProperty("qss", "file_date")
        self.v_label_layout.addWidget(self.date_label, 0, Qt.AlignmentFlag.AlignLeft)

        self.spacer_1 = QWidget(self)
        self.spacer_1.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.spacer_1.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.v_label_layout.addWidget(self.spacer_1)

        self.h_layout.addLayout(self.v_label_layout, 1)

        self.remove_button = QPushButton(icon=icons.minus(size=20, color=(255, 0, 0)))
        self.remove_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.remove_button.clicked.connect(self.on_remove)
        self.v_btn_layout.addWidget(self.remove_button, 0, Qt.AlignmentFlag.AlignRight)

        self.spacer_2 = QWidget(self)
        self.spacer_2.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.spacer_2.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.v_btn_layout.addWidget(self.spacer_2)

        self.h_layout.addLayout(self.v_btn_layout, 0)


class ResultsList(QGroupBox):
    def __init__(self,signals: AppSignals,  title: str ):
        QGroupBox.__init__(self, title)
        self.signals = signals


class FoldersList(QGroupBox):
    def __init__(self, signals: AppSignals, title: str):
        QGroupBox.__init__(self, title)
        self.signals = signals
        self.signals.MODEL_LOAD.connect(self.load_folders)
        self.signals.ADD_FOLDER.connect(self.add_folder)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.list_widget = QListWidget(self)
        self.list_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.layout.addWidget(self.list_widget)

    def load_folders(self, model: dict):
        for folder in model["folders_to_scan"].values():
            self.add_folder(folder)

    def add_folder(self, folder: dict):
        # on_remove = lambda
        folder_widget = FolderItem(folder["path"],
                                   "Size: %s" % folder["size"],
                                   "Date: %s" % folder["date"],
                                   lambda: self.remove_folder(self.list_widget, folder["path"])
                                   )
        folder_widget.setFixedHeight(80)

        folder_item = QListWidgetItem(self.list_widget)
        folder_item.setSizeHint(QSize(folder_widget.sizeHint().width(), 75))

        self.list_widget.addItem(folder_item)
        self.list_widget.setItemWidget(folder_item, folder_widget)
        # folder_widget.set_on_remove(lambda: self.remove_folder(folder["path"]))

    def remove_folder(self, list_widget, path):
        self.signals.REMOVE_FOLDER.emit(path)
        print("Removed %s" % path)
        for i in range(0, list_widget.count()):
            w = list_widget.itemWidget(list_widget.item(i))
            if w is not None and w.path == path:
                list_widget.takeItem(i)


class CentralWidget(QWidget):
    def __init__(self, signals: AppSignals):
        QWidget.__init__(self)
        self.signals = signals

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.folders = FoldersList(self.signals, "Folders to scan")
        self.folders.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.folders.setFixedWidth(400)
        self.layout.addWidget(self.folders)

        self.results = ResultsList(self.signals, "Duplicates")
        self.results.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.addWidget(self.results)


class DRQMainWindow(QMainWindow):
    def __init__(self, signals: AppSignals):
        QMainWindow.__init__(self)

        self.signals = signals

        # window settings
        self.setWindowTitle("Duplicate Remover")
        self.setMinimumSize(1000, 600)
        # self.setUnifiedTitleAndToolBarOnMac(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        geometry = self.screen().availableGeometry()
        center_point = QPoint(
            int((geometry.width() - self.width()) / 2),
            int((geometry.height() - self.height()) / 2)
        )
        self.move(center_point)

        # subscriptions
        self.signals.STATUS_MESSAGE_SET.connect(self.set_message)

        # toolbar
        self.tool_bar = DRToolbar(self.signals)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.tool_bar)

        # main window
        self.central_widget = CentralWidget(signals)
        self.setCentralWidget(self.central_widget)

        # status bar
        self.status = self.statusBar()
        self.status.showMessage(DEFAULT_STATUS_TEXT)

        # load style
        with open(configs.APP_STYLE_FILE_PATH, "r") as file:
            style = file.read()
            self.setStyleSheet(style)

    @Slot(str)
    def set_message(self, message):
        if message is None or len(message) == 0:
            self.status.showMessage(text=DEFAULT_STATUS_TEXT)
        else:
            self.status.showMessage(text=message)
