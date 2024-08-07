from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QSizePolicy,
    QLineEdit,
    QComboBox,
    QFileDialog,
)

from configs import (
    EXTENSIONS_TO_SCAN,
    DELETE_ORIGINAL_FILES,
    MERGE_FOLDER,
    SETTINGS_WINDOW_STYLE,
    PARSE_DATE_FROM_FILENAME,
    MERGE_FILE_FORMAT,
    APPLICATION_THEME,
    MERGE_FILE_FORMATS,
    APPLICATION_THEMES,
    HOME_DIR,
)
from model.signals import AppSignals
from util import icons
from util.utils import do_if_present
from view.widgets.animated_toggle import AnimatedToggle
from view.widgets.setting_elment import SettingsElement

ICON_COLOR = (0, 0, 0)
ICON_SIZE = 20


class SettingsWindow(QWidget):
    def __init__(self, signals: AppSignals, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        # signals
        self.signals = signals

        self.setWindowTitle("Settings")
        self.setMinimumWidth(800)
        self.setMinimumHeight(800)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)

        self.signals.CONFIGS_LOAD.connect(self.load_configs)
        self.signals.CONFIGS_CHANGE.connect(self.load_configs)

        # scan settings group
        self.scan_settings_label = QLabel("Scan settings")
        self.scan_settings_label.setProperty("qss", "group-label")
        self.layout.addWidget(self.scan_settings_label)

        # Select folder label
        self.destination_folder = SettingsElement(
            self.signals,
            icons.picture(size=ICON_SIZE, color=ICON_COLOR),
            "Select destination folder",
        )
        self.destination_folder.mousePressEvent = self.select_destination_folder
        self.destination_folder.setProperty("qss", "group-top")
        self.layout.addWidget(self.destination_folder)

        self.destination_folder_label = QLabel(text="Folder address")
        self.destination_folder_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        self.destination_folder.addWidget(self.destination_folder_label)

        # Delete original files
        self.scan_sys_dirs = SettingsElement(
            self.signals,
            icons.trash_bin(size=ICON_SIZE, color=ICON_COLOR),
            "Delete original files",
        )
        self.scan_sys_dirs.setProperty("qss", "group-middle")
        self.layout.addWidget(self.scan_sys_dirs)

        self.delete_original_files_toggle = AnimatedToggle()
        self.delete_original_files_toggle.stateChanged.connect(
            self.delete_original_files
        )
        self.delete_original_files_toggle.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        self.scan_sys_dirs.addWidget(self.delete_original_files_toggle)

        # Extension items
        self.extensions_to_scan = SettingsElement(
            self.signals,
            icons.picture_file(size=ICON_SIZE, color=ICON_COLOR),
            "Extension to scan",
        )
        self.extensions_to_scan.setProperty("qss", "group-middle")
        self.layout.addWidget(self.extensions_to_scan)

        self.extensions_to_scan_edit = QLineEdit()
        self.extensions_to_scan_edit.setMinimumWidth(250)
        self.extensions_to_scan_edit.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        self.extensions_to_scan_edit.editingFinished.connect(self.edit_files_extensions)
        self.extensions_to_scan.addWidget(self.extensions_to_scan_edit)

        # Parse date from filename
        self.parse_date_from_file_name = SettingsElement(
            self.signals,
            icons.a_z(size=ICON_SIZE, color=ICON_COLOR),
            "Parse date from filename",
        )
        self.parse_date_from_file_name.setProperty("qss", "group-middle")
        self.layout.addWidget(self.parse_date_from_file_name)

        self.parse_filename_date_toggle = AnimatedToggle()
        self.parse_filename_date_toggle.stateChanged.connect(
            self.parse_date_from_filename
        )
        self.parse_filename_date_toggle.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        self.parse_date_from_file_name.addWidget(self.parse_filename_date_toggle)

        # Merge filename format
        self.merge_filename_format = SettingsElement(
            self.signals,
            icons.edit(size=ICON_SIZE, color=ICON_COLOR),
            "Merge file name format",
        )
        self.merge_filename_format.setProperty("qss", "group-bottom")
        self.layout.addWidget(self.merge_filename_format)

        self.filename_format_combo = QComboBox()
        self.filename_format_combo.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        self.filename_format_combo.currentIndexChanged.connect(self.change_merge_format)
        self.merge_filename_format.addWidget(self.filename_format_combo)

        # appearance
        self.appearance_label = QLabel("Appearance")
        self.appearance_label.setProperty("qss", "group-label")
        self.layout.addWidget(self.appearance_label)

        # app theme
        self.app_theme = SettingsElement(
            self.signals, icons.adjust(size=ICON_SIZE, color=ICON_COLOR), "Choose theme"
        )
        self.app_theme.setProperty("qss", "group")

        self.app_theme_combo = QComboBox()
        self.app_theme_combo.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        self.app_theme_combo.currentIndexChanged.connect(self.change_appearance_theme)
        self.app_theme.addWidget(self.app_theme_combo)

        self.layout.addWidget(self.app_theme)

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
    def load_configs(self, cfg: dict):
        do_if_present(cfg.get(MERGE_FOLDER), self.destination_folder_label.setText)
        do_if_present(
            cfg.get(DELETE_ORIGINAL_FILES), self.delete_original_files_toggle.setChecked
        )
        do_if_present(cfg.get(EXTENSIONS_TO_SCAN), self.extensions_to_scan_edit.setText)
        do_if_present(
            cfg.get(PARSE_DATE_FROM_FILENAME),
            self.parse_filename_date_toggle.setChecked,
        )

        do_if_present(cfg.get(MERGE_FILE_FORMATS), self.filename_format_combo.addItems)
        do_if_present(
            cfg.get(MERGE_FILE_FORMATS),
            lambda formats: do_if_present(
                do_if_present(cfg.get(MERGE_FILE_FORMAT), formats.index),
                self.filename_format_combo.setCurrentIndex,
            ),
        )

        do_if_present(cfg.get(APPLICATION_THEMES), self.app_theme_combo.addItems)
        do_if_present(
            cfg.get(APPLICATION_THEMES),
            lambda themes: do_if_present(
                do_if_present(cfg.get(APPLICATION_THEME), themes.index),
                self.app_theme_combo.setCurrentIndex,
            ),
        )

    @Slot(dict)
    def select_destination_folder(self, event):
        directory = QFileDialog.getExistingDirectory(
            self, caption="Select destination directory", dir=HOME_DIR
        )
        if directory is not None and len(directory) != 0:
            self.signals.CONFIGS_CHANGE.emit({MERGE_FOLDER: directory})

    @Slot(dict)
    def delete_original_files(self, state):
        result = True if state > 0 else False
        self.signals.CONFIGS_CHANGE.emit({DELETE_ORIGINAL_FILES: result})

    @Slot(dict)
    def edit_files_extensions(self):
        # TODO Validate extensions to scan
        text = self.extensions_to_scan_edit.text()
        self.signals.CONFIGS_CHANGE.emit({EXTENSIONS_TO_SCAN: text})

    @Slot(dict)
    def parse_date_from_filename(self, state):
        result = True if state > 0 else False
        self.signals.CONFIGS_CHANGE.emit({PARSE_DATE_FROM_FILENAME: result})

    @Slot(dict)
    def change_merge_format(self, index):
        text = self.filename_format_combo.itemText(index)
        self.signals.CONFIGS_CHANGE.emit({MERGE_FILE_FORMAT: text})

    @Slot(dict)
    def change_appearance_theme(self, index):
        text = self.app_theme_combo.itemText(index)
        self.signals.CONFIGS_CHANGE.emit({APPLICATION_THEME: text})
