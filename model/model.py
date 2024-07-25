from configs import ConfigManager

FOLDERS_TO_SCAN_CHANGED = "folders_to_scan_changed"
MERGE_FOLDER_CHANGE = "merge_folder_change"
STATUS_MESSAGE_CHANGED = "status_changed"
CONFIGS_CHANGE = "configs_change"
RESULTS_ARRIVED = "results_arrived"


class BaseModel:
    def __init__(self):
        self._event_listeners = {}

    def subscribe(self, event, fn):
        if event in self._event_listeners:
            self._event_listeners[event].append(fn)
        else:
            self._event_listeners[event] = [fn]

        return lambda: self._event_listeners[event].remove(fn)

    def publish(self, event, data=None):
        if event not in self._event_listeners.keys():
            return

        for func in self._event_listeners[event]:
            data = data if data is not None else self
            func(data)


class ApplicationModel(BaseModel):
    def __init__(self):
        super().__init__()
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
        self.publish(MERGE_FOLDER_CHANGE, self.merge_folder)
        self.publish(CONFIGS_CHANGE, self.to_configs())

    def add_folder_to_scan(self, record: dict):
        self.folders_to_scan[record.get("path")] = record
        self.publish(FOLDERS_TO_SCAN_CHANGED, self.folders_to_scan)
        self.publish(CONFIGS_CHANGE, self.to_configs())

    def remove_folder_to_scan(self, path):
        self.folders_to_scan.pop(path)
        self.publish(FOLDERS_TO_SCAN_CHANGED, self.folders_to_scan)
        self.publish(CONFIGS_CHANGE, self.to_configs())

    def set_status(self, status):
        self.publish(STATUS_MESSAGE_CHANGED, status)

    def show_results(self, duplicates):
        self.duplicates = duplicates
        self.publish(RESULTS_ARRIVED, duplicates)

    def update_model(self, config_manager: ConfigManager):
        self.merge_folder = config_manager.get("merge_folder", default="")
        self.folders_to_scan = config_manager.get("folders_to_scan", default={})

        self.publish(MERGE_FOLDER_CHANGE, self.merge_folder)
        self.publish(FOLDERS_TO_SCAN_CHANGED, self.folders_to_scan)
