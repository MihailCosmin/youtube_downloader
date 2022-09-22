from os.path import dirname
from os.path import realpath
from os.path import splitext
from os.path import basename

import sys
from sys import executable

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QFrame

from PySide6.QtGui import QIcon

from PySide6.QtCore import QThreadPool
from PySide6.QtCore import QEasingCurve
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtCore import Qt

exe = ''
if splitext(basename(__file__))[1] == '.pyw'\
        or splitext(basename(__file__))[1] == '.py':
    exe = dirname(realpath(__file__))
elif splitext(basename(__file__))[1] == '.exe':
    exe = dirname(executable)
sys.path.append(exe)

from utils.thread import Worker
from ytb.youtube import YoutubeDLP
from widgets.center import CenterWidget
from widgets.settings import SettingsWidget
from widgets.left import LeftWidget
from widgets.right import RightWidget

from widgets.title_bar import TitleBar

from utils.format import format_loading_bar


class SplitWindowYoutubeBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self._height = QApplication.primaryScreen().size().height()
        self._left_bar_width = 50
        self._left_width = round(
            (QApplication.primaryScreen().size().width() - self._left_bar_width) * 0.1,
            0)
        self._right_width = round(
            (QApplication.primaryScreen().size().width() - self._left_bar_width) * 0.9,
            0)

        self.titleBar = TitleBar(self)
        self.setContentsMargins(0, self.titleBar.height(), 0, 0)

        self.resize(640, self.titleBar.height() + 480)

        self.queue = []
        self.worker = None
        self.threadpool = QThreadPool()
        self.progress_bar = None

        self.setObjectName(u"main_window")

        self.setWindowTitle("Youtube Downloader")
        self.resize(QApplication.primaryScreen().size())

        self.central_widget = CenterWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)

        self.title_bar_layout = QHBoxLayout()
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.title_bar = QFrame()
        self.title_bar.setLayout(self.title_bar_layout)
        self.title_bar.setObjectName(u"title_bar")
        
        self.app_layout = QHBoxLayout()
        # self.main_layout.addWidget(self.title_bar)
        self.main_layout.addLayout(self.app_layout)
        self.setLayout(self.main_layout)
        self.main_layout.setSpacing(0)

        self.settings_widget = SettingsWidget(parent=self)
        self.settings_widget.hide()
        self.left_widget = LeftWidget(parent=self)
        self.left_widget.setObjectName(u"left_widget")

        self.title_handle_bar = QFrame()
        self.title_handle_bar.setObjectName(u"title_handle_bar")

        # self.title_handle_bar.dragMoveEvent(self.mouseMoveEvent)

        self.minimize_button = QPushButton()
        self.maximize_button = QPushButton()
        self.exit_button = QPushButton()

        self.minimize_button.setObjectName(u"minimize_button")
        self.maximize_button.setObjectName(u"maximize_button")
        self.exit_button.setObjectName(u"exit_button")

        self.minimize_button.setMaximumWidth(20)
        self.maximize_button.setMaximumWidth(20)
        self.exit_button.setMaximumWidth(20)

        self.minimize_button.clicked.connect(self.showMinimized)
        self.maximize_button.clicked.connect(self.toggleMaximizeRestore)
        self.exit_button.clicked.connect(self.close)

        self.title_bar_layout.addWidget(self.title_handle_bar)
        self.title_bar_layout.addWidget(self.minimize_button)
        self.title_bar_layout.addWidget(self.maximize_button)
        self.title_bar_layout.addWidget(self.exit_button)

        # set left widget style
        # self.left_widget.setStyleSheet("background-color: #000000; border: 0px solid #000000; border-radius: 0px;")

        self.right_widget = RightWidget(parent=self)

        self.ydl = YoutubeDLP()

        # add a frame 
        self.left_menu_frame = QFrame()
        self.left_menu_frame.setObjectName(u"left_menu_frame")

        self.left_menu_frame.setMaximumWidth(self._left_bar_width)
        self.left_menu_frame.setMinimumWidth(self._left_bar_width)
        self.left_frame_layout = QVBoxLayout(self.left_menu_frame)

        self.left_menu_frame.settings_button = QPushButton("")
        self.left_menu_frame.settings_button.setIcon(QIcon("icons/icon_settings.png"))
        self.left_menu_frame.settings_button.setIconSize(self.left_menu_frame.settings_button.iconSize() * 2)
        self.left_menu_frame.settings_button.clicked.connect(self.toggle_settings)
        self.left_frame_layout.addWidget(self.left_menu_frame.settings_button)

        self.left_menu_frame.downloads_button = QPushButton("")
        self.left_menu_frame.downloads_button.setIcon(QIcon("icons/cil-vertical-align-bottom.png"))
        self.left_menu_frame.downloads_button.setIconSize(self.left_menu_frame.settings_button.iconSize() * 2)
        self.left_menu_frame.downloads_button.clicked.connect(self.toggle_downloads)
        self.left_frame_layout.addWidget(self.left_menu_frame.downloads_button)

        # left_frame_layout alignment to top
        self.left_frame_layout.addStretch()

        self.app_layout.addWidget(self.left_menu_frame)

        self.app_layout.addWidget(self.left_widget)
        self.app_layout.addWidget(self.right_widget)

        with open("themes/dark.qss", "r", encoding="utf-8") as _:
            stylesheet = _.read()
        self.setStyleSheet(stylesheet)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.showMaximized()

    def toggleMaximizeRestore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def toggle_settings(self):
        pass

    def toggle_downloads(self):
        if self.left_widget.width() != 0:
            self.left_widget.setMinimumWidth(0)
            self.animation = QPropertyAnimation(self.left_widget, b"maximumWidth")
            self.animation.setDuration(500)
            self.animation.setStartValue(self.left_widget.width())
            self.animation.setEndValue(0)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()
        else:
            self.animation = QPropertyAnimation(self.left_widget, b"minimumWidth")
            self.animation.setDuration(500)
            self.animation.setStartValue(0)
            self.animation.setEndValue(self._left_width)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()

    def _download_queue(self, progress_bar=None):
        self.progress_bar = progress_bar
        self.progress_bar.show()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Download starting...")
        self.progress_bar.setValue(0)

        self.worker = Worker(
            self._download_single_queue,
            progress=True,
            console=False,
 
        )
        self.worker.signals.progress.connect(self._progress_bar_update)
        self.worker.signals.finished.connect(self._thread_complete)
        self.threadpool.start(self.worker)

    def _thread_complete(self):
        self.progress_bar.setValue(100)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Done")

    def _download_single_queue(self, progress_callback):
        total = len(self.queue)
        for ind, url in enumerate(self.queue):
            self.ydl.download_video(url)
            progress_callback.emit(round(ind / total * 100, 0))
        progress_callback.emit(100)

    def _download_single_video(self, url, progress_bar=None):
        self.progress_bar = progress_bar
        self.progress_bar.show()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Download starting...")
        self.progress_bar.setValue(0)
        self.worker = Worker(
            self.ydl.download_video,
            url,
            progress=True,
            console=False
        )
        self.worker.signals.progress.connect(self._progress_bar_update)

        self.threadpool.start(self.worker)

    def _download_playlist(self, progress_bar=None):
        self.progress_bar = progress_bar
        self.progress_bar.show()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Download starting...")
        self.progress_bar.setValue(0)
        self.worker = Worker(
            self.ydl.download_playlist,
            self._get_current_url(),
            progress=True,
            console=False
        )

        self.worker.signals.progress.connect(self._progress_bar_update)
        self.worker.signals.finished.connect(self._thread_complete)

        self.threadpool.start(self.worker)

    def _get_current_url(self):
        return self.webview.url().toString().strip()

    def _get_title_of_current_url(self):
        return self.webview.title()

    def _progress_bar_update(self, num):
        """progress_bar_update
        Update progress bar

        Args:
            num (_type_): percentage of the progress bar
        """
        if self.progress_bar is not None:
            self.progress_bar.setTextVisible(False)
            self.progress_bar = format_loading_bar(self.progress_bar, width=self._left_width * 0.35)
            self.progress_bar.setValue(num)
            if num == 100:
                self.progress_bar.setTextVisible(True)
                self.progress_bar.setFormat("Done")

    # def mouseMoveEvent(self, event):
    #     if self.clickPos is not None:
    #         self.window().move(event.globalPos() - self.clickPos)

    # def mouseMoveEvent(self, event):
    #     if self.pressing:
    #         self.end = self.mapToGlobal(event.pos())
    #         self.movement = self.end - self.start
    #         self.setGeometry(self.mapToGlobal(self.movement).x(),
    #                             self.mapToGlobal(self.movement).y(),
    #                             self.width(),
    #                             self.height())
    #         self.start = self.end

if __name__ == "__main__":
    app = QApplication([])
    window = SplitWindowYoutubeBrowser()
    app.exec()
