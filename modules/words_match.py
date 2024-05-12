import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QWidget, QGridLayout,
                               QPushButton, QApplication)
from PySide2.QtWidgets import QMessageBox, QLabel, QHBoxLayout

from utils.gen_words import gen_words
from utils.read_words import random_words


class WordsMatch(QWidget):

    def __init__(self):
        super().__init__()
        self.select = []
        self.select_word = ""
        self.select_btn = None
        self.origin_words = []
        self.right_num = 0
        self.buttons = []
        self.difficult = "简单"
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(800, 800)
        grid = QGridLayout()
        self.setLayout(grid)

        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']
        self.origin_words = random_words(8)
        words = gen_words(self.origin_words)

        positions = [(i, j) for i in range(5) for j in range(4)]
        print(positions)
        x =1
        for position, name in zip(positions, words):

            if name == '':
                continue
            button = QPushButton(name)
            button.clicked.connect(lambda state=1, b=button: self.click_btn(b))
            button.setFixedHeight(100)
            self.set_default_style(button)
            grid.addWidget(button, *position)
            self.buttons.append(button)

        self.move(300, 150)
        self.setWindowTitle('成语匹配游戏')
        self.close_btn = QPushButton("退出游戏")
        self.reset_btn = QPushButton("重新开始")
        grid.addWidget(self.close_btn, 4, 3)
        grid.addWidget(self.reset_btn, 4, 2)
        self.close_btn.setFixedHeight(50)
        self.reset_btn.setFixedHeight(50)
        self.close_btn.clicked.connect(self.close)
        self.reset_btn.clicked.connect(self.reset)

        hlay = QHBoxLayout()
        label = QLabel("游戏难度：简单  ")

        # self.difficult = "简单"
        easy_btn = QPushButton("简单")
        easy_btn.clicked.connect(lambda: label.setText("游戏难度：简单  "))
        diff_btn = QPushButton("困难")
        diff_btn.clicked.connect(lambda: label.setText("游戏难度：困难  "))

        hlay.addWidget(label)
        hlay.setAlignment(label, Qt.AlignRight)

        hlay.addWidget(easy_btn)
        hlay.addWidget(diff_btn)
        h = QWidget()
        h.setLayout(hlay)
        grid.addWidget(h, 4, 0, 1, 2)

        self.show()

    def reset(self):
        self.origin_words = random_words(8)
        words = gen_words(self.origin_words)
        print("本关游戏词汇")
        print(words)
        for i, name in enumerate(words):
            self.buttons[i].setText(name)
            self.buttons[i].setDisabled(False)
            self.set_default_style(self.buttons[i])
        self.select_btn = None
        self.select_word = ""
        self.right_num = 0

    def click_btn(self, button):
        print("执行了")
        print(button)
        text = button.text()
        cur_word = self.select_word + text
        cur_word2 = text + self.select_word
        if cur_word in self.origin_words or cur_word2 in self.origin_words:
            button.setDisabled(True)
            self.set_green(button)
            self.select_btn.setDisabled(True)
            self.set_green(self.select_btn)
            self.select_btn = None
            self.select_word = ""
            self.right_num = self.right_num + 2
            if self.right_num == 16:
                print("你过关了")
                self.showInformation()
                # QMessageBox.information(None, '恭喜过关', '你完成了所有成语的匹配!!!!')
        else:
            self.select_btn = button
            self.select_word = text

    def showInformation(self):
        reply = QMessageBox.information(None, '恭喜过关', '你完成了所有成语的匹配!!!!\n是否再玩一次',
                                        QMessageBox.Ok | QMessageBox.Cancel,
                                        QMessageBox.Ok)
        if reply == QMessageBox.Ok:
            print('点击了 OK')
            self.reset()

        else:
            print('点击了 Cancel')

    def set_green(self, button):
        button.setStyleSheet("QPushButton {"
                             "  background-color: green;"
                             "  color: white;"
                             "  font-size: 20px;"
                             "  font-weight: bold;"
                             "font-family: 'Microsoft YaHei';"
                             "}")

    def set_default_style(self, button):
        button.setStyleSheet("QPushButton {"
                             "  background-color: #87CEEB;"
                             "  color: white;"
                             "  font-size: 20px;"
                             "  font-weight: bold;"
                             "font-family: 'Microsoft YaHei';"
                             "}")


def main():
    app = QApplication(sys.argv)
    ex = WordsMatch()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
