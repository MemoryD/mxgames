#!python3
# -*- coding: utf-8 -*-
'''
@name: life
@author: Memory
@date: 2018/11/19
@document: {"F11": 全屏,
            "空格": 暂停游戏,
            "点击": 复活或者杀死一个生命
            }
'''
import pygame
from mxgames import game
from random import randint

ROWS = 50
SCREEN_SIZE = (500, 500)                                                # 屏幕的尺寸
COLOR = [0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 0xff00ff, 0x00ffff]    # 颜色
UPDATE_TIME = 1500                                                      # 刷新间隔
ALL_INDEX =  [(i,j) for i in range(ROWS) for j in range(ROWS)]

class Life(game.Game):
    def __init__(self, title, size, rows, fps=30):
        super(Life, self).__init__(title, size, fps)
        self.rows = rows                                                # 一条边小格子数量
        self.side = self.screen.get_width() // rows                     # 小格子的边长
        self.lifes = [[False for i in range(rows)] for j in range(rows)]# 生命，True 是活，False 是死
        self.init_lifes()
        self.bind_key(pygame.K_SPACE, self.pause)
        self.bind_click(1, self.reverse)

    def init_lifes(self):                                               # 初始化，随机生成一些生命
        t = self.rows // 3                                              # 控制范围
        for i in range(t, 2*t):
            for j in range(t, 2*t):
                if randint(1, 5) == 1:
                    self.lifes[i][j] = True                             # 设置为活的

    def pause(self, key):
        self.is_pause = not self.is_pause

    def reverse(self, x, y):                                            # 翻转，死的活，活的死
        i = x // self.side
        j = y // self.side
        if i < 0 or j < 0 or i >= self.rows or j >= self.rows:
            return
        self.lifes[i][j] = not self.lifes[i][j]
        rect = pygame.Rect(i*self.side, j*self.side, self.side, self.side)
        if self.lifes[i][j]:
            self.screen.fill(COLOR[randint(0, len(COLOR)-1)], rect)
        else:
            self.screen.fill((0, 0, 0), rect)
        pygame.display.update(rect)

    def neigh_num(self, x, y):                                          # 有几个邻居
        num = 0
        for i in game.EIGHT_NEIGH:
            tx = x + i[0]
            ty = y + i[1]
            if tx > 0 and ty > 0 and tx < self.rows and ty < self.rows:
                if self.lifes[tx][ty]:
                    num += 1
        return num

    def update(self, current_time):                                     # 根据有几个邻居更新生命
        if current_time < self.last_time + UPDATE_TIME or self.is_pause:
            return
        self.last_time = current_time
        self.is_draw = True
        temp_lifes = [[False for i in range(self.rows)] for j in range(self.rows)]
        for i, j in ALL_INDEX:
            num = self.neigh_num(i, j)
            if num == 3:                                            # 3个邻居为活
                temp_lifes[i][j] = True
            elif num == 2:                                          # 两个邻居保持现状
                temp_lifes[i][j] = self.lifes[i][j]                 # 其他情况全死

        self.lifes = temp_lifes

    def draw(self, current_time):                                       # 绘制
        if not self.is_draw or self.is_pause:
            return
        self.is_draw = False
        self.screen.fill((0, 0, 0))                                     # 背景
        for i, j in ALL_INDEX:
            if self.lifes[i][j]:                                    # 绘制活的
                rect = pygame.Rect(i*self.side, j*self.side, self.side, self.side)
                self.screen.fill(COLOR[randint(0, len(COLOR)-1)], rect)

        pygame.display.update()                                         # 刷新屏幕


if __name__ == '__main__':
    print('''
    Welcome to Life Game!
    press SPACE to pause game.
    click MOUSE LEFT BUTTON to create a life, or death a life.
    press F11 to fullscreen.
    ''')
    life = Life("life", SCREEN_SIZE, ROWS)
    life.run()
