from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QPushButton,
    QWidget,
    QSizePolicy,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)

from model.dto.folder import FolderDTO
from util import icons, utils
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
        self.v_btn_layout = QVBoxLayout()
        self.v_btn_layout.setSpacing(0)

        self.image = QLabel()
        folder = icons.open_folder(size=40, color=(244, 191, 79))
        self.image.setProperty("qss", "file_icon")
        self.image.setPixmap(folder.pixmap(folder.availableSizes()[0]))
        self.image.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.v_icon_layout.addWidget(self.image)

        self.h_layout.addLayout(self.v_icon_layout)

        self.path_label = QLabel(text=utils.short_path(self.folder.path))
        self.path_label.setProperty("qss", "file_label")
        self.path_label.setFixedWidth(275)
        # self.path_label.setStyleSheet("border: 1px solid silver;")
        self.v_label_layout.addWidget(self.path_label)

        self.size_label = QLabel(text=self.folder.size)
        self.size_label.setProperty("qss", "file_size")
        self.size_label.setFixedWidth(275)
        # self.size_label.setStyleSheet("border: 1px solid silver;")
        self.v_label_layout.addWidget(self.size_label)

        self.date_label = QLabel(text=self.folder.date)
        self.date_label.setProperty("qss", "file_date")
        self.date_label.setFixedWidth(275)
        # self.date_label.setStyleSheet("border: 1px solid silver;")
        self.v_label_layout.addWidget(self.date_label)

        self.h_layout.addLayout(self.v_label_layout)

        self.remove_button = QPushButton(
            icon=icons.trash_bin(size=20, color=(150, 53, 47))
        )
        self.remove_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.remove_button.setFixedWidth(20)
        self.remove_button.clicked.connect(self.on_remove)
        self.v_btn_layout.addWidget(self.remove_button)

        self.spacer = QWidget(self)
        self.spacer.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )
        self.remove_button.setFixedWidth(20)
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
