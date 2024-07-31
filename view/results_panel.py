from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtGui import (
    QColor,
    QTextBlockFormat,
    Qt,
)
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QPlainTextEdit,
)
from model.signals import AppSignals
from util.utils import threaded

LIGHT_BLUE = "#f0f8ff"
LAVENDER = "#e6e6fa"

BLUE_FMT = QTextBlockFormat()
BLUE_FMT.setAlignment(Qt.AlignmentFlag.AlignLeft)
BLUE_FMT.setBackground(QColor.fromString(LIGHT_BLUE))

LAVENDER_FMT = QTextBlockFormat()
LAVENDER_FMT.setAlignment(Qt.AlignmentFlag.AlignLeft)
LAVENDER_FMT.setBackground(QColor.fromString(LAVENDER))


class ResultsList(QGroupBox):
    def __init__(self, signals: AppSignals, title: str):
        QGroupBox.__init__(self, title)
        self.signals = signals
        self.signals.RESULTS_ARRIVED.connect(self.results_arrived)
        self.signals.SCANNING.connect(self.scanning)
        self.signals.PRINT_RESULT_CHUNK.connect(self.print_text_block)

        self.h_layout = QHBoxLayout()
        self.setLayout(self.h_layout)

        self.text_edit = QPlainTextEdit()
        self.text_edit.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
        self.text_edit.setReadOnly(True)
        self.h_layout.addWidget(self.text_edit)

        self.setLayout(self.h_layout)

    @Slot(list)
    @threaded
    def results_arrived(self, duplicates: list):
        if len(duplicates) == 0:
            return

        duplicates = [
            "\n".join([f"{value}" for i, value in enumerate(entries)])
            + ("\n" if i < len(duplicates) - 1 else "")  # skip last end line
            for i, entries in enumerate(duplicates)
        ]

        for i, blocks in enumerate(duplicates):
            for d in blocks:
                if i % 2 == 1:
                    self.signals.PRINT_RESULT_CHUNK.emit(d, BLUE_FMT)
                else:
                    self.signals.PRINT_RESULT_CHUNK.emit(d, LAVENDER_FMT)

    @Slot(str, QTextBlockFormat)
    def print_text_block(self, text: str, fmt: QTextBlockFormat):
        self.text_edit.textCursor().beginEditBlock()
        self.text_edit.textCursor().setBlockFormat(fmt)
        self.text_edit.textCursor().insertText(text)
        self.text_edit.textCursor().endEditBlock()

    def scanning(self):
        self.text_edit.clear()
