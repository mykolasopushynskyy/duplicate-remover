from typing import Sequence

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication

import configs
from model.signals import AppSignals
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
