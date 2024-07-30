"""
This module contains config manager class and various additional util methods.
"""

import json
import os

from PySide6.QtCore import Slot
from appdirs import user_config_dir
from model.signals import AppSignals

APP_NAME = "Duplicate Remover"

PROJECT_DIR = os.path.dirname(__file__)
HOME_DIR = os.path.expanduser("~")
ICONS_FONT_FILE_PATH = os.path.abspath(os.path.join(PROJECT_DIR, "assets", "icons.ttf"))
APP_STYLE_FILE_PATH = os.path.abspath(os.path.join(PROJECT_DIR, "assets", "style.qss"))
CONFIG_FILE_LOCATION_NAME = "config.json"


class ConfigManager:
    def __init__(
            self,
            signals: AppSignals,
            config_file: str = CONFIG_FILE_LOCATION_NAME
    ):
        self.signals = signals
        self.config_dir = user_config_dir(APP_NAME)
        os.makedirs(self.config_dir, exist_ok=True)
        self.config_file = os.path.join(self.config_dir, config_file)
        self.config = self.load_config()

        # subscribe for config change
        # QObject.connect(self, signal=signals.CONFIGS_CHANGE, receiver=self.update_configs)
        signals.CONFIGS_CHANGE.connect(self.update_configs)

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f)
        else:
            return {}

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key, default=None):
        val = self.config.get(key)
        return default if val is None else val

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    @Slot(dict)
    def update_configs(self, model: dict):
        for k, v in model:
            self.config[k] = v
        self.save_config()
