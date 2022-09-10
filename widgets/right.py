from PySide2 import QtWebEngineWidgets

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

class RightWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.right_layout = QtWidgets.QGridLayout()
        self.setLayout(self.right_layout)
        self.right_layout.setContentsMargins(10, 0, 0, 0)

        self.setMinimumWidth(self.parent._right_width)
        self.setMaximumWidth(self.parent._right_width)

        self.parent.webview = self._youtube_browser_widget()
        self.right_layout.addWidget(self.parent.webview)
    
    def _youtube_browser_widget(self):
        browser = QtWebEngineWidgets.QWebEngineView()
        browser.load(QtCore.QUrl("https://www.youtube.com"))
        return browser
