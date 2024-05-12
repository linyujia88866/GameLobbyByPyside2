from pygame import init, image, display, QUIT, quit, event
import sys
import random

# 初始化Pygame
init()

# 设置屏幕尺寸和标题
screen_width = 800
screen_height = 600
screen = display.set_mode((screen_width, screen_height))
display.set_caption("🧩Tower Defense Game")

# 设置颜色
white = (255, 255, 255)

# 加载图片
background_image = image.load("蓝色背景.png")
tower_image = image.load("tower.png")
enemy_image = image.load("enemy.png")

# 定义塔的矩形
tower_rect = tower_image.get_rect()

# 主循环
while True:
    for event in event.get():
        if event.type == QUIT:
            quit()
            sys.exit()

    # 绘制背景
    screen.blit(background_image, (0, 0))

    # 绘制塔
    screen.blit(tower_image, (50, 50))
    tower_rect.topleft = (50, 50)

    # 生成敌人
    if random.randint(1, 100) <= 3:
        enemy_rect = enemy_image.get_rect()
        enemy_rect.topleft = (random.randint(0, screen_width), random.randint(0, screen_height))
        screen.blit(enemy_image, enemy_rect)

    # 更新屏幕
    display.flip()
