import sys
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox


class ButtonApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个垂直布局
        self.vbox = QVBoxLayout()

        # 循环创建十个按钮
        for i in range(1, 11):
            button = QPushButton('Button {}'.format(i))
            button.clicked.connect(lambda checked, button=button: self.on_button_click(button))
            self.vbox.addWidget(button)

        # 设置主窗口的布局
        self.setLayout(self.vbox)

        # 设置窗口的标题
        self.setWindowTitle('Button Example')

        # 设置窗口的尺寸
        self.setGeometry(100, 100, 300, 200)
        self.show()

    def on_button_click(self, button):
        # 显示点击的按钮文本
        QMessageBox.information(self, 'Button Clicked', 'You clicked: ' + button.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ButtonApp()
    sys.exit(app.exec_())