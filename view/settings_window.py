from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QSizePolicy,
    QHBoxLayout, QFrame,
)

import configs
from model.signals import AppSignals
from util import icons


# TODO Implement settings window
# TODO Implement the following settings:
# TODO
# TODO 1. files extensions to scan
# TODO 2. enable/disable scan of system dirs
# TODO 3. appearance - light/dark/system
# TODO 4. destination folder change (move out/copy from toolbar)
# TODO 6. show individual files in scan result
# TODO 5. TBD


class SettingElement(QFrame):
    def __init__(self, signals: AppSignals, image: QIcon, label: str, *args, **kwargs):
        QFrame.__init__(self, *args, **kwargs)

        self.signals = signals

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.layout = QHBoxLayout()
        self.image = image

        self.icon_label = QLabel()
        self.icon_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        self.icon_label.setPixmap(self.image.pixmap(self.image.availableSizes()[0]))
        self.layout.addWidget(self.icon_label)

        self.title_label = QLabel(text=label)
        self.layout.addWidget(self.title_label)

        # spacer
        self.spacer = QWidget(self)
        self.spacer.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.spacer.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.layout.addWidget(self.spacer)

        self.setLayout(self.layout)

    def addWidget(self, widget: QWidget):
        self.layout.addWidget(widget)


class SettingsWindow(QWidget):
    def __init__(self, signals: AppSignals, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        # signals
        self.signals = signals

        self.setWindowTitle("Settings")
        self.setMinimumWidth(800)
        self.setMinimumHeight(800)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)

        # scan settings
        self.scan_settings_label = QLabel("Scan settings")
        self.scan_settings_label.setProperty("qss", "group-label")
        self.layout.addWidget(self.scan_settings_label)

        self.destination_folder = SettingElement(
            self.signals,
            icons.open_folder(size=20, color=(0, 0, 0)),
            "Select destination folder"
        )
        self.destination_folder.setProperty("qss", "group-top")
        self.layout.addWidget(self.destination_folder)

        self.scan_sys_dirs = SettingElement(
            self.signals,
            icons.system(size=20, color=(0, 0, 0)),
            "Scan system dirs"
        )
        self.scan_sys_dirs.setProperty("qss", "group-middle")
        self.layout.addWidget(self.scan_sys_dirs)

        self.extensions_to_scan = SettingElement(
            self.signals,
            icons.picture_file(size=20, color=(0, 0, 0)),
            "Extension to scan"
        )
        self.extensions_to_scan.setProperty("qss", "group-middle")
        self.layout.addWidget(self.extensions_to_scan)

        self.parse_date_from_file_name = SettingElement(
            self.signals,
            icons.calender(size=20, color=(0, 0, 0)),
            "Parse date from filename"
        )
        self.parse_date_from_file_name.setProperty("qss", "group-middle")
        self.layout.addWidget(self.parse_date_from_file_name)

        self.merge_filename_format = SettingElement(
            self.signals,
            icons.edit(size=20, color=(0, 0, 0)),
            "Merge file name format"
        )
        self.merge_filename_format.setProperty("qss", "group-bottom")
        self.layout.addWidget(self.merge_filename_format)

        # appearance
        self.appearance_label = QLabel("Appearance")
        self.appearance_label.setProperty("qss", "group-label")
        self.layout.addWidget(self.appearance_label)

        self.destination_folder = SettingElement(
            self.signals,
            icons.adjust(size=20, color=(0, 0, 0)),
            "Choose theme"
        )
        self.destination_folder.setProperty("qss", "group")
        self.layout.addWidget(self.destination_folder)

        # spacer
        self.v_spacer = QWidget(self)
        self.v_spacer.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        self.v_spacer.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.layout.addWidget(self.v_spacer)

        self.setLayout(self.layout)

        # load style
        with open(configs.SETTINGS_WINDOW_STYLE, "r") as file:
            style = file.read()
            self.setStyleSheet(style)
