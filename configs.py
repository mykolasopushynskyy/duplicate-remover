"""
This module contains config manager class and various additional util methods.
"""

import json
import os

from PySide6.QtCore import Slot
from appdirs import user_config_dir
from model.signals import AppSignals

PROJECT_DIR = os.path.dirname(__file__)

APP_NAME = "Duplicate Remover"
HOME_DIR = os.path.expanduser("~")
ICONS_FONT_FILE_PATH = os.path.abspath(os.path.join(PROJECT_DIR, "assets", "icons.ttf"))
MAIN_WINDOW_STYLE = os.path.abspath(
    os.path.join(PROJECT_DIR, "assets", "main_window.qss")
)
SETTINGS_WINDOW_STYLE = os.path.abspath(
    os.path.join(PROJECT_DIR, "assets", "settings_window.qss")
)
CONFIG_FILE_NAME = "config.json"
DEFAULT_CONFIG_FILE_PATH = os.path.abspath(
    os.path.join(PROJECT_DIR, "assets", CONFIG_FILE_NAME)
)

# json file keys
MERGE_FOLDER = "merge_folder"
FOLDERS_TO_SCAN = "folders_to_scan"
DELETE_ORIGINAL_FILES = "delete_original_files"
EXTENSIONS_TO_SCAN = "extensions_to_scan"
PARSE_DATE_FROM_FILENAME = "parse_date_from_filename"
MERGE_FILE_FORMAT = "merge_file_format"
SYSTEM_FOLDERS_TO_SKIP = "system_folders_to_skip"
APPEARANCE_THEME = "appearance_theme"


def load_file(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    else:
        return {}


class ConfigManager:
    def __init__(self, signals: AppSignals, config_file: str = CONFIG_FILE_NAME):
        self.signals = signals
        self.config_dir = user_config_dir(APP_NAME)
        os.makedirs(self.config_dir, exist_ok=True)
        self.config_file = os.path.join(self.config_dir, config_file)
        self.configs = self.load_config()

        # subscribe for config change
        signals.CONFIGS_CHANGE.connect(self.update_configs)

    def load_config(self):
        default_config = load_file(DEFAULT_CONFIG_FILE_PATH)
        config = load_file(self.config_file)

        return {
            key: value
            for (key, value) in (tuple(default_config.items()) + tuple(config.items()))
        }

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.configs, f, indent=4)

    def get(self, key, default=None):
        val = self.configs.get(key)
        return default if val is None else val

    def set(self, key, value):
        self.configs[key] = value
        self.save_config()

    @Slot(dict)
    def update_configs(self, model: dict):
        for k, v in model.items():
            self.configs[k] = v
        self.save_config()
