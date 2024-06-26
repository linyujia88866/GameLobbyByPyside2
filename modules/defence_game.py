import math
import random
import sys

from PySide2.QtCore import QTimer, QLine, QPoint, QRectF, Signal
from PySide2.QtGui import QPainter, QPen, Qt, QBrush
from PySide2.QtWidgets import QApplication, QWidget, QFrame, QVBoxLayout, QLabel, QDialog
from PySide2.QtWidgets import QPushButton, QMessageBox, QSizePolicy

from component.button_with_progress import MyProgressButton


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
    button = MyProgressButton(parent, text)
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
    button.button.setFixedHeight(30)
    button.setFixedHeight(50)
    button.setFixedWidth(120)

    # button.progress.value()
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


# noinspection PyTypeChecker
class DefenceGame(QDialog):
    animationFinished = Signal()

    def __init__(self):
        super().__init__()
        # self.progress_bar = QProgressBar()
        self.close_btn = None
        self.reset_btn = None
        self.step = 1
        self.init_tower = None
        self.label_monster_life = None
        self.game_timer = QTimer(self)
        # self.progress_value = 0
        self.counter = 0  # 前三轮炮塔不攻击，用于计算当前轮次
        self.buttons = []  # 当前已出现的怪物
        self.towers = []  # 所有的炮塔
        self.attack = 50  # 当前的炮塔攻击力
        self.score = 0  # 击杀怪物数量
        self.speed = 50  # 怪物行进速度
        self.grade = 1  # 当前等级
        self.upgrade_line = 10  # 升级门槛
        self.upgrade_attack = 50  # 本次升级增加的攻击力
        self.init_life = 100.0  # 怪物初始生命值
        self.monster_name = "怪物"  # 怪物的名称
        self.bullet_x = 0  # 子弹初始位置，也就是炮塔初始位置
        self.bullet_y = 350  # 子弹初始位置，也就是炮塔初始位置
        self.radius = 10  # 子弹的半径

        self.label_attack = QLabel("", self)
        self.label_monster_life = QLabel("", self)
        self.label_score = QLabel("", self)
        self.label_upgrade_target = QLabel("", self)
        self.end_point_x = 0  # 子弹的结束位置，也就是当前最靠前的怪兽的位置
        self.end_point_y = 0
        self.to_delete_monster = None  # 指向生命已经降为0的怪兽，并会在下一轮攻击之前回收

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('塔防游戏')
        self.setFixedSize(800, 1000)
        self.animationFinished.connect(self.refresh_game)
        self.move(500, 0)
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 创建横线
        h_line = create_horizontal_line()
        h_line.setParent(self)
        h_line.move(0, 600)

        self.label_attack.move(100, 900)
        self.label_attack.setFixedWidth(200)
        self.label_monster_life.setFixedWidth(200)
        self.label_monster_life.move(300, 900)

        self.label_score.setFixedWidth(200)
        self.label_score.move(500, 900)
        self.label_upgrade_target.setFixedWidth(200)
        self.label_upgrade_target.move(100, 950)

        self.init_tower = create_button_with_stylesheet(self, "基础炮塔")
        self.init_tower.move(400 - self.init_tower.width() // 2, 850)

        self.close_btn = QPushButton("退出游戏", self)
        self.close_btn.setParent(self)
        self.reset_btn = QPushButton("重新开始", self)
        self.close_btn.clicked.connect(self.close)
        self.reset_btn.clicked.connect(self.reset)

        self.reset_btn.move(500, 950)
        self.close_btn.move(620, 950)

        self.set_data_frame()

        self.game_timer.timeout.connect(self.create_new_monster)
        self.game_timer.start(1000)  # 每1000毫秒更新一次进度

        self.show()

    def close_window(self):
        print("-------")

    def set_data_frame(self):
        self.label_attack.setText(f"基础炮塔攻击力：{self.attack}")
        self.label_monster_life.setText(f"怪物基础生命值：{self.init_life}")
        self.label_score.setText(f"击杀怪物：{self.score}")
        self.label_upgrade_target.setText(f"击杀怪物数量达到 {self.upgrade_line} 可升级")

    def create_new_monster(self):
        self.counter += 1

        button = create_red_button_with_stylesheet(f"{self.monster_name}{self.counter}", self)
        button.setParent(self)
        button.progress.setMaximum(self.init_life)
        button.progress.setValue(button.progress.maximum())
        x = random.randint(0, 800 - button.width())

        self.buttons.append(button)
        # 在这里可以添加更多的按钮设置代码
        button.show()
        button.move(x, 0)
        for b in self.buttons:
            b.move(b.x(), self.speed + b.y())
            # if b.y() > 800:
            #     self.game_timer.stop()
            #     self.show_information()
            #     return

        if self.buttons[0].y() > 800:
            self.game_timer.stop()
            self.show_information()
            return

        if self.counter > 3:
            self.draw_attack()

    def refresh_game(self):
        self.bullet_x = 0
        self.bullet_y = 350
        self.update()
        self.attack_and_refresh()
        self.set_data_frame()
        self.upgrade()
        self.game_timer.start(300)

    def draw_attack(self):
        self.game_timer.stop()
        self.end_point_x = -(self.width() / 2 - self.buttons[0].x()) + self.buttons[0].width() / 2
        self.end_point_y = -self.height() / 2 + self.buttons[0].y() + self.buttons[0].height() / 2 + 20

        self.bullet_x = 0
        self.bullet_y = 350
        self.step = (self.end_point_y - 350) / 10

        self.animationTimer = QTimer(self)
        self.animationTimer.timeout.connect(self.animate)
        self.animationTimer.start(50)

    def animate(self):
        self.bullet_y += self.step
        self.bullet_x = 0 + (self.end_point_x - 0) / (self.end_point_y - 350) * (self.bullet_y - 350)

        if math.fabs(self.bullet_y - self.end_point_y) < 1:
            self.animationTimer.stop()
            self.animationFinished.emit()
            # self.animationFinished.emit()  # 动画结束，发出信号
        self.update()

    def attack_and_refresh(self):
        # if self.to_delete_monster is not None:
        #     self.to_delete_monster.deleteLater()
        #     self.to_delete_monster = None
        life = float(self.buttons[0].progress.value())
        if life > 0:
            if (life - self.attack) <= 0:
                self.buttons[0].setValue(0)
                self.buttons[0].setDisbled(True)
                self.to_delete_monster = self.buttons.pop(0)
                self.to_delete_monster.deleteLater()
                self.score += 1

            else:
                self.buttons[0].setValue((life - self.attack))
        else:
            self.buttons[0].deleteLater()
            self.buttons.pop(0)
            self.attack_and_refresh()

    def upgrade(self):
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

            if choice == QMessageBox.AcceptRole:
                self.attack += self.upgrade_attack
            elif choice == QMessageBox.RejectRole:
                self.attack = math.pow(math.sqrt(self.attack) + 1, 2) // 1
            else:
                self.attack = self.attack * 1.1 // 1

            self.upgrade_line += 10
            self.upgrade_attack = self.upgrade_attack + 50
            self.init_life += 50
            self.speed += 1

            self.set_data_frame()

    def reset(self):
        self.score = 0
        self.speed = 50
        self.grade = 1
        for button in self.buttons:
            button.deleteLater()
        self.counter = 0
        self.init_life = 100
        self.attack = 50
        self.upgrade_attack = 50
        self.upgrade_line = 10
        self.buttons = []
        self.set_data_frame()
        self.game_timer.start(1000)

    def show_information(self):
        reply = QMessageBox.information(None, '游戏失败', '怪物攻破了城墙！！\n是否重新开始？',
                                        QMessageBox.Ok | QMessageBox.Cancel,
                                        QMessageBox.Ok)
        if reply == QMessageBox.Ok:
            self.reset()

    def paintEvent(self, event):
        # painter = QPainter(self)
        # painter.setRenderHint(QPainter.Antialiasing)
        # painter.translate(self.width() / 2, self.height() / 2)
        #
        # pen = QPen(Qt.black, 2)
        # painter.setPen(pen)
        # # 绘制轨迹
        # brush = QBrush(Qt.blue)
        # painter.setBrush(brush)
        #
        # painter.drawLine(QLine(QPoint(0, 350), QPoint(self.end_point_x, self.end_point_y)))

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        pen = QPen(Qt.blue, 2)
        painter.setPen(pen)
        brush = QBrush(Qt.cyan)
        painter.setBrush(brush)
        circle_rect = QRectF(self.bullet_x - self.radius, self.bullet_y - self.radius,
                             2 * self.radius, 2 * self.radius)
        painter.drawEllipse(circle_rect)


def main():
    app = QApplication(sys.argv)
    ex = DefenceGame()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
