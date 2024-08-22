from typing import Sequence

from PySide6.QtCore import Slot, QSize
from PySide6.QtWidgets import QApplication

import configs
from model.signals import AppSignals
from util import icons
from view.main_window import DRQMainWindow
from view.theme_detector import detect_system_theme, LIGHT_THEME


class DRQApplication(QApplication):
    def __init__(self, args: Sequence[str], signals: AppSignals):
        super().__init__(args)
        self.signals = signals
        self.setApplicationName(configs.APP_NAME)

        # Window creation
        self.window = DRQMainWindow(signals)
        self.window.show()

        self.signals.CONFIGS_LOAD.connect(self.change_theme)
        self.signals.CONFIGS_CHANGE.connect(self.change_theme)

    @Slot(dict)
    def change_theme(self, cfg: dict):
        # TODO Use QSS as template and switch colors only
        cfg_theme = cfg.get(configs.APPLICATION_THEME)

        # return if no theme change
        if cfg_theme is None or len(cfg_theme) == 0:
            return

        # theme to lower case
        cfg_theme = cfg_theme.lower()

        # detect system theme
        if cfg_theme == "auto":
            cfg_theme = detect_system_theme()

        theme_to_set = (
            configs.LIGHT_THEME if cfg_theme == LIGHT_THEME else configs.DARK_THEME
        )

        # set theme
        with open(theme_to_set, "r") as theme_file:
            self.setStyleSheet(theme_file.read())

        toolbar = self.window.toolbar
        settings = self.window.toolbar.settings

        themed_icon_color = (
            (90, 90, 90) if cfg_theme == LIGHT_THEME else (206, 208, 214)
        )

        # toolbar icons
        toolbar.add_folder_btn.setIcon(icons.plus(size=20, color=themed_icon_color))
        toolbar.exclude_folder_btn.setIcon(
            icons.minus(size=20, color=themed_icon_color)
        )
        toolbar.search_duplicates_btn.setIcon(
            icons.search(size=20, color=themed_icon_color)
        )
        toolbar.merge_duplicates_btn.setIcon(
            icons.picture(size=20, color=themed_icon_color)
        )
        toolbar.destination_folder_btn.setIcon(
            icons.open_folder(size=20, color=themed_icon_color)
        )
        toolbar.settings_btn.setIcon(icons.configs(size=20, color=themed_icon_color))

        # settings icons
        settings.destination_folder.icon_label.setPixmap(
            icons.picture(size=20, color=themed_icon_color).pixmap(QSize(20, 20))
        )
        settings.scan_sys_dirs.icon_label.setPixmap(
            icons.trash_bin(size=20, color=themed_icon_color).pixmap(QSize(20, 20))
        )
        settings.extensions_to_scan.icon_label.setPixmap(
            icons.picture_file(size=20, color=themed_icon_color).pixmap(QSize(20, 20))
        )
        settings.parse_date_from_file_name.icon_label.setPixmap(
            icons.a_z(size=20, color=themed_icon_color).pixmap(QSize(20, 20))
        )
        settings.app_theme.icon_label.setPixmap(
            icons.adjust(size=20, color=themed_icon_color).pixmap(QSize(20, 20))
        )
