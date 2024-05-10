from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton


class SubWindow1(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(200, 200)
        self.setWindowTitle('填写成语')
        layout = QVBoxLayout()
        layout.addWidget(QLabel('这是子界面1'))
        close_button = QPushButton('关闭', self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)


class SubWindow2(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(200, 200)
        self.setWindowTitle('子界面1')
        layout = QVBoxLayout()
        layout.addWidget(QLabel('这是子界面1'))
        close_button = QPushButton('关闭', self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)


class SubWindow3(QDialog):
    def __init__(self):
        super().__init__()
        print(111)
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(200, 200)
        self.setWindowTitle('子界面1')
        layout = QVBoxLayout()
        layout.addWidget(QLabel('这是子界面1'))
        close_button = QPushButton('关闭', self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)


class SubWindow4(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(200, 200)
        self.setWindowTitle('子界面1')
        layout = QVBoxLayout()
        layout.addWidget(QLabel('这是子界面1'))
        close_button = QPushButton('关闭', self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)


class SubWindow5(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(200, 200)
        self.setWindowTitle('子界面1')
        layout = QVBoxLayout()
        layout.addWidget(QLabel('这是子界面1'))
        close_button = QPushButton('关闭', self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)  # 其他四个子界面类类似...
