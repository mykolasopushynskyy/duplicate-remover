from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QPushButton,
    QWidget,
    QSizePolicy,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)

from util import icons, utils


class FolderItem(QWidget):
    def __init__(
        self,
        path: str,
        size: str,
        date: str,
        on_remove: callable = None,
        *args,
        **kwargs
    ):
        QWidget.__init__(self, *args, **kwargs)
        self.path = path
        self.size = size
        self.date = date
        self.on_remove = on_remove

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.h_layout = QHBoxLayout()
        self.setLayout(self.h_layout)

        self.v_icon_layout = QVBoxLayout()
        self.v_label_layout = QVBoxLayout()
        self.v_btn_layout = QVBoxLayout()

        self.image = QLabel()
        folder = icons.open_folder(size=40, color=(244, 191, 79))
        self.image.setProperty("qss", "file_icon")
        self.image.setPixmap(folder.pixmap(folder.availableSizes()[0]))
        self.image.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.v_icon_layout.addWidget(self.image)

        self.h_layout.addLayout(self.v_icon_layout, 0)

        self.path_label = QLabel(text=utils.short_path(self.path))
        self.path_label.setProperty("qss", "file_label")
        self.path_label.setFixedHeight(16)
        self.path_label.setMaximumWidth(245)
        self.v_label_layout.addWidget(self.path_label, 0, Qt.AlignmentFlag.AlignLeft)

        self.size_label = QLabel(text=self.size)
        self.size_label.setProperty("qss", "file_size")
        self.path_label.setFixedHeight(16)
        self.v_label_layout.addWidget(self.size_label, 0, Qt.AlignmentFlag.AlignLeft)

        self.date_label = QLabel(text=self.date)
        self.date_label.setProperty("qss", "file_date")
        self.path_label.setFixedHeight(16)
        self.v_label_layout.addWidget(self.date_label, 0, Qt.AlignmentFlag.AlignLeft)

        self.spacer_1 = QWidget(self)
        self.spacer_1.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        self.spacer_1.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.v_label_layout.addWidget(self.spacer_1)

        self.h_layout.addLayout(self.v_label_layout, 1)

        self.remove_button = QPushButton(
            icon=icons.trash_bin(size=20, color=(150, 53, 47))
        )
        self.remove_button.setFixedWidth(20)
        self.remove_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        self.remove_button.clicked.connect(self.on_remove)
        self.v_btn_layout.addWidget(self.remove_button, 0, Qt.AlignmentFlag.AlignRight)

        self.spacer_2 = QWidget(self)
        self.spacer_2.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        self.spacer_2.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.v_btn_layout.addWidget(self.spacer_2)

        self.h_layout.addLayout(self.v_btn_layout, 0)
