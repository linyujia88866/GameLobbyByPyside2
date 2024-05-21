import sys

from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QApplication, QMainWindow, QTextEdit, QStatusBar, QVBoxLayout, QWidget, QHBoxLayout, \
    QLabel, QRadioButton, QGridLayout, QDialog, QComboBox, QLineEdit, QPushButton, QMessageBox, QTreeWidget, \
    QTreeWidgetItem

from utils.database_util import insert_note, query_cates, query_notes, query_note, update_note


class NotebookMainWin(QDialog):
    def __init__(self):
        super().__init__()
        self.status_bar = None
        self.init_ui()
        self.show()

    def init_ui(self):
        # 设置窗口标题
        self.setWindowTitle('简易笔记本')
        # 设置窗口的尺寸
        self.setGeometry(300, 300, 400, 300)
        self.setFixedSize(800, 500)

        # 创建一个布局
        layout = QGridLayout(self)
        self.setLayout(layout)
        self.note_content_widget = NoteBook()
        self.catalog_widget = Catalogue()
        layout.addWidget(self.note_content_widget, 0, 1, 1, 1)
        layout.addWidget(self.catalog_widget, 0, 0, 1, 1)
        layout.setColumnStretch(1, 1)

        self.catalog_widget.get_content.connect(self.click_title)
        self.note_content_widget.sava.connect(self.save_note)

    def click_title(self, text):
        response = query_note(text)
        content = response.get("content")
        self.note_content_widget.titleEdit.setText(text)
        self.note_content_widget.textEdit.setText(content)

    def save_note(self):
        self.catalog_widget.get_data()
        self.catalog_widget.set_data()


class Catalogue(QWidget):
    get_content = Signal(str)

    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.data = {}
        self.init_ui()

    def init_ui(self):
        # 创建一个QTreeWidget
        self.tree = QTreeWidget()
        # 设置列数
        self.tree.setColumnCount(1)
        # 设置头部信息
        self.tree.setHeaderLabels(['所有笔记'])
        # 创建树节点
        # self.populate_tree()

        self.layout.addWidget(self.tree, 0, 0, 1, 1)
        self.setLayout(self.layout)
        self.get_data()
        self.set_data()

        # 将信号与槽函数连接
        self.tree.itemClicked.connect(self.on_item_clicked)

    def populate_tree(self):
        # 添加顶级节点
        top_level_item = QTreeWidgetItem(self.tree)
        top_level_item.setText(0, 'Top Level 1')
        # top_level_item.setText(1, 'Data 1')
        # 添加子级节点
        child_item = QTreeWidgetItem(top_level_item)
        child_item.setText(0, 'Child 1')
        # child_item.setText(1, 'Child Data 1')
        # 添加另一个顶级节点
        top_level_item2 = QTreeWidgetItem(self.tree)
        top_level_item2.setText(0, 'Top Level 2')
        # top_level_item2.setText(1, 'Data 2')

    def get_data(self):
        self.tree.clear()
        self.data.clear()
        response = query_notes()
        result = response.get('content')

        res_list = (result.replace("[", "").replace("]", "").replace("'", "")
                    .replace("'", "").replace("(", "").replace(")", "").replace(" ", "")
                    .split(","))
        for cat, title in zip(res_list[1::2], res_list[::2]):
            if cat in self.data:
                self.data[cat].append(title)
            else:
                self.data[cat] = []
                self.data[cat].append(title)

    def set_data(self):
        for cat, titles in self.data.items():
            top_level_item = QTreeWidgetItem(self.tree)
            top_level_item.setText(0, cat)

            for title in titles:
                child_item = QTreeWidgetItem(top_level_item)
                child_item.setText(0, title)

    def on_item_clicked(self, item):
        if item.parent() is not None:
            self.get_content.emit(item.text(0))


# noinspection PyTypeChecker
class NoteBook(QWidget):
    sava = Signal()

    def __init__(self):
        super().__init__()
        self.status_bar = None
        self.edit_btn = None
        self.read_btn = None
        self.save_btn = None
        self.left_widget = None
        self.content_widget = None
        self.title_widget = None
        self.button_widget = None
        self.textEdit = None
        self.content_label = None
        self.title_label = None
        self.titleEdit = None
        self.mode = None
        self.init_ui()

    def init_ui(self):
        self.mode = "read"
        # 设置窗口标题
        # self.setWindowTitle('简易笔记本')

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

        # # 创建中心控件
        # central_widget = QWidget()
        # central_widget.setLayout(layout)
        # self.setCentralWidget(central_widget)

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
        # self.status_bar = QStatusBar()
        # self.setStatusBar(self.status_bar)

        # 设置窗口的尺寸
        # self.setGeometry(300, 300, 400, 300)
        # self.setFixedSize(800, 500)
        self.setLayout(layout)
        # self.show()
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
            get_response = query_note(title)
            if "success" in get_response.get("message"):
                update_note(title, text, cate)
            else:

                insert_note(title, text, cate)
            self.sava.emit()
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
        self.new_cate_line.textChanged.connect(self.change_category)
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
        if not self.mode:
            SaveDialog.category = self.comboBox.currentText()
        else:
            SaveDialog.category = self.new_cate_line.text()

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
    mainWindow = NotebookMainWin()
    # mainWindow = NoteBook()
    # sd = SaveDialog()
    # sd.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
