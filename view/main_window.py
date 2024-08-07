from PySide6.QtCore import Slot, QPoint, Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QSizePolicy,
    QHBoxLayout,
    QProgressBar,
)

import configs
from model.signals import AppSignals
from view.folders_panel import FoldersList
from view.results_panel import ResultsList
from view.toolbar import DRToolbar

DEFAULT_STATUS_TEXT = "···"


class CentralWidget(QWidget):
    def __init__(self, signals: AppSignals):
        QWidget.__init__(self)
        self.signals = signals

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.folders = FoldersList(self.signals, "Folders to scan")
        self.folders.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )
        self.folders.setFixedWidth(400)
        self.layout.addWidget(self.folders)

        self.results = ResultsList(self.signals, "Duplicates")
        self.results.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.layout.addWidget(self.results)


# TODO Disable views during search like toolbar, folder list, etc
class DRQMainWindow(QMainWindow):
    def __init__(self, signals: AppSignals):
        QMainWindow.__init__(self)

        self.signals = signals

        # window settings
        self.setWindowTitle("Duplicate Remover")
        self.setMinimumSize(1200, 800)
        # self.setUnifiedTitleAndToolBarOnMac(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        geometry = self.screen().availableGeometry()
        center_point = QPoint(
            int((geometry.width() - self.width()) / 2),
            int((geometry.height() - self.height()) / 2),
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
        self.progressBar = QProgressBar()
        self.progressBar.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setMaximumSize(200, 20)
        self.progressBar.hide()

        self.status = self.statusBar()
        self.status.showMessage(DEFAULT_STATUS_TEXT)
        self.status.addPermanentWidget(self.progressBar)

        # load style
        with open(configs.MAIN_WINDOW_STYLE, "r") as file:
            style = file.read()
            self.setStyleSheet(style)

    @Slot(str)
    def set_message(self, message, progress=0):
        if message is None or len(message) == 0:
            self.status.showMessage(DEFAULT_STATUS_TEXT)
        else:
            self.status.showMessage(message)

        if progress > 0:
            self.progressBar.show()
            self.progressBar.setValue(progress)
        else:
            self.progressBar.hide()
