import sys

from PySide2.QtGui import Qt
from PySide2.QtWidgets import QApplication, QProgressBar, QVBoxLayout, QWidget


class ProgressBarExample(QWidget):
    def __init__(self):
        super().__init__()
        self.progress_bar = QProgressBar()

        self.progress_bar.setAlignment(Qt.AlignCenter)  # 设置进度条文本居中对齐
        self.progress_bar.setRange(0, 100)  # 设置进度条的范围
        self.progress_bar.setValue(50)  # 设置当前进度
        self.progress_bar.setStyleSheet("QProgressBar {"  # 设置进度条样式
                                        "text-align: center;"  # 文本居中
                                        "border: none;"  # 无边框
                                        "color: white;"  # 文本颜色
                                        "background-color: #222222;"  # 背景颜色
                                        "}"
                                        "QProgressBar::chunk {"  # 进度条已完成部分样式
                                        "background-color: #00ff00;"  # 已完成部分颜色
                                        "}")

        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        self.show()


def main():
    app = QApplication(sys.argv)
    window = ProgressBarExample()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
