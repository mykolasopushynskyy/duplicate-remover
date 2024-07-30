from PySide6.QtCore import Slot, QPoint, Qt, QSize, QFile
from PySide6.QtGui import QAction, QIcon, QImage
from PySide6.QtWidgets import QMainWindow, QToolBar, QPushButton, QToolButton, QWidget, QSizePolicy, QLabel, QStyle, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox

import configs
from model.signals import AppSignals
from util import icons
from view.qt.toolbar import DRToolbar

DEFAULT_STATUS_TEXT = "···"


class FolderItem(QWidget):
    def __init__(self, signals: AppSignals, path: str, size: str, date: str, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.signals = signals
        self.path = path
        self.size = size
        self.date = date

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.image = QLabel()
        folder = icons.folder(size=40, color=(0, 0, 0))
        self.image.setProperty("qss", "file_icon")
        self.image.setPixmap(folder.pixmap(folder.availableSizes()[0]))
        self.image.setFixedSize(50, 50)
        self.image.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.layout.addWidget(self.image, 0, 0, 0, 3, Qt.AlignmentFlag.AlignLeft)

        self.path_label = QLabel(text=self.path)
        self.path_label.setProperty("qss", "file_label")
        self.layout.addWidget(self.path_label, 0, 1)

        self.size_label = QLabel(text=self.size)
        self.size_label.setProperty("qss", "file_size")
        self.layout.addWidget(self.size_label, 1, 1)

        self.date_label = QLabel(text=self.date)
        self.date_label.setProperty("qss", "file_date")
        self.layout.addWidget(self.date_label, 2, 1)

        self.remove_button = QPushButton(icon=icons.minus(size=20, color=(255, 0, 0)))
        self.remove_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.remove_button.clicked.connect(self.remove_folder)
        self.layout.addWidget(self.remove_button, 0, 2)

    def remove_folder(self):
        self.signals.REMOVE_FOLDER.emit(self.path)
        self.deleteLater()


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
        self.signals.REMOVE_FOLDER.emit(self.restyle_list)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.spacer = None

    def load_folders(self, model: dict):
        for folder in model["folders_to_scan"].values():
            self.add_folder(folder, add_spacer=False)
        self.add_spacer()
        self.restyle_list()

    def restyle_list(self):
        for i, w in enumerate(self.findChildren(FolderItem)):
            w.layout.setProperty("qss", "even_item" if i % 2 == 1 else "odd_item")
            w.update()

    def add_folder(self, folder: dict, add_spacer=True):
        folder_widget = FolderItem(self.signals, folder["path"], "Size: %s" % folder["size"], "Date: %s" % folder["date"])
        self.layout.addWidget(folder_widget)

        if add_spacer:
            self.spacer.deleteLater()
            self.add_spacer()
        self.restyle_list()

    def add_spacer(self):
        self.spacer = QWidget(self)
        self.spacer.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.spacer.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.layout.addWidget(self.spacer)


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
