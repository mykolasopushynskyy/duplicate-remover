from enum import Enum


class Topic(Enum):
    SCANNING = "scan_started"
    MODEL_LOAD = "model_load"
    REMOVE_FOLDER_PRESSED = "remove_folder_pressed"
    ADD_FOLDER_PRESSED = "add_folder_pressed"
    SELECT_FOLDER_PRESSED = "select_folder_pressed"
    SCAN_DUPLICATES_PRESSED = "scan_duplicates_pressed"
    STATUS_MESSAGE_SET = "status_changed"
    MERGE_FOLDER_CHANGED = "merge_folder_change"
    FOLDERS_TO_SCAN_CHANGED = "folders_to_scan_changed"
    RESULTS_ARRIVED = "results_arrived"
    CONFIGS_CHANGE = "configs_change"


class PubSubBroker:
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
