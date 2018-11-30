#!python3
# -*- coding: utf-8 -*-
'''
@name: Mine
@author: Memory&Xinxin
@date: 2018/11/29
@document: {"F11": 全屏,
            "鼠标左键": 打开一个格子,
            "鼠标右键": 标记一个地雷,
            "鼠标左右键齐按": 打开本格子周围8个格子
            }
'''
import pygame
from mxgames import game
from random import randint

ROWS = 20
COLUMS = 20
SIDE = 25
MINE_NUM = 66
SCREEN_WIDTH = ROWS * SIDE
SCREEN_HEIGHT = COLUMS * SIDE

CLOSE = 0
OPEN = 1
EMPTY = 2
NUMBER = 3
MINE = 4
COLOR = {CLOSE: 0x5555ff, OPEN: 0xaaaaff, NUMBER: 0xaaaaff, MINE: 0x222222}
FOUR_NEIGH = [(0, -1), (0, 1), (-1, 0), (1, 0)]
EIGHT_NEIGH = FOUR_NEIGH + [(1, 1), (1, -1), (-1, 1), (-1, -1)]
# NUM_COLOR = [0x3377ff,  0xffff22, 0x22ffff, 0x22ff22, 0xff2222, 0xff22ff, 0xff9922, 0x2222ff]
NUM_COLOR = [(0x33, 0x77, 0xff), (0xff, 0x22, 0x22), (0xff, 0x22, 0xff), (0xff, 0xff, 0x22), 
(0x22, 0xff, 0xff), (0x22, 0xff, 0x22), (0xff, 0x99, 0x22), (0x22, 0x22, 0xff)]


