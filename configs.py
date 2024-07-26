"""
This module contains config manager class and various additional util methods.
"""

import json
import os
from appdirs import user_config_dir

from model import events
from model.pubsub import PubSubBroker

APP_NAME = "Duplicate Remover"

PROJECT_DIR = os.path.dirname(__file__)
ICONS_FONT_FILE_PATH = os.path.abspath(os.path.join(PROJECT_DIR, "assets", "icons.ttf"))
CONFIG_FILE_LOCATION_NAME = "config.json"


class ConfigManager:
    def __init__(
        self, pubsub: PubSubBroker, config_file: str = CONFIG_FILE_LOCATION_NAME
    ):
        self.config_dir = user_config_dir(APP_NAME)
        os.makedirs(self.config_dir, exist_ok=True)
        self.config_file = os.path.join(self.config_dir, config_file)
        self.config = self.load_config()
        self.pubsub = pubsub

        # subscribe for config change
        self.pubsub.subscribe(events.CONFIGS_CHANGE, self.update_configs)

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

    def update_configs(self, model):
        self.config = model.to_configs()
        self.save_config()
