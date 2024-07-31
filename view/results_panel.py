from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtGui import QTextCursor, QTextCharFormat, QBrush, QColor, QTextBlockFormat, Qt
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QTextEdit, QPlainTextEdit,
)
from model.signals import AppSignals

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

        self.h_layout = QHBoxLayout()
        self.setLayout(self.h_layout)

        self.text_edit = QTextEdit()
        self.text_edit.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        self.text_edit.setReadOnly(True)
        self.h_layout.addWidget(self.text_edit)

        self.setLayout(self.h_layout)

    @Slot(list)
    def results_arrived(self, duplicates: list):
        if len(duplicates) == 0:
            return

        duplicates = [
            "\n".join([f" {i + 1:<3}: {value}" for i, value in enumerate(entries)]) + "\n" if i < len(duplicates) - 2 else ""
            for i, entries in enumerate(duplicates)
            if len(entries) > 1
        ]

        for i, blocks in enumerate(duplicates):
            for d in blocks:
                if i % 2 == 1:
                    self.print_text_block(d, BLUE_FMT)
                else:
                    self.print_text_block(d, LAVENDER_FMT)

    def print_text_block(self, text: str, fmt: QTextBlockFormat):
        self.text_edit.textCursor().beginEditBlock()
        self.text_edit.textCursor().setBlockFormat(fmt)
        self.text_edit.textCursor().insertText(text)
        self.text_edit.textCursor().endEditBlock()

    def scanning(self):
        self.text_edit.clear()
