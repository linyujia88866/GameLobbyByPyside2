import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton

from sub_windows import SubWindow1, SubWindow2, SubWindow3, SubWindow4, SubWindow5


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.sub_window5 = None
        self.sub_window1 = None
        self.sub_window2 = None
        self.sub_window3 = None
        self.sub_window4 = None

    def init_ui(self):
        self.setWindowTitle('主界面')
        self.setFixedSize(200, 600)

        button1 = QPushButton('打开子界面1', self)
        button2 = QPushButton('打开子界面2', self)
        button3 = QPushButton('打开子界面3', self)
        button4 = QPushButton('打开子界面4', self)
        button5 = QPushButton('打开子界面5', self)
        button1.clicked.connect(self.open_sub_window1)
        button2.clicked.connect(self.open_sub_window2)
        button3.clicked.connect(self.open_sub_window3)
        button4.clicked.connect(self.open_sub_window4)
        button5.clicked.connect(self.open_sub_window5)
        button1.move(50, 50)
        button2.move(50, 100)
        button3.move(50, 150)
        button4.move(50, 200)
        button5.move(50, 250)

        # 其他按钮类似...

        self.show()

    def open_sub_window1(self):
        self.sub_window1 = SubWindow1()
        self.sub_window1.show()

    def open_sub_window2(self):
        self.sub_window2 = SubWindow2()
        self.sub_window2.show()

    def open_sub_window3(self):
        self.sub_window3 = SubWindow3()
        self.sub_window3.show()

    def open_sub_window4(self):
        self.sub_window4 = SubWindow4()
        self.sub_window4.show()

    def open_sub_window5(self):
        self.sub_window5 = SubWindow5()
        self.sub_window5.show()


# ...其他打开子界面的方法

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())