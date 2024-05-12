import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide2.QtCore import QThread, QTimer, Slot
from PySide2.QtCore import Signal


class ButtonGenerator(QThread):
    buttonCreated = Signal(int)

    def __init__(self, parent=None):
        super(ButtonGenerator, self).__init__(parent)
        self.counter = 0

    def run(self):
        # 创建一个定时器，每1000毫秒（1秒）触发一次
        self.timer = QTimer()
        self.timer.timeout.connect(self.create_button)
        self.timer.start(1000)

    def create_button(self):
        print("=")
        self.counter += 1
        # 发射buttonCreated信号，并传递计数器值作为参数
        self.buttonCreated.emit(self.counter)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(800, 800)
        self.button_generator = ButtonGenerator()
        self.button_generator.start()
        self.button_generator.buttonCreated.connect(self.on_button_created)
        self.button_generator.start()

    @Slot(int)
    def on_button_created(self, counter):
        print(counter)
        button = QPushButton(f"Button {counter}")
        # 在这里可以添加更多的按钮设置代码
        button.show()  # 或者将按钮添加到布局中


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())