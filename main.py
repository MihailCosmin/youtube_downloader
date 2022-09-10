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
from widgets.settings import SettingsWidget
from widgets.left import LeftWidget
from widgets.right import RightWidget
from utils.format import format_loading_bar
from utils.format import format_button

# TODO: Re-organize the code, split into modules
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

        self.central_widget = CenterWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.layout.setSpacing(0)

        self.settings_widget = SettingsWidget(parent=self)
        self.settings_widget.hide()
        self.left_widget = LeftWidget(parent=self)
        self.right_widget = RightWidget(parent=self)

        self.ydl = YoutubeDLP()

        self.layout.addWidget(self.left_widget)
        self.layout.addWidget(self.right_widget)

        self.showMaximized()

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
            self.progress_bar = format_loading_bar(self.progress_bar)
            self.progress_bar.setValue(num)
            if num == 100:
                self.progress_bar.setTextVisible(True)
                self.progress_bar.setFormat("Done")
                self.progress_bar.setStyleSheet(
                    "QProgressBar {background-color: #006400; border: 0px solid #006400; border-radius: 5px; text-align: center;}"
                )

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = SplitWindowYoutubeBrowser()
    app.exec_()
