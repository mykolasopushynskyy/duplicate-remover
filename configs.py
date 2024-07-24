"""
This module contains config manager class and various additional util methods.
"""

import json
import os

from appdirs import user_config_dir

PROJECT_DIR = os.path.dirname(__file__)
ICONS_FONT_FILE_PATH = os.path.abspath(os.path.join(PROJECT_DIR, 'resources', 'icons.ttf'))
CONFIG_FILE_LOCATION_NAME = 'config.json'


class ConfigManager:
    def __init__(self, app_name, config_file=CONFIG_FILE_LOCATION_NAME):
        self.app_name = app_name
        self.config_dir = user_config_dir(app_name)
        os.makedirs(self.config_dir, exist_ok=True)
        self.config_file = os.path.join(self.config_dir, config_file)
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()
