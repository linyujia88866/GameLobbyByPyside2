import sys

from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QPushButton, QApplication)
from PySide2.QtWidgets import QMessageBox

from gen_words import gen_words
from read_words import random_words


class WordsMatch(QWidget):

    def __init__(self):
        super().__init__()
        self.select = []
        self.select_word = ""
        self.select_btn = None
        self.origin_words = []
        self.right_num = 0
        self.buttons = []
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

        for position, name in zip(positions, words):

            if name == '':
                continue
            button = QPushButton(name)
            button.setFixedHeight(100)
            button.clicked.connect(lambda checked, button=button: self.click_btn(button))
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
        self.show()

    def reset(self):
        self.origin_words = random_words(8)
        words = gen_words(self.origin_words)
        print("本关游戏词汇")
        print(words)
        for i, name in enumerate(words):
            self.buttons[i].setText(name)
            self.buttons[i].setDisabled(False)
        self.select_btn = None
        self.select_word = ""
        self.right_num = 0

    def click_btn(self, button):
        text = button.text()
        cur_word = self.select_word + text
        cur_word2 = text + self.select_word
        if cur_word in self.origin_words or cur_word2 in self.origin_words:
            button.setDisabled(True)
            self.select_btn.setDisabled(True)
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
        reply = QMessageBox.information(None, '恭喜过关', '你完成了所有成语的匹配!!!!\n是否再玩一次', QMessageBox.Ok | QMessageBox.Cancel,
                                        QMessageBox.Ok)
        if reply == QMessageBox.Ok:
            print('点击了 OK')
            self.reset()

        else:
            print('点击了 Cancel')


def main():
    app = QApplication(sys.argv)
    ex = WordsMatch()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
