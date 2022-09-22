from PySide6.QtWidgets import QWidget
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui

from utils.format import format_button
from utils.format import format_loading_bar
from utils.format import format_button_transparent

class LeftWidget(QWidget):
    """_summary_

    Args:
        QWidget (_type_): _description_
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.left_layout = QtWidgets.QGridLayout()
        self.left_layout.setObjectName(u"left_layout")

        self.setLayout(self.left_layout)

        self.left_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.left_layout.setContentsMargins(5, 5, 5, 5)
        # self.setStyleSheet("QWidget {border: 1px solid #ffffff;}")

        self.setMinimumWidth(self.parent._left_width)
        self.setMaximumWidth(self.parent._left_width)

        self.settings_button = QtWidgets.QPushButton("")
        self.settings_button.setIcon(QtGui.QIcon("icons/settings.png"))

        self.settings_button.setMinimumWidth(self.settings_button.iconSize().width() + 10)
        self.settings_button.setMaximumWidth(self.settings_button.iconSize().width() + 10)

        self.settings_button = format_button_transparent(self.settings_button)

        self.settings_button.clicked.connect(self.parent.settings_widget._show_settings)
        self.left_layout.addWidget(self.settings_button, 0, 4, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
        self.button1 = QtWidgets.QPushButton("Download Current Video")
        self.button1.setMinimumWidth(self.parent._left_width - 10)
        self.button2 = QtWidgets.QPushButton("Add Video to Queue")
        self.button3 = QtWidgets.QPushButton("Download Playlist")
        self.button4 = QtWidgets.QPushButton("Download Queue")
        self.button1 = format_button(self.button1, self.parent._left_width * 0.6)
        self.button2 = format_button(self.button2, self.parent._left_width * 0.6)
        self.button3 = format_button(self.button3, self.parent._left_width * 0.6)
        self.button4 = format_button(self.button4, self.parent._left_width * 0.6)

        self.queue_label = QtWidgets.QLabel("Download Queue")

        # create a loading bar
        self.loading_bar_single = QtWidgets.QProgressBar()
        self.loading_bar_playlist = QtWidgets.QProgressBar()
        self.loading_bar_queue = QtWidgets.QProgressBar()
        self.loading_bar_single = format_loading_bar(self.loading_bar_single, width=self.parent._left_width * 0.35)
        self.loading_bar_playlist = format_loading_bar(self.loading_bar_playlist, width=self.parent._left_width * 0.35)
        self.loading_bar_queue = format_loading_bar(self.loading_bar_queue, width=self.parent._left_width * 0.35)

        self._create_video_queue_widget()

        self.left_layout.addWidget(self.button1, 1, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.left_layout.addWidget(self.loading_bar_single, 1, 1, 1, 4, QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.left_layout.addWidget(self.loading_bar_playlist, 2, 1, 1, 4, QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.left_layout.addWidget(self.loading_bar_queue, 6, 1, 1, 4, QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)

        self.left_layout.addWidget(self.button3, 2, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.left_layout.addWidget(self.button2, 3, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.left_layout.addWidget(self.button4, 6, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.left_layout.addWidget(self.queue_label, 4, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        # self.queue_label.setStyleSheet("QLabel {border: 0px solid #ffffff;}")

        self.button1.clicked.connect(lambda: self.parent._download_single_video(self.parent._get_current_url(), progress_bar=self.loading_bar_single))
        self.button2.clicked.connect(self._add_current_url_to_queue)
        self.button3.clicked.connect(lambda: self.parent._download_playlist(progress_bar=self.loading_bar_playlist))
        self.button4.clicked.connect(lambda: self.parent._download_queue(progress_bar=self.loading_bar_queue))
        self.loading_bar_single.hide()
        self.loading_bar_playlist.hide()
        self.loading_bar_queue.hide()

    def _create_video_queue_widget(self, ):
        self.checklists_widget = QtWidgets.QWidget()
        self.checklists_layout = QtWidgets.QVBoxLayout()
        self.checklists_layout.setStretch(0, 9)
        self.checklists_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.checklists_widget.setLayout(self.checklists_layout)
        # self.checklists_widget.setStyleSheet("QWidget {background-color: #ffffff; border: 1px solid #ffffff; border-radius: 5px;}")

        self.checklists_widget.setFixedWidth(self.parent._left_width)

        self.checklists_scroll = QtWidgets.QScrollArea()
        self.checklists_scroll.setObjectName(u"checklists_scroll")
        self.checklists_scroll.setWidget(self.checklists_widget)
        self.checklists_scroll.setWidgetResizable(True)
        self.checklists_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.checklists_scroll.setStyleSheet("QScrollArea {border: 0px solid #ffffff;}")
        self.checklists_scroll.setFixedHeight(self.parent._height * 0.85 - 30 * 4 - 10)
        self.checklists_scroll.setFixedWidth(self.parent._left_width * 0.95)
        self.left_layout.addWidget(self.checklists_scroll, 5, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

    def _add_current_url_to_queue(self):
        if self.parent._get_current_url() is not None and \
                self.parent._get_current_url() not in self.parent.queue and \
                self.parent._get_current_url() != "about:blank" and \
                self.parent._get_current_url() != "https://www.youtube.com/" and \
                "https://www.youtube.com/feed/" not in self.parent._get_current_url():
            self.parent.queue.append(self.parent._get_current_url())
            button = QtWidgets.QPushButton(self.parent._get_current_url())
            button.setLayoutDirection(QtCore.Qt.LeftToRight)
            button.clicked.connect(lambda: self.remove_checklist_button(button))

            self.checklists_layout.addWidget(
                button
            )

            self.checklists_layout.setAlignment(button, QtCore.Qt.AlignLeft)

            # on button hover change font color to red
            #self.checklists_layout.itemAt(self.checklists_layout.count() - 1).widget().setStyleSheet("QPushButton:hover {color: red;}")

    def remove_checklist_button(self, button):
        self.checklists_layout.removeWidget(button)
        self.parent.queue.remove(button.text())
        button.deleteLater()
