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

        self.back_button = QPushButton()
        self.back_button.setObjectName(u"back_button")
        self.back_button.setIconSize(self.back_button.iconSize() * 2)
        self.back_button.clicked.connect(self.parent.back_button_clicked)
        self.back_button.setToolTip("Go back to the previous page")
        self.left_frame_layout.addWidget(self.back_button)

        self.downloads_button = QPushButton("")
        self.downloads_button.setObjectName(u"downloads_button")
        self.downloads_button.setIconSize(self.downloads_button.iconSize() * 2)
        self.downloads_button.clicked.connect(self.parent.toggle_downloads)
        self.downloads_button.setToolTip("Toggle Download Tab")
        self.left_frame_layout.addWidget(self.downloads_button)

        self.clear_cache = QPushButton()
        self.clear_cache.setObjectName(u"clear_cache")
        self.clear_cache.setIconSize(self.clear_cache.iconSize() * 2)
        self.clear_cache.clicked.connect(self.parent.clear_cache_clicked)
        self.clear_cache.setToolTip("Clear YouTube cache")
        self.left_frame_layout.addWidget(self.clear_cache)

        self.left_frame_layout.addStretch(1)

        self.settings_button = QPushButton("")
        self.settings_button.setObjectName(u"settings_button")
        self.settings_button.setIconSize(self.settings_button.iconSize() * 2)
        self.settings_button.clicked.connect(self.parent.toggle_settings)
        self.settings_button.setToolTip("Toggle Settings Tab")
        self.left_frame_layout.addWidget(self.settings_button)
    
        self.left_frame_layout.addStretch()
