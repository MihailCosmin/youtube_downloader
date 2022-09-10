from os.path import join
from os.path import dirname
from os.path import realpath
from os.path import splitext
from os.path import basename
from os.path import expanduser

import sys
from sys import executable

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtWebEngineCore
from PySide2 import QtWebEngineWidgets

from PySide2.QtCore import QThreadPool

from adblockparser import AdblockRules

exe = ''
if splitext(basename(__file__))[1] == '.pyw'\
        or splitext(basename(__file__))[1] == '.py':
    exe = dirname(realpath(__file__))
elif splitext(basename(__file__))[1] == '.exe':
    exe = dirname(executable)
sys.path.append(exe)

from thr.thread import Worker
from ytb.youtube import YoutubeDLP
from widgets.center import CenterWidget
from widgets.left import LeftWidget

# TODO: Make loading bars work
# TODO: Make ads traffic filter work 

# with open("easylist.txt", "r", encoding="utf-8") as _:
#     raw_rules = _.readlines()
#     rules = AdblockRules(raw_rules)

# class WebEngineUrlRequestInterceptor(QtWebEngineCore.QWebEngineUrlRequestInterceptor):
#     def interceptRequest(self, info):
#         url = info.requestUrl().toString()
#         if rules.should_block(url):
#             print("block::::::::::::::::::::::", url)
#             info.block(True)

