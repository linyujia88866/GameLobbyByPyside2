import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QTextEdit, QStatusBar, QVBoxLayout, QWidget, QHBoxLayout, \
    QLabel, QRadioButton, QGridLayout, QDialog, QComboBox, QLineEdit, QPushButton, QMessageBox

from utils.database_util import insert_note, query_cates


class NoteBook(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.mode = "read"
        # 设置窗口标题
        self.setWindowTitle('简易笔记本')

        self.titleEdit = QTextEdit()
        self.title_label = QLabel("标题")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.content_label = QLabel("内容")
        self.content_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # 创建一个QTextEdit来编辑文本
        self.textEdit = QTextEdit()

        # 创建一个布局
        layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        h_layout2 = QHBoxLayout()
        h_layout3 = QHBoxLayout()

        self.button_widget = QWidget()
        self.title_widget = QWidget()
        self.content_widget = QWidget()
        self.title_widget.setLayout(h_layout)
        self.content_widget.setLayout(h_layout2)
        self.button_widget.setLayout(h_layout3)

        self.title_widget.setFixedHeight(50)

        h_layout.addWidget(self.title_label)
        h_layout.addWidget(self.titleEdit)

        self.left_widget = QWidget()
        left_layout = QVBoxLayout()
        self.left_widget.setLayout(left_layout)
        left_layout.addWidget(self.content_label, Qt.AlignTop)
        self.left_widget.setFixedWidth(50)
        self.title_label.setFixedWidth(50)

        h_layout2.addWidget(self.left_widget)
        h_layout2.addWidget(self.textEdit)

        layout.addWidget(self.button_widget)
        layout.addWidget(self.title_widget)
        layout.addWidget(self.content_widget)

        # 创建中心控件
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.save_btn = QPushButton("保存笔记")
        self.read_btn = QPushButton("浏览模式")
        self.edit_btn = QPushButton("编辑模式")

        self.save_btn.clicked.connect(self.save_note)
        self.read_btn.clicked.connect(self.read)
        self.edit_btn.clicked.connect(self.edit)

        # # 创建菜单栏
        # menuBar = self.menuBar()
        # fileMenu = menuBar.addMenu('文件')
        # # fileMenu = menuBar.addMenu('退出')
        # saveAction = QAction('保存', self)
        # exitAction = QAction('退出', self)
        # exitAction.triggered.connect(self.close)
        # saveAction.triggered.connect(self.save_note)
        # fileMenu.addAction(saveAction)
        # fileMenu.addAction(exitAction)

        h_layout3.addWidget(self.save_btn)
        h_layout3.addWidget(self.read_btn)
        h_layout3.addWidget(self.edit_btn)
        h_layout3.addWidget(QLabel())

        h_layout3.setStretch(3, 1)

        # 创建状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # 设置窗口的尺寸
        self.setGeometry(300, 300, 400, 300)
        self.setFixedSize(800, 500)
        self.show()
        self.edit()

    def read(self):
        self.titleEdit.setReadOnly(True)
        self.textEdit.setReadOnly(True)
        self.mode = "read"
        self.save_btn.setDisabled(True)
        self.titleEdit.setStyleSheet("background-color: rgb(199, 199, 199);")
        self.textEdit.setStyleSheet("background-color: rgb(199, 199, 199);")

    def edit(self):
        self.titleEdit.setReadOnly(False)
        self.textEdit.setReadOnly(False)
        self.mode = "edit"
        self.save_btn.setDisabled(False)
        self.titleEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit.setStyleSheet("background-color: rgb(255, 255, 255);")

    def save_note(self):
        if self.textEdit.toPlainText().__len__() == 0:
            QMessageBox.warning(None, "提示", "没有内容!", QMessageBox.Ok)
            return
        if self.titleEdit.toPlainText().__len__() == 0:
            QMessageBox.warning(None, "提示", "请先输入标题！", QMessageBox.Ok)
        save_dlg = SaveDialog()
        save_dlg.exec_()
        if SaveDialog.cancel:
            QMessageBox.warning(None, "提示", "取消保存！", QMessageBox.Ok)
            return
        cate = SaveDialog.category
        text = self.textEdit.toPlainText()
        title = self.titleEdit.toPlainText()
        try:
            insert_note(title, text, cate)
        except Exception as err:
            QMessageBox.warning(None, "保存失败", str(err), QMessageBox.Ok)
            return
        QMessageBox.information(None, "提示", "保存成功", QMessageBox.Ok)


class SaveDialog(QDialog):
    category = "默认分类"
    cancel = False

    #
    # _instance = None
    #
    # def __new__(cls, *args, **kwargs):
    #     if cls._instance is None:
    #         # cls._instance = super(SingletonClass, cls).__new__(cls)  # python2.x中，super()函数的使用语法格式
    #         cls._instance = super().__new__(cls)  # python3.x中，super()函数的使用语法格式
    #     return cls._instance

    def __init__(self):
        super().__init__()
        self.setWindowTitle("保存笔记")
        self.lay = QGridLayout()

        self.tip = QLabel("笔记将被保存到以下分类")
        self.slc_radio = QRadioButton("选择已有分类")

        # self.label = QLabel("创建新的分类")
        self.create_radio = QRadioButton("创建新的分类")

        self.setLayout(self.lay)
        self.setFixedSize(300, 150)

        self.comboBox = QComboBox()

        self.slc_radio.setChecked(True)
        self.label = QLabel()

        self.lay.addWidget(self.tip, 0, 0, 1, 5)
        self.lay.addWidget(self.slc_radio, 1, 0, 1, 2)
        self.lay.addWidget(self.create_radio, 1, 3, 1, 2)
        self.lay.addWidget(self.comboBox, 2, 0, 1, 5)

        self.new_label = QLabel("新分类名")
        self.new_label.setAlignment(Qt.AlignCenter)
        self.new_cate_line = QLineEdit()

        self.lay.addWidget(self.new_label, 3, 0, 1, 1)
        self.lay.addWidget(self.new_cate_line, 3, 1, 1, 4)

        self.ok_button = QPushButton("保存")
        self.cancel_button = QPushButton("取消")

        self.lay.addWidget(self.ok_button, 8, 3, 1, 1)
        self.lay.addWidget(self.cancel_button, 8, 4, 1, 1)

        self.ok_button.clicked.connect(self.close)
        self.cancel_button.clicked.connect(self.cancel_save)

        self.lay.addWidget(self.label, 7, 0, 1, 5)

        self.lay.setRowStretch(7, 1)
        self.new_label.hide()
        self.new_cate_line.hide()

        self.slc_radio.toggled.connect(self.change_mode)
        self.comboBox.currentIndexChanged.connect(self.change_category)
        self.mode = False
        self.query_data()
        self.comboBox.setCurrentIndex(0)

    def cancel_save(self):
        SaveDialog.cancel = True
        self.close()

    def query_data(self):
        response = query_cates()
        result = response.get('categories')
        categories = result.replace(" ", "").replace("\n", "").replace(",", "").replace(")", "").replace("]",
                                                                                                         "").replace(
            "[", "").replace("'", "").split("(")

        self.comboBox.addItem("默认分类")
        for category in categories:
            # 添加下拉选项
            if category and category != "默认分类":
                self.comboBox.addItem(category)
        return categories

    def change_category(self):
        SaveDialog.category = self.comboBox.currentText()

    def change_mode(self):
        self.mode = not self.mode
        if self.mode:
            self.comboBox.hide()
            self.new_cate_line.show()
            self.new_label.show()
        else:
            self.comboBox.show()
            self.new_label.hide()
            self.new_cate_line.hide()


def main():
    app = QApplication(sys.argv)
    mainWindow = NoteBook()
    # sd = SaveDialog()
    # sd.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
