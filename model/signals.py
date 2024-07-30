from PySide6.QtCore import QObject, Signal


class AppSignals(QObject):

    SCANNING = Signal(bool, name="scan_started")
    MODEL_LOAD = Signal(dict, name="model_load")
    REMOVE_FOLDER = Signal(str, name="remove_folder_pressed")
    ADD_FOLDER = Signal(dict, name="add_folder_pressed")
    SELECT_FOLDER_CHANGED = Signal(name="select_folder_pressed")
    SCAN_PRESSED = Signal(name="scan_duplicates_pressed")
    STATUS_MESSAGE_SET = Signal(str, name="status_changed")
    MERGE_FOLDER_CHANGED = Signal(str, name="merge_folder_change")
    FOLDERS_TO_SCAN_CHANGED = Signal(dict, name="folders_to_scan_changed")
    RESULTS_ARRIVED = Signal(list, name="results_arrived")
    CONFIGS_CHANGE = Signal(dict, name="configs_change")

    def __init__(self):
        QObject.__init__(self)
