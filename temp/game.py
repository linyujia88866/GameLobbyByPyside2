import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton


class TowerDefenseGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个按钮
        self.button = QPushButton('Start Game', self)
        self.button.clicked.connect(self.start_game)
        self.button.move(100, 50)

        # 设置窗口属性
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Tower Defense')
        self.show()

    def start_game(self):
        # 游戏开始的逻辑
        print('Game started!')


# 创建应用程序实例
app = QApplication(sys.argv)

# 创建游戏实例并运行
game = TowerDefenseGame()
sys.exit(app.exec_())