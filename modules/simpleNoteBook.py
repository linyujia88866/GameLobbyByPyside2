import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QStatusBar, QVBoxLayout, QWidget


class NoteBook(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('简易笔记本')

        # 创建一个QTextEdit来编辑文本
        self.textEdit = QTextEdit()

        # 创建一个布局
        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)

        # 创建中心控件
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        # 创建菜单栏
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('文件')
        exitAction = QAction('退出', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        # 创建状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # 设置窗口的尺寸
        self.setGeometry(300, 300, 400, 300)
        self.show()


def main():
    app = QApplication(sys.argv)
    mainWindow = NoteBook()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
