import math
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import Qt, QPointF, QLine, QPoint
from PySide2.QtGui import QPainter, QPen, QBrush


class TrajectoryWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 400)
        self.setWindowTitle("炮弹发射轨迹")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)

        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        # 假设初速度为5，重力加速度为9.8，射击角度为45度
        velocity = 5
        angle = 45
        gravity = 9.8
        time = 2  # 假设飞行时间为2秒

        # 计算高度和水平距离
        height = velocity ** 2 * math.sin(2 * angle * math.pi / 180) / gravity
        distance = velocity ** 2 * math.cos(2 * angle * math.pi / 180) / gravity

        # 绘制轨迹
        brush = QBrush(Qt.blue)
        painter.setBrush(brush)
        painter.drawEllipse(QPointF(-distance / 2, -height), 10, 10)
        painter.drawLine(QLine(QPoint(1,2), QPoint(100,100)))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrajectoryWidget()
    window.show()
    sys.exit(app.exec_())