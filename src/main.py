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

from PySide6.QtCore import QThreadPool
from PySide6.QtCore import QEasingCurve
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtCore import QPoint
from PySide6.QtCore import Qt

exe = ''
if splitext(basename(__file__))[1] == '.pyw'\
        or splitext(basename(__file__))[1] == '.py':
    exe = dirname(realpath(__file__))
elif splitext(basename(__file__))[1] == '.exe':
    exe = dirname(executable)
sys.path.append(exe)

from ytb.youtube import YoutubeDLP

from utils.thread import Worker
from utils.format import format_loading_bar

from widgets.center import CenterWidget
from widgets.settings import SettingsWidget
from widgets.left import LeftWidget
from widgets.right import RightWidget
from widgets.title_bar import TitleBar
from widgets.left_menu import LeftMenu

class SplitWindowYoutubeBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self._height = QApplication.primaryScreen().size().height()
        self._left_bar_width = 50
        self._left_width = round(
            (QApplication.primaryScreen().size().width() - self._left_bar_width) * 0.17,
            0)
        self._right_width = round(
            (QApplication.primaryScreen().size().width() - self._left_bar_width) * 0.83,
            0)

        self.dragPos = QPoint()

        self.title_bar = TitleBar(self)
        self.setContentsMargins(0, 0, 0, 0)

        self.queue = []
        self.worker = None
        self.threadpool = QThreadPool()
        self.progress_bar = None

        self.setObjectName(u"main_window")

        self.setWindowTitle("Youtube Downloader")
        self.setMaximumWidth(QApplication.primaryScreen().size().width())
        print(f"width 0: {self.width()}")

        self.central_widget = CenterWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        self.app_layout = QHBoxLayout()
        self.app_layout.setContentsMargins(0, 10, 0, 10)
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addLayout(self.app_layout)
        self.setLayout(self.main_layout)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.settings_widget = SettingsWidget(parent=self)
        self.left_widget = LeftWidget(parent=self)
        self.left_widget.setObjectName(u"left_widget")

        self.right_widget = RightWidget(parent=self)

        self.ydl = YoutubeDLP()

        self.left_menu_frame = LeftMenu(parent=self)
        self.app_layout.addWidget(self.left_menu_frame)

        self.app_layout.addWidget(self.left_widget)
        self.app_layout.addWidget(self.settings_widget)
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
        if self.settings_widget.width() != 0:
            self.settings_widget.setMinimumWidth(0)
            self.settings_widget.setMaximumWidth(0)
            self.central_widget.setMaximumWidth(QApplication.primaryScreen().size().width())
            self.central_widget.setMinimumWidth(QApplication.primaryScreen().size().width())
            self.setMaximumWidth(QApplication.primaryScreen().size().width())
            self.setMinimumWidth(QApplication.primaryScreen().size().width())
            self.animation = QPropertyAnimation(self.webview, b"maximumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(0)
            self.animation.setEndValue(QApplication.primaryScreen().size().width())
            self.animation.setEasingCurve(QEasingCurve.BezierSpline)
            self.animation.start()
        else:
            self.webview.setMaximumWidth(0)
            self.webview.setMinimumWidth(0)
            self.setMaximumWidth(QApplication.primaryScreen().size().width())
            self.setMinimumWidth(QApplication.primaryScreen().size().width())
            self.left_widget.setMaximumWidth(0)
            self.left_widget.setMinimumWidth(0)
            self.animation = QPropertyAnimation(self.settings_widget, b"minimumWidth")
            self.animation.setDuration(500)
            self.animation.setStartValue(0)
            self.animation.setEndValue(self._right_width + self._left_width)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()

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

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def close(self):
        self.webpage.deleteLater()
        super().close()

if __name__ == "__main__":
    app = QApplication([])
    window = SplitWindowYoutubeBrowser()
    app.exec()
