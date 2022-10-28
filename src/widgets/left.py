from regex import search
from regex import findall
from regex import V1

from pyperclip import copy as clipboard_copy
from pyperclip import paste as clipboard_paste

from PySide6.QtWidgets import QWidget
from PySide6 import QtWidgets
from PySide6 import QtCore

from utils.format import format_button
from utils.format import format_loading_bar

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

        self.setMinimumWidth(self.parent.left_width)
        self.setMaximumWidth(self.parent.left_width)

        self.button1 = QtWidgets.QPushButton("Download Current Video")
        self.button1.setMinimumWidth(self.parent.left_width - 10)
        self.button2 = QtWidgets.QPushButton("Add Video to Queue")
        self.button3 = QtWidgets.QPushButton("Download Playlist")
        self.button4 = QtWidgets.QPushButton("Download Queue")
        self.button1 = format_button(self.button1, self.parent.left_width * 0.6)
        self.button2 = format_button(self.button2, self.parent.left_width * 0.6)
        self.button3 = format_button(self.button3, self.parent.left_width * 0.6)
        self.button4 = format_button(self.button4, self.parent.left_width * 0.6)

        self.button1.setObjectName(u"button1")
        self.button2.setObjectName(u"button2")
        self.button3.setObjectName(u"button3")
        self.button4.setObjectName(u"button4")

        self.queue_label = QtWidgets.QLabel("Download Queue")

        self.loading_bar_single = QtWidgets.QProgressBar()
        self.loading_bar_playlist = QtWidgets.QProgressBar()
        self.loading_bar_queue = QtWidgets.QProgressBar()
        
        # TODO: Delete format_loading_bar function and use qss
        self.loading_bar_single = format_loading_bar(self.loading_bar_single, width=self.parent.left_width * 0.35)
        self.loading_bar_playlist = format_loading_bar(self.loading_bar_playlist, width=self.parent.left_width * 0.35)
        self.loading_bar_queue = format_loading_bar(self.loading_bar_queue, width=self.parent.left_width * 0.35)

        self._create_video_queue_widget()

        self.left_layout.addWidget(self.button1, 1, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.left_layout.addWidget(self.loading_bar_single, 1, 1, 1, 4, QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.left_layout.addWidget(self.loading_bar_playlist, 2, 1, 1, 4, QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.left_layout.addWidget(self.loading_bar_queue, 6, 1, 1, 4, QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)

        self.left_layout.addWidget(self.button3, 2, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.left_layout.addWidget(self.button2, 3, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.left_layout.addWidget(self.button4, 6, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.left_layout.addWidget(self.queue_label, 4, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.button1.clicked.connect(lambda: self.parent._download_single_video(progress_bar=self.loading_bar_single))
        self.button2.clicked.connect(self._add_current_url_to_queue)
        self.button3.clicked.connect(lambda: self.parent._download_playlist(progress_bar=self.loading_bar_playlist))
        self.button4.clicked.connect(lambda: self.parent._download_queue(progress_bar=self.loading_bar_queue))
        self.loading_bar_single.hide()
        self.loading_bar_playlist.hide()
        self.loading_bar_queue.hide()

    def _create_video_queue_widget(self, ):
        self.checklists_widget = QtWidgets.QWidget()
        self.checklists_layout = QtWidgets.QVBoxLayout()
        self.checklists_widget.setObjectName(u"checklists_widget")
        self.checklists_layout.setStretch(0, 9)
        self.checklists_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.checklists_widget.setLayout(self.checklists_layout)

        self.checklists_widget.setFixedWidth(self.parent.left_width)

        self.checklists_scroll = QtWidgets.QScrollArea()
        self.checklists_scroll.setObjectName(u"checklists_scroll")
        self.checklists_scroll.setWidget(self.checklists_widget)
        self.checklists_scroll.setWidgetResizable(True)
        self.checklists_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.checklists_scroll.setFixedHeight(self.parent.height * 0.85 - 30 * 4 - 10)
        self.checklists_scroll.setFixedWidth(self.parent.left_width * 0.95)
        self.left_layout.addWidget(self.checklists_scroll, 5, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        
        # queue connect right click
        self.checklists_scroll.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.checklists_scroll.customContextMenuRequested.connect(self._queue_right_click_menu)

    def _queue_right_click_menu(self, pos):
        menu = QtWidgets.QMenu()
        paste_action = menu.addAction("Paste URL(s)")
        action = menu.exec_(self.checklists_scroll.mapToGlobal(pos))
        if action == paste_action:
            paste = clipboard_paste().replace("\n", " ")
            single_url_regex = r"https[-:/a-zA-Z0-9\.\-\?\&\=\_]*"
            if paste.count("https") > 1:
                print("multi")
                for url in findall(single_url_regex, paste, V1):
                    self._add_current_url_to_queue(url)
            else:
                print("single")
                self._add_current_url_to_queue(paste)

    def _add_current_url_to_queue(self, url: str = None):
        if url in (None, False) and self.parent._get_current_url() is not None and \
                self.parent._get_current_url() not in self.parent.queue and \
                self.parent._get_current_url() != "about:blank" and \
                self.parent._get_current_url() != "https://www.youtube.com/" and \
                "https://www.youtube.com/feed/" not in self.parent._get_current_url():
            url = self.parent._get_current_url()
        elif url in (None, False):
            return
        self.parent.queue.append(url)
        button = QtWidgets.QPushButton(url)
        button.setLayoutDirection(QtCore.Qt.LeftToRight)

        button.setStyleSheet("QPushButton {background-color: transparent;}")
        button.clicked.connect(lambda: self.remove_checklist_button(button))

        self.checklists_layout.addWidget(
            button
        )

        # connect right click to context menu for each button
        button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        button.customContextMenuRequested.connect(self._queue_button_right_click_menu)

    def _queue_button_right_click_menu(self, pos):
        button_menu = QtWidgets.QMenu()
        button_menu.setObjectName(u"button_menu")

        # Could not figure out how to add this styling in the qss, so I did it here
        # I think it's not even possible, because the menu is created dynamically
        if self.parent.config["theme"][0] == "dark":
            button_menu.setStyleSheet(
                f"""QMenu {{background-color: rgb(38, 38, 38); border: 1px solid rgb(38, 38, 38);text-align: left;color: white;padding: 5px;padding-left: 20px;padding-right: 20px;}}
                QMenu::item {{background-color: rgb(38, 38, 38); border: 1px solid rgb(38, 38, 38);text-align: left;color: white;}}
                QMenu::item:selected {{background-color: rgb(38, 38, 38); border: 1px solid rgb(38, 38, 38);text-align: left;color: {self.parent.config['accent'][0]};}}
                """
            )
        else:
            button_menu.setStyleSheet(
                f"""QMenu {{background-color: rgb(255, 255, 255); border: 1px solid rgb(255, 255, 255);text-align: left;color: black;padding: 5px;padding-left: 20px;padding-right: 20px;}}
                QMenu::item {{background-color: rgb(255, 255, 255); border: 1px solid rgb(255, 255, 255);text-align: left;color: black;}}
                QMenu::item:selected {{background-color: rgb(255, 255, 255); border: 1px solid rgb(255, 255, 255);text-align: left;color: {self.parent.config['accent'][0]};}}
                """
            )
        remove_action = button_menu.addAction("Remove")
        copy_action = button_menu.addAction("Copy URL")
        action = button_menu.exec_(self.sender().mapToGlobal(pos))
        if action == remove_action:
            self.remove_checklist_button(self.sender())
        elif action == copy_action:
            clipboard_copy(self.sender().text())

    def remove_checklist_button(self, button):
        self.checklists_layout.removeWidget(button)
        self.parent.queue.remove(button.text())
        button.deleteLater()
