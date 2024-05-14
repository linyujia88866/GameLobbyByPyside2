from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QPushButton, QProgressBar, QVBoxLayout


class MyProgressButton(QWidget):
    def __init__(self, parent=None, text=""):
        super().__init__()

        self.progress = QProgressBar(self)
        self.progress.setFixedHeight(10)
        self.button = QPushButton(text, self)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.start_progress()

    def start_progress(self):
        self.progress.setVisible(True)  # 显示进度条
        self.progress.setTextVisible(False)
        self.progress.setValue(100)
        self.progress.setAlignment(Qt.AlignCenter)  # 设置进度条文本居中对齐
        self.progress.setRange(0, 100)  # 设置进度条的范围
        self.progress.setStyleSheet("QProgressBar {"  # 设置进度条样式
                                    "text-align: center;"  # 文本居中
                                    "border: none;"  # 无边框
                                    "color: white;"  # 文本颜色
                                    "background-color: #999999;"  # 背景颜色
                                    "}"
                                    "QProgressBar::chunk {"  # 进度条已完成部分样式
                                    "background-color: #ff5500;"  # 已完成部分颜色
                                    "}")
        # self.setFixedHeight(50)

    def setText(self, text):
        self.button.setText(text)


    def text(self):
        return self.button.text()

    def setValue(self, value):
        self.progress.setValue(value)


    def setDisbled(self, x):
        self.button.setEnabled(x)
        self.progress.setEnabled(x)
        self.button.setStyleSheet("QPushButton {"  # 设置进度条样式
                                    "background-color: #999999;"  # 背景颜色
                                    "}"
                        )
