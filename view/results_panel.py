from PySide6 import QtWidgets
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QTextEdit,
)

from model.signals import AppSignals


class ResultsList(QGroupBox):
    def __init__(self, signals: AppSignals, title: str):
        QGroupBox.__init__(self, title)
        self.signals = signals
        self.signals.RESULTS_ARRIVED.connect(self.results_arrived)

        self.h_layout = QHBoxLayout()
        self.setLayout(self.h_layout)

        self.text_edit = QTextEdit()
        self.text_edit.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        self.h_layout.addWidget(self.text_edit)

        self.setLayout(self.h_layout)

    def results_arrived(self, duplicates: list):
        if len(duplicates) == 0:
            return

        text = "\n".join(
            [
                "\n".join([f"{i + 1}:{value}" for i, value in enumerate(entries)])
                for entries in duplicates
                if len(entries) > 1
            ]
        )

        self.text_edit.setText(text)
