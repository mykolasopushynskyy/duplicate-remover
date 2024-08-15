from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAbstractFileIconProvider
from PySide6.QtWidgets import (
    QPushButton,
    QWidget,
    QSizePolicy,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFileIconProvider,
)

from model.dto.folder import FolderDTO
from util import utils
from view.widgets.animated_toggle import AnimatedToggle


class FolderItem(QWidget):
    def __init__(
        self,
        folder: FolderDTO,
        on_remove: callable = None,
        on_exclude: callable = None,
        *args,
        **kwargs
    ):
        QWidget.__init__(self, *args, **kwargs)
        self.folder = folder
        self.on_remove = on_remove
        self.on_exclude = on_exclude

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.h_layout = QHBoxLayout()
        self.h_layout.setSpacing(0)
        self.setLayout(self.h_layout)

        self.v_icon_layout = QVBoxLayout()
        self.v_icon_layout.setSpacing(0)
        self.v_label_layout = QVBoxLayout()
        self.v_label_layout.setSpacing(0)
        self.h_label_layout = QHBoxLayout()
        self.h_label_layout.setSpacing(0)
        self.v_btn_layout = QVBoxLayout()
        self.v_btn_layout.setSpacing(0)

        self.image = QLabel()
        folder = QFileIconProvider().icon(QAbstractFileIconProvider.IconType.Folder)
        self.image.setProperty("qss", "file_icon")
        self.image.setPixmap(folder.pixmap(QSize(40, 40)))
        self.image.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.v_icon_layout.addWidget(self.image)

        self.h_layout.addLayout(self.v_icon_layout)

        self.path_label = QLabel(text=utils.short_path(self.folder.path))
        self.path_label.setProperty("qss", "file_label")
        self.path_label.setFixedWidth(265)
        self.v_label_layout.addWidget(self.path_label)

        self.size_label = QLabel(text=self.folder.size)
        self.size_label.setProperty("qss", "file_size")
        self.size_label.setFixedWidth(265)
        self.v_label_layout.addWidget(self.size_label)

        self.date_label = QLabel(text=self.folder.date)
        self.date_label.setProperty("qss", "file_date")
        self.date_label.setFixedWidth(140)
        self.h_label_layout.addWidget(self.date_label)

        self.exclude_label = QLabel(text=self.folder.date)
        self.exclude_label.setProperty("qss", "exclude_label")
        self.exclude_label.setFixedWidth(115)
        self.exclude_label.setText("Exclude")
        self.exclude_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.h_label_layout.addWidget(self.exclude_label)

        self.v_label_layout.addLayout(self.h_label_layout)
        self.h_layout.addLayout(self.v_label_layout)

        self.remove_button = QPushButton(
            icon=QFileIconProvider().icon(QAbstractFileIconProvider.IconType.Trashcan)
        )
        self.remove_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.remove_button.setFixedWidth(10)
        self.remove_button.clicked.connect(self.on_remove)
        self.v_btn_layout.addWidget(self.remove_button)

        self.spacer = QWidget(self)
        self.spacer.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )
        self.spacer.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.v_btn_layout.addWidget(self.spacer)

        self.exclude_check = AnimatedToggle()
        self.exclude_check.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )
        self.exclude_check.setFixedWidth(30)
        self.exclude_check.setChecked(self.folder.exclude)
        self.exclude_check.stateChanged.connect(self.on_exclude)
        self.v_btn_layout.addWidget(self.exclude_check)

        self.h_layout.addLayout(self.v_btn_layout)
