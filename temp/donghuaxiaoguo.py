from PySide2.QtWidgets import QApplication, QWidget, QSizePolicy
from PySide2.QtCore import Qt, Signal, QRectF, QPoint, QTimer, QSize
from PySide2.QtGui import QPainter, QPen, QBrush


class AnimatedCircleWidget(QWidget):
    # 定义信号，当动画结束时发出
    animationFinished = Signal()

    def __init__(self, parent=None):
        super(AnimatedCircleWidget, self).__init__(parent)
        self.center = QPoint(50, 50)
        self.radius = 10
        self.animationTimer = QTimer(self)
        self.animationTimer.timeout.connect(self.animate)
        self.animationStep = 0
        self.maxRadius = 50
        self.animationTimer.start(100)  # 每0.1秒更新一次

    def sizeHint(self):
        return QSize(100, 100)

    def animate(self):
        self.radius += 1
        if self.radius > self.maxRadius:
            self.animationTimer.stop()
            self.animationFinished.emit()  # 动画结束，发出信号
        self.update()  # 请求重绘部件

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.blue, 2)
        painter.setPen(pen)
        brush = QBrush(Qt.cyan)
        painter.setBrush(brush)
        circleRect = QRectF(self.center.x() - self.radius, self.center.y() - self.radius,
                            2 * self.radius, 2 * self.radius)
        painter.drawEllipse(circleRect)


if __name__ == "__main__":
    app = QApplication([])
    widget = AnimatedCircleWidget()
    widget.show()
    widget.animationFinished.connect(app.quit)  # 动画结束后退出应用
    app.exec_()