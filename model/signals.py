from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QTextBlockFormat

from model.dto.folder import FolderDTO


class AppSignals(QObject):

    PROCESSING = Signal(bool, name="processing")
    CONFIGS_LOAD = Signal(dict, name="model_load")
    REMOVE_FOLDER_PRESSED = Signal(str, name="remove_folder_pressed")
    ADD_FOLDER_PRESSED = Signal(FolderDTO, name="add_folder_pressed")
    SELECT_FOLDER_CHANGED = Signal(name="select_folder_pressed")
    SCAN_PRESSED = Signal(name="scan_duplicates_pressed")
    MERGE_PRESSED = Signal(name="merge_pressed")
    STATUS_MESSAGE_SET = Signal(str, int, name="status_changed")
    RESULTS_ARRIVED = Signal(list, name="results_arrived")
    PRINT_RESULT_CHUNK = Signal(str, QTextBlockFormat, name="print_result_chunk")
    CONFIGS_CHANGE = Signal(dict, name="configs_change")

    def __init__(self):
        QObject.__init__(self)