class SplitWindowYoutubeBrowser(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._height = QtWidgets.QApplication.primaryScreen().size().height()
        self._left_width = round(QtWidgets.QApplication.primaryScreen().size().width() * 0.1, 0) + 100
        self._right_width = round(QtWidgets.QApplication.primaryScreen().size().width() * 0.9, 0) - 140

        self.queue = []
        self.worker = None
        self.threadpool = QThreadPool()
        self.progress_bar = None

        # Traffic filter
        # self.interceptor = WebEngineUrlRequestInterceptor()
        # QtWebEngineWidgets.QWebEngineProfile.defaultProfile().setRequestInterceptor(self.interceptor)

        self.setWindowTitle("Youtube Downloader")
        self.resize(QtWidgets.QApplication.primaryScreen().size())

        self._create_central_widget()       
        self._create_left_widget()
        self._create_right_widget()
        self._create_settings_widget()

        self.ydl = YoutubeDLP()

        self.layout.addWidget(self.left_widget)
        self.layout.addWidget(self.right_widget)

        self.showMaximized()

    def _create_central_widget(self):
        self.central_widget = CenterWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.layout.setSpacing(0)

    def _create_left_widget(self):
        self.left_widget = LeftWidget(parent=self)

    def _create_right_widget(self):
        self.right_widget = QtWidgets.QWidget()
        self.right_layout = QtWidgets.QVBoxLayout(self.right_widget)
        self.right_layout.setContentsMargins(10, 0, 0, 0)

        self.right_widget.setMinimumWidth(self._right_width)
        self.right_widget.setMaximumWidth(self._right_width)

        self.webview = self._youtube_browser_widget()
        self.right_layout.addWidget(self.webview)

    def _create_settings_widget(self):
        self.settings_widget = QtWidgets.QWidget()
        self.settings_layout = QtWidgets.QVBoxLayout(self.settings_widget)
        self.settings_top_widget = QtWidgets.QWidget()
        self.settings_top_layout = QtWidgets.QHBoxLayout(self.settings_top_widget)       
        self.settings_layout.addWidget(self.settings_top_widget)
        self.settings_top_widget.setStyleSheet("QWidget {border: 1px solid #ffffff; border-radius: 5px;}")
        self.settings_top_widget.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=5, xOffset=2, yOffset=2))

        self.settings_layout.setStretch(0, 9)

        self.settings_widget.setMinimumWidth(self._right_width)
        self.settings_widget.setMaximumWidth(self._right_width)

        self.settings_bottom_widget = QtWidgets.QWidget()
        self.settings_bottom_layout = QtWidgets.QHBoxLayout(self.settings_bottom_widget)
        self.settings_layout.addWidget(self.settings_bottom_widget)
        self.settings_bottom_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.apply_button = QtWidgets.QPushButton("Apply")
        self._format_button(self.apply_button)
        self.settings_bottom_layout.addWidget(self.apply_button)
        self.apply_button.clicked.connect(self._show_browswer)

        self.close_button = QtWidgets.QPushButton("Close")
        self._format_button(self.close_button)
        self.settings_bottom_layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self._show_browswer)

        self.apply_button.move(self._right_width - self.apply_button.width() - 10, 0)
        self.close_button.move(self._right_width - self.close_button.width() - 10, 30)

        self.settings_widget.hide()

    def _format_button(self, button, width: int = 80, height: int = 30):
        button.setFixedHeight(height)
        button.setFixedWidth(width)
        button.move(0, 0)
        button.raise_()
        button.setFlat(True)
        button.setStyleSheet("QPushButton {background-color: #000000; color: #ffffff; border: 1px solid #ffffff; border-radius: 5px;}")
        button.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=5, xOffset=2, yOffset=2))
        button.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        button.setWindowOpacity(0.5)
        button.setMouseTracking(True)

        # on hover 
        button.enterEvent = lambda event: button.setWindowOpacity(1)
        button.leaveEvent = lambda event: button.setWindowOpacity(0.5)

        # on hover make text green
        button.enterEvent = lambda event: button.setStyleSheet("QPushButton {background-color: #000000; color: #00ff00; border: 1px solid #ffffff; border-radius: 5px;}")
        button.leaveEvent = lambda event: button.setStyleSheet("QPushButton {background-color: #000000; color: #ffffff; border: 1px solid #ffffff; border-radius: 5px;}")

    def _format_loading_bar(self, bar, height: int = 26):
        bar.setMinimum(0)
        bar.setMaximum(100)
        bar.setValue(0)
        bar.setTextVisible(False)
        bar.setMinimumHeight(height)
        bar.setFixedWidth(self._left_width * 0.35)
        bar.setStyleSheet("QProgressBar {border: 1px solid #ffffff; border-radius: 5px; text-align: right;}")
        bar.setStyleSheet("QProgressBar::chunk {background-color: #000000; width: 10px;}")
        bar.setAlignment(QtCore.Qt.AlignCenter)

    def _format_button_transparent(self, button):
        button.setWindowOpacity(0.0)
        button.setStyleSheet("QPushButton {border: 0px solid #ffffff;}")

    def _show_settings(self):
        self.webview.hide()
        self.right_layout.addWidget(self.settings_widget)
        self.settings_widget.show()

    def _show_browswer(self):
        self.settings_widget.hide()
        self.webview.show()

    def _youtube_browser_widget(self):
        browser = QtWebEngineWidgets.QWebEngineView()
        browser.load(QtCore.QUrl("https://www.youtube.com"))
        return browser

    def _download_queue(self, progress_bar=None):
        self.progress_bar = progress_bar
        self.progress_bar.show()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Download starting...")
        self.progress_bar.setStyleSheet("QProgressBar {text-align: center;}")
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
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Done")
        self.progress_bar.setStyleSheet("QProgressBar {background-color: #006400; border: 0px solid #006400; border-radius: 5px; text-align: center;}")

    def _add_current_url_to_queue(self):
        if self._get_current_url() is not None and \
                self._get_current_url() not in self.queue and \
                self._get_current_url() != "about:blank" and \
                self._get_current_url() != "https://www.youtube.com/" and \
                "https://www.youtube.com/feed/" not in self._get_current_url():
            self.queue.append(self._get_current_url())
            button = QtWidgets.QPushButton(self._get_current_url())
            button.setLayoutDirection(QtCore.Qt.LeftToRight)
            button.clicked.connect(lambda: self._remove_checklist_button(button))

            self.checklists_layout.addWidget(
                button
            )

            self.checklists_layout.setAlignment(button, QtCore.Qt.AlignLeft)

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
        self.progress_bar.setStyleSheet("QProgressBar {text-align: center;}")
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
        self.progress_bar.setStyleSheet("QProgressBar {text-align: center;}")
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
            self._format_loading_bar(self.progress_bar)
            self.progress_bar.setValue(num)
            if num == 100:
                self.progress_bar.setTextVisible(True)
                self.progress_bar.setFormat("Done")
                self.progress_bar.setStyleSheet("QProgressBar {background-color: #006400; border: 0px solid #006400; border-radius: 5px; text-align: center;}")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = SplitWindowYoutubeBrowser()
    app.exec_()
