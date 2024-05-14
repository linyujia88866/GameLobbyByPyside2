from PySide2.QtCore import Signal
from PySide2.QtWidgets import QWidget, QPushButton, QApplication


class MyWidget(QWidget):
    # 定义信号
    customSignal = Signal(int)  # 信号可以传递一个整数参数

    def __init__(self):
        super(MyWidget, self).__init__()
        self.button = QPushButton('Press Me', self)

        # 连接信号到槽
        self.button.clicked.connect(self.on_button_clicked)

        # 连接自定义信号到槽
        self.customSignal.connect(self.on_custom_signal)

    def on_button_clicked(self, checked):
        # 当按钮被点击时，发射自定义信号
        self.customSignal.emit(42)

    def on_custom_signal(self, value):
        # 槽函数处理自定义信号
        print(f"Custom signal received with value: {value}")


# 应用程序入口
app = QApplication([])
widget = MyWidget()
widget.show()
app.exec_()