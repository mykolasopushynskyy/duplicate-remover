from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QSizePolicy,
    QHBoxLayout,
    QFrame,
    QLineEdit,
    QComboBox,
)

from configs import (
    EXTENSIONS_TO_SCAN,
    DELETE_ORIGINAL_FILES,
    MERGE_FOLDER,
    SETTINGS_WINDOW_STYLE,
    PARSE_DATE_FROM_FILENAME,
    MERGE_FILE_FORMAT,
)
from model.signals import AppSignals
from util import icons
from view.widgets.animated_toggle import AnimatedToggle


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
        self.icon_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.icon_label.setPixmap(self.image.pixmap(self.image.availableSizes()[0]))
        self.layout.addWidget(self.icon_label)

        self.title_label = QLabel(text=label)
        self.title_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.layout.addWidget(self.title_label)

        # spacer
        self.spacer = QWidget(self)
        self.spacer.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.spacer.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.layout.addWidget(self.spacer)

        self.setLayout(self.layout)

    def addWidget(
        self,
        widget: QWidget,
    ):
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

        self.signals.MODEL_LOAD.connect(self.set_values_from_configs)
        self.signals.CONFIGS_CHANGE.connect(self.set_values_from_configs)

        # scan settings group
        self.scan_settings_label = QLabel("Scan settings")
        self.scan_settings_label.setProperty("qss", "group-label")
        self.layout.addWidget(self.scan_settings_label)

        # Select folder label
        self.destination_folder = SettingElement(
            self.signals,
            icons.open_folder(size=20, color=(0, 0, 0)),
            "Select destination folder",
        )
        self.destination_folder.setProperty("qss", "group-top")
        self.layout.addWidget(self.destination_folder)

        self.destination_folder_label = QLabel(text="Folder address")
        self.destination_folder_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        self.destination_folder.addWidget(self.destination_folder_label)

        # Scan system dirs
        self.scan_sys_dirs = SettingElement(
            self.signals,
            icons.system(size=20, color=(0, 0, 0)),
            "Delete original files",
        )
        self.scan_sys_dirs.setProperty("qss", "group-middle")
        self.layout.addWidget(self.scan_sys_dirs)

        self.delete_original_files_toggle = AnimatedToggle()
        self.delete_original_files_toggle.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        self.scan_sys_dirs.addWidget(self.delete_original_files_toggle)

        # Extension items
        self.extensions_to_scan = SettingElement(
            self.signals,
            icons.picture_file(size=20, color=(0, 0, 0)),
            "Extension to scan",
        )
        self.extensions_to_scan.setProperty("qss", "group-middle")
        self.layout.addWidget(self.extensions_to_scan)

        self.extensions_to_scan_edit = QLineEdit()
        self.extensions_to_scan_edit.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        self.extensions_to_scan_edit.setMinimumWidth(250)
        self.extensions_to_scan.addWidget(self.extensions_to_scan_edit)

        # Parse date from filename
        self.parse_date_from_file_name = SettingElement(
            self.signals,
            icons.calender(size=20, color=(0, 0, 0)),
            "Parse date from filename",
        )
        self.parse_date_from_file_name.setProperty("qss", "group-middle")
        self.layout.addWidget(self.parse_date_from_file_name)

        self.parse_filename_date_toggle = AnimatedToggle()
        self.parse_filename_date_toggle.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        self.parse_date_from_file_name.addWidget(self.parse_filename_date_toggle)

        # Merge filename format
        self.merge_filename_format = SettingElement(
            self.signals, icons.edit(size=20, color=(0, 0, 0)), "Merge file name format"
        )
        self.merge_filename_format.setProperty("qss", "group-bottom")
        self.layout.addWidget(self.merge_filename_format)

        self.filename_format_combo = QComboBox()
        self.filename_format_combo.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        self.filename_format_combo.setMinimumWidth(250)
        self.merge_filename_format.addWidget(self.filename_format_combo)

        # appearance
        self.appearance_label = QLabel("Appearance")
        self.appearance_label.setProperty("qss", "group-label")
        self.layout.addWidget(self.appearance_label)

        self.destination_folder = SettingElement(
            self.signals, icons.adjust(size=20, color=(0, 0, 0)), "Choose theme"
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
        with open(SETTINGS_WINDOW_STYLE, "r") as file:
            style = file.read()
            self.setStyleSheet(style)

    @Slot(dict)
    def set_values_from_configs(self, cfg: dict):
        self.destination_folder_label.setText(cfg[MERGE_FOLDER])
        self.delete_original_files_toggle.setChecked(cfg[DELETE_ORIGINAL_FILES])
        self.extensions_to_scan_edit.setText(" ".join(cfg[EXTENSIONS_TO_SCAN]))
        self.parse_filename_date_toggle.setChecked(cfg[PARSE_DATE_FROM_FILENAME])
        self.filename_format_combo.addItems(cfg[MERGE_FILE_FORMAT])
