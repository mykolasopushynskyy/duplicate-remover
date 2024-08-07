from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QSizePolicy,
    QHBoxLayout,
    QFrame,
)

from model.signals import AppSignals


class SettingsElement(QFrame):
    def __init__(self, signals: AppSignals, image: QIcon, label: str, *args, **kwargs):
        QFrame.__init__(self, *args, **kwargs)

        self.signals = signals

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.layout = QHBoxLayout()
        self.image = image

        self.icon_label = QLabel()
        self.icon_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        self.icon_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.icon_label.setPixmap(self.image.pixmap(self.image.availableSizes()[0]))
        self.layout.addWidget(self.icon_label)

        self.title_label = QLabel(text=label)
        self.title_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.layout.addWidget(self.title_label)

        # spacer
        self.spacer = QWidget(self)
        self.spacer.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.spacer.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.layout.addWidget(self.spacer)

        self.setLayout(self.layout)

    def addWidget(
        self,
        widget: QWidget,
    ):
        self.layout.addWidget(widget)