class Grid(object):
    def __init__(self, screen, t, rect):
        self.screen = screen
        self.type = t
        self.rect = rect
        self.number = 0
        self.flag = False
        self.open = False
        self.dead = False
        self.win = False
        self.num_font = pygame.font.SysFont("Calibri", 22, True)

    def draw(self):
        if not self.open:
            self.screen.fill(COLOR[CLOSE], self.rect)
            if not self.flag:
                return
            start = (self.rect.left + self.rect.width // 3, self.rect.top + self.rect.height // 6)
            end = (self.rect.left + self.rect.width // 3, self.rect.top + self.rect.height * 5 // 6)
            mid = (self.rect.left + self.rect.width // 3, self.rect.top + self.rect.height // 2)
            tail = (self.rect.left + self.rect.width * 4 // 5, self.rect.top + self.rect.height // 2)
            pygame.draw.line(self.screen, 0xffffff, start, end, 2)
            pygame.draw.polygon(self.screen, 0xff0000, [start, mid, tail])
        elif self.type == EMPTY:
            self.screen.fill(COLOR[OPEN], self.rect)
        elif self.type == NUMBER:
            self.screen.fill(COLOR[OPEN], self.rect)
            num = self.num_font.render(str(self.number), True, NUM_COLOR[self.number-1])
            self.screen.blit(num, num.get_rect(center=self.rect.center))
        elif self.type == MINE:
            if self.dead:
                self.screen.fill(0xff1122, self.rect)
            elif self.win:
                self.screen.fill(0x11ff11, self.rect)
            else:
                self.screen.fill(COLOR[OPEN], self.rect)
            pygame.draw.circle(self.screen, COLOR[MINE], self.rect.center, self.rect.width // 3)


class Mine(game.Game):
    def __init__(self, title, size, fps=25):
        super(Mine, self).__init__(title, size, fps)
        self.left_mine = MINE_NUM
        self.flag_num = 0
        self.left_btn = False
        self.right_btn = False
        self.start_time = 0
        self.world = []
        self.init_mine()
        self.bind_click(1, self.click_left)
        self.bind_click(3, self.click_right)

    def init_mine(self):
        for i in range(ROWS):
            row = []
            for j in range(COLUMS):
                rect = pygame.Rect(j*SIDE+1, i*SIDE+1, SIDE-2, SIDE-2)
                row.append(Grid(self.screen, EMPTY, rect))
            self.world.append(row)

        for i in range(MINE_NUM):
            x = randint(0, ROWS-1)
            y = randint(0, COLUMS-1)
            while self.world[x][y].type != EMPTY:
                x = randint(0, ROWS-1)
                y = randint(0, COLUMS-1)
            self.world[x][y].type = MINE

        for i in range(ROWS):
            for j in range(COLUMS):
                self.set_num(i, j)

    def set_num(self, i, j):
        if self.world[i][j].type == MINE:
            return

        num = 0
        for neigh in EIGHT_NEIGH:
            x, y = i + neigh[0], j + neigh[1]
            if x < 0 or y < 0 or x >= ROWS or y >= COLUMS:
                continue
            if self.world[x][y].type == MINE:
                num += 1
        if num > 0:
            self.world[i][j].type = NUMBER
            self.world[i][j].number = num

    def click_left(self, x, y):
        if self.start_time == 0:
            self.start_time = pygame.time.get_ticks()
        self.left_btn = True

    def click_right(self, x, y):
        if self.start_time == 0:
            self.start_time = pygame.time.get_ticks()
        self.right_btn = True

    def open(self, i, j):
        if i < 0 or j < 0 or i >= ROWS or j >= COLUMS:
            return
        if self.world[i][j].open or self.world[i][j].flag:
            return
        if self.world[i][j].type == MINE:
            if not self.world[i][j].flag:
                self.world[i][j].dead = True
                self.draw_mine(self.world[i][j], False)
                self.show_end(False)
                return
        elif self.world[i][j].type == NUMBER:
            self.world[i][j].open = True
        elif self.world[i][j].type == EMPTY:
            self.world[i][j].open = True
            for neigh in EIGHT_NEIGH:
                x, y = i + neigh[0], j + neigh[1]
                self.open(x, y)
        self.is_draw = True

    def show_end(self, win=False):
        self.draw(0)
        self.end = True
        for i in range(ROWS):
            for j in range(COLUMS):
                if self.world[i][j].type != MINE:
                    continue
                self.draw_mine(self.world[i][j], win)
                self.timer.tick(30)

    def draw_mine(self, mine, win):
        mine.open = True
        mine.win = win
        mine.draw()
        pygame.display.update()

    def update(self, current_time):
        if self.end:
            return
        if self.start_time == 0:
            time = 0
        else:
            time = (pygame.time.get_ticks() - self.start_time) / 1000
        title = "Mine ---- mine: %d   time: %.2f" % (self.left_mine, time)
        pygame.display.set_caption(title)

        x, y = pygame.mouse.get_pos()
        i, j = y // SIDE, x // SIDE
        if self.left_btn and self.right_btn:
            if self.world[i][j].open and self.world[i][j].type == NUMBER:
                for neigh in EIGHT_NEIGH:
                    x, y = i + neigh[0], j + neigh[1]
                    self.open(x, y)
        elif self.left_btn:
            self.open(i, j)
        elif self.right_btn:
            if not self.world[i][j].open:
                self.world[i][j].flag = not self.world[i][j].flag
                if self.world[i][j].flag:
                    self.flag_num += 1
                else:
                    self.flag_num -= 1
                if self.world[i][j].type == MINE:
                    if self.world[i][j].flag:
                        self.left_mine -= 1
                    else:
                        self.left_mine += 1
                self.is_draw = True

        if self.left_mine == 0 and self.flag_num == MINE_NUM:
            self.show_end(True)
        self.left_btn = False
        self.right_btn = False

    def draw(self, current_time):
        if not self.is_draw or self.end:
            return
        self.is_draw = False
        self.screen.fill(0x000000)
        for i in range(ROWS):
            for j in range(COLUMS):
                self.world[i][j].draw()
        pygame.display.update()


if __name__ == '__main__':
    print('''
    Welcome to Mine!
    click LEFT MOUSE BUTTON to open a cell.
    click RIGHT MOUSE BUTTON to mark a mine.
    click the LEFT and RIGHT MOUSE BUTTONS simultaneously to open all the cells around.
    press F11 to fullscreen.
    ''')
    mine = Mine("Mine", (SCREEN_WIDTH, SCREEN_HEIGHT))
    mine.run()
