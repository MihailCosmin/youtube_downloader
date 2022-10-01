from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QPushButton


class LeftMenu(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent

        self.setObjectName(u"left_menu_frame")

        self.setMaximumWidth(self.parent.left_bar_width)
        self.setMinimumWidth(self.parent.left_bar_width)
        self.left_frame_layout = QVBoxLayout(self)

        self.settings_button = QPushButton("")
        self.settings_button.setObjectName(u"settings_button")
        self.settings_button.setIconSize(self.settings_button.iconSize() * 2)
        self.settings_button.clicked.connect(self.parent.toggle_settings)
        self.left_frame_layout.addWidget(self.settings_button)

        self.downloads_button = QPushButton("")
        self.downloads_button.setObjectName(u"downloads_button")
        self.downloads_button.setIconSize(self.settings_button.iconSize() * 2)
        self.downloads_button.clicked.connect(self.parent.toggle_downloads)
        self.left_frame_layout.addWidget(self.downloads_button)

        self.left_frame_layout.addStretch()
