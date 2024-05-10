from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


class ExampleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 初始化界面代码...
        pass

    def showInformation(self):
        reply = QMessageBox.information(self, '信息标题', '这是一条信息', QMessageBox.Ok | QMessageBox.Cancel,
                                        QMessageBox.Ok)
        if reply == QMessageBox.Ok:
            print('点击了 OK')
        else:
            print('点击了 Cancel')


if __name__ == '__main__':
    app = QApplication([])
    ex = ExampleApp()
    ex.showInformation()
    ex.show()
    app.exec_()