from PySide6.QtWidgets import QFileDialog

# imports for BubbleLabel
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLabel

from PySide6.QtGui import QPainterPath
from PySide6.QtGui import QPainter
from PySide6.QtGui import QColor
from PySide6.QtGui import QPen

from PySide6.QtCore import QParallelAnimationGroup
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtCore import QEasingCurve
from PySide6.QtCore import QRectF
from PySide6.QtCore import QPoint
from PySide6.QtCore import Qt
from PySide6.QtCore import Property

class BrowseDirectory(QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFileMode(QFileDialog.Directory)

    def get_path(self):
        return self.getExistingDirectory(self.parent, "Select Directory")

class BubbleLabel(QWidget):

    BackgroundColor = QColor(195, 195, 195)
    BorderColor = QColor(150, 150, 150)

    def __init__(self, *args, **kwargs):
        text = kwargs.pop("text", "")
        super().__init__(*args, **kwargs)

        self.setWindowFlags(Qt.Window | Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        # Set minimum width and height
        self.setMinimumWidth(200)
        self.setMinimumHeight(58)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        layout = QVBoxLayout(self)
        # Top left and bottom right margins (16 below because triangles are included)
        layout.setContentsMargins(8, 8, 8, 16)
        self.label = QLabel(self)
        layout.addWidget(self.label)
        self.setText(text)

    def setText(self, text):
        self.label.setText(text)

    def text(self):
        return self.label.text()

    def stop(self):
        self.hide()
        self.animationGroup.stop()
        self.close()

    def show(self):
        super().show()

        # Window start position
        startPos = QPoint(
            QApplication.primaryScreen().size().width() - self.width() - 100,
            QApplication.primaryScreen().size().height() - self.height())
        endPos = QPoint(
            QApplication.primaryScreen().size().width() - self.width() - 100,
            QApplication.primaryScreen().size().height() - self.height() * 3 - 5)
        self.move(startPos)
        # Initialization animation
        self.initAnimation(startPos, endPos)

    def initAnimation(self, startPos, endPos):
        # Transparency animation
        opacityAnimation = QPropertyAnimation(self, b"opacity")
        opacityAnimation.setStartValue(1.0)
        opacityAnimation.setEndValue(0.0)
        # Set the animation curve
        opacityAnimation.setEasingCurve(QEasingCurve.InQuad)
        opacityAnimation.setDuration(4000)  
        # Moving up animation
        moveAnimation = QPropertyAnimation(self, b"pos")
        moveAnimation.setStartValue(startPos)
        moveAnimation.setEndValue(endPos)
        moveAnimation.setEasingCurve(QEasingCurve.InQuad)
        moveAnimation.setDuration(5000)  
        # Parallel animation group (the purpose is to make the two animations above simultaneously)
        self.animationGroup = QParallelAnimationGroup(self)
        self.animationGroup.addAnimation(opacityAnimation)
        self.animationGroup.addAnimation(moveAnimation)
        # Close window at the end of the animation
        self.animationGroup.finished.connect(self.close)  
        self.animationGroup.start()

    def paintEvent(self, event):
        super(BubbleLabel, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Antialiasing

        rectPath = QPainterPath()                     # Rounded Rectangle
        triPath = QPainterPath()                      # Bottom triangle

        height = self.height() - 8                    # Offset up 8
        rectPath.addRoundedRect(QRectF(0, 0, self.width(), height), 5, 5)
        x = self.width() / 5 * 4
        triPath.moveTo(x, height)                     # Move to the bottom horizontal line 4/5
        # Draw triangle
        triPath.lineTo(x + 6, height + 8)
        triPath.lineTo(x + 12, height)

        rectPath.addPath(triPath)                     # Add a triangle to the previous rectangle

        # Border brush
        painter.setPen(QPen(self.BorderColor, 1, Qt.SolidLine,
                            Qt.RoundCap, Qt.RoundJoin))
        # Background brush
        painter.setBrush(self.BackgroundColor)
        # Draw shape
        painter.drawPath(rectPath)
        # Draw a line on the bottom of the triangle to ensure the same color as the background
        painter.setPen(QPen(self.BackgroundColor, 1,
                            Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(x, height, x + 12, height)

    def windowOpacity(self):
        return super(BubbleLabel, self).windowOpacity()

    def setWindowOpacity(self, opacity):
        super(BubbleLabel, self).setWindowOpacity(opacity)

    # Since the opacity property is not in QWidget, you need to redefine one
    # opacity = pyqtProperty(float, windowOpacity, setWindowOpacity)
    opacity = Property(float, windowOpacity, setWindowOpacity)
