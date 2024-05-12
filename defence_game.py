import math
import random
import sys

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication, QWidget, QFrame, QVBoxLayout, QLabel
from PySide2.QtWidgets import QPushButton, QMessageBox, QSizePolicy


def create_button_with_stylesheet(parent, text):
    button = QPushButton(text, parent)
    button.setStyleSheet("QPushButton {"
                         "  background-color: rgb(29, 126, 236); /* 天蓝色 */"
                         "  color: white;"
                         "  border-radius: 4px;"
                         "}"
                         "QPushButton:hover {"
                         "  background-color: rgb(17, 98, 178); /* 深天蓝色 */"
                         "}"
                         "QPushButton:pressed {"
                         "  background-color: rgb(5, 70, 136); /* 更深的天蓝色 */"
                         "}")
    return button


def create_red_button_with_stylesheet(text, parent):
    button = QPushButton(text, parent)
    button.setStyleSheet("QPushButton {"
                         "  background-color: rgb(236, 126, 29); /* 天蓝色 */"
                         "  color: white;"
                         "  border-radius: 4px;"
                         "}"
                         "QPushButton:hover {"
                         "  background-color: rgb(178, 98, 17); /* 深天蓝色 */"
                         "}"
                         "QPushButton:pressed {"
                         "  background-color: rgb(136, 70, 5); /* 更深的天蓝色 */"
                         "}")
    return button

def create_horizontal_line():
    # 创建一个QFrame作为横线
    line = QFrame()

    # 设置线的样式，例如：NoFrame，这样它就不会有边框
    line.setFrameShape(QFrame.HLine)
    line.setFixedWidth(800)

    # 设置线的尺寸策略，例如：Expanding，这样它就会占据可用空间
    line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

    # 如果需要，可以设置线的颜色
    # line.setStyleSheet('color: red;')

    return line


class DefenceGame(QWidget):
    def __init__(self):
        super().__init__()
        # self.progress_bar = QProgressBar()
        self.progress_timer = QTimer(self)
        # self.progress_value = 0
        self.counter = 0
        self.buttons = []
        self.towers = []
        self.attack = 50
        self.score = 0
        self.speed = 50
        self.upgrade_line = 10
        self.upgrade_attack = 50
        self.init_life = 100.0
        self.monster_name = "怪物"

        self.label_attack = QLabel("", self)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('塔防游戏')
        self.setFixedSize(800, 1000)
        self.move(500, 0)
        layout = QVBoxLayout()
        # layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        # 创建横线
        hline = create_horizontal_line()
        hline.setParent(self)
        hline.move(0, 600)


        self.label_attack.move(100, 900)
        self.label_attack.setText(f"当前炮塔攻击力：{self.attack}")
        self.label_attack.setFixedWidth(150)

        self.label_monster_life = QLabel(f"怪物基础生命值：{self.init_life}", self)
        self.label_monster_life.setFixedWidth(150)
        self.label_monster_life.move(250, 900)
        self.init_tower = create_button_with_stylesheet(self, f"炮塔：攻击力{self.attack}")

        self.init_tower.move(400 - self.init_tower.width() // 2, 850)
        # 添加横线到布局中
        # layout.addWidget(hline)

        # self.progress_bar.setValue(0)
        # self.progress_bar.setMaximum(100)

        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(1000)  # 每1000毫秒更新一次进度

        self.show()

    def update_progress(self):
        # self.progress_value += 1
        # if self.progress_value <= 100:
        #     self.progress_bar.setValue(self.progress_value)
        # else:
        #     self.progress_timer.stop()  # 进度达到100%后停止计时器
        self.counter += 1
        button = create_red_button_with_stylesheet(f"{self.monster_name}生命值{self.init_life}", self)
        x = random.randint(0, 800 - button.width())

        self.buttons.append(button)
        # 在这里可以添加更多的按钮设置代码
        button.show()
        # button.y()
        button.move(x, 0)
        for b in self.buttons:
            b.move(b.x(), self.speed + b.y())
            if b.y() > 800:
                self.progress_timer.stop()
                self.show_information()
                return
        if self.counter < 3:
            return
        life = float(self.buttons[0].text().strip(f"{self.monster_name}生命值"))
        if life > 0:
            if (life - self.attack) <= 0:
                self.buttons[0].deleteLater()
                self.score += 1
                self.buttons.pop(0)
            else:
                self.buttons[0].setText(f"{self.monster_name}生命值{(life - self.attack)}")
        else:
            self.buttons[0].deleteLater()
            self.score += 1
            self.buttons.pop(0)
        print(f"当前分数{self.score}")
        if self.score >= self.upgrade_line:
            # 创建消息框对象
            message_box = QMessageBox()

            # 设置消息框的文本
            message_box.setText("炮塔按照不同的方式增加攻击力")

            # 设置消息框的标题
            message_box.setWindowTitle("选择炮塔升级方式")

            # 添加三个按钮，每个按钮对应一个QMessageBox.ButtonRole
            message_box.addButton(f"增加{self.upgrade_attack}攻击力", QMessageBox.AcceptRole)
            message_box.addButton("按二次方增长攻击力", QMessageBox.RejectRole)
            message_box.addButton("攻击力变为原来的1.1倍", QMessageBox.ApplyRole)

            # 显示消息框
            choice = message_box.exec_()
            print(choice)
            if choice == QMessageBox.AcceptRole:
                print(f'User chose 增加{self.upgrade_attack}攻击力')
                self.attack += self.upgrade_attack
            elif choice == QMessageBox.RejectRole:
                print('User chose 按二次方增长攻击力')
                self.attack = math.pow(math.sqrt(self.attack) + 1, 2) // 1
            else:
                print('User chose 攻击力变为原来的1.1倍')
                self.attack = self.attack * 1.1 // 1
            print(f"升级后的攻击力为：{self.attack}")
            self.upgrade_line += 10
            self.init_life += 50
            self.speed += 1
            self.init_tower.setText(f"炮塔：攻击力{self.attack}")
    def show_information(self):
        reply = QMessageBox.information(None, '游戏失败', '怪物攻破了城墙！！',
                                        QMessageBox.Ok | QMessageBox.Cancel,
                                        QMessageBox.Ok)
        if reply == QMessageBox.Ok:
            print('点击了 OK')
            # self.reset()

        else:
            print('点击了 Cancel')


def main():
    app = QApplication(sys.argv)
    ex = ProgressBarExample()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
