from configs import ConfigManager
from model.pubsub import PubSubBroker, Topic


class ApplicationModel:
    def __init__(self, pubsub: PubSubBroker):
        super().__init__()
        self.pubsub = pubsub
        self.merge_folder = ""
        self.folders_to_scan = {}
        self.status_message = ""
        self.duplicates = ""

    def to_configs(self):
        return dict(
            merge_folder=self.merge_folder,
            folders_to_scan=self.folders_to_scan
        )

    def set_merge_folder(self, path):
        self.merge_folder = path
        self.pubsub.publish(Topic.MERGE_FOLDER_CHANGED, self.merge_folder)
        self.pubsub.publish(Topic.CONFIGS_CHANGE, self.to_configs())

    def add_folder_to_scan(self, record: dict):
        self.folders_to_scan[record.get("path")] = record
        self.pubsub.publish(Topic.FOLDERS_TO_SCAN_CHANGED, self.folders_to_scan)
        self.pubsub.publish(Topic.CONFIGS_CHANGE, self.to_configs())

    def remove_folder_to_scan(self, path):
        self.folders_to_scan.pop(path)
        self.pubsub.publish(Topic.FOLDERS_TO_SCAN_CHANGED, self.folders_to_scan)
        self.pubsub.publish(Topic.CONFIGS_CHANGE, self.to_configs())

    def set_status(self, status):
        self.pubsub.publish(Topic.STATUS_MESSAGE_SET, status)

    def show_results(self, duplicates):
        self.duplicates = duplicates
        self.pubsub.publish(Topic.RESULTS_ARRIVED, duplicates)

    def update_model(self, config_manager: ConfigManager):
        self.merge_folder = config_manager.get("merge_folder", default="")
        self.folders_to_scan = config_manager.get("folders_to_scan", default={})

        self.pubsub.publish(Topic.MERGE_FOLDER_CHANGED, self.merge_folder)
        self.pubsub.publish(Topic.FOLDERS_TO_SCAN_CHANGED, self.folders_to_scan)
