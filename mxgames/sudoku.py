#!python3
# -*- coding: utf-8 -*-
'''
@name: Sudoku
@author: Memory&Xinxin
@date: 2018/12/2
@document: {"F11": 全屏,
            "鼠标左键": 点击数字,
            }
'''
import pygame
from mxgames import game
from random import randint

ROWS = 9
SIDE = 60
BLANK = 3
SCREEN_WIDTH = ROWS * SIDE + 2
SCREEN_HEIGHT = ROWS * SIDE + 2
KEY_NUM = [key for key in range(pygame.K_1, pygame.K_9+1)] + [key for key in range(pygame.K_KP1, pygame.K_KP9+1)]


class Sudoku(game.Game):
    def __init__(self, title, size, fps=30):
        super(Sudoku, self).__init__(title, size, fps)
        self.num_font = pygame.font.SysFont("Calibri", 40)
        self.digits = [[] for i in range(9)]
        while not self.make_digits():
            pass
        self.blank = [[False for i in range(ROWS)] for j in range(ROWS)]
        self.blank_num = randint(30, 45)
        self.make_blank()
        self.select = (-1, -1)
        self.tip_num = -1
        self.is_win = False
        self.wrong_pos = []
        self.start_time = 0
        self.answer = [[0 for i in range(ROWS)] for j in range(ROWS)]
        for i in range(ROWS):
            for j in range(ROWS):
                if not self.blank[i][j]:
                    self.answer[i][j] = self.digits[i][j]
        self.bind_click(1, self.click)
        self.bind_key(KEY_NUM, self.input_num)
        self.bind_key(pygame.K_BACKSPACE, self.clear_num)

    def make_digits(self):
        col_lists = [[] for i in range(9)]
        area_lists = [[] for i in range(3)]
        nine = self.random_nine()
        for i in range(9):
            col_lists[i].append(nine[i])
        area_lists[0] = nine[0:3]
        area_lists[1] = nine[3:6]
        area_lists[2] = nine[6:]

        for i in range(8):
            nine = self.random_nine()
            if i % 3 == 2:
                area_lists[0] = []
                area_lists[1] = []
                area_lists[2] = []
            for j in range(9):
                area_index = j // 3
                count = 0
                error = False
                while nine[0] in col_lists[j] or nine[0] in area_lists[area_index]:
                    count += 1
                    if count >= len(nine):
                        error = True
                        break
                    nine.append(nine.pop(0))
                if error:
                    return False
                first = nine.pop(0)
                col_lists[j].append(first)
                area_lists[area_index].append(first)
        self.digits = col_lists
        return True

    def random_nine(self):
        nine = [i + 1 for i in range(9)]
        for i in range(5):
            nine.append(nine.pop(randint(0, 8)))
        return nine

    def make_blank(self):
        num = 0
        while True:
            x, y = randint(0, ROWS-1), randint(0, ROWS-1)
            if self.blank[x][y]:
                continue
            self.blank[x][y] = True
            num += 1
            if num == self.blank_num:
                break

    def click(self, x, y):
        i, j = y // SIDE, x // SIDE
        if self.blank[i][j]:
            self.select = (i, j)
            self.tip_num = -1
        else:
            self.select = (-1, -1)
            self.tip_num = self.answer[i][j]

        self.is_draw = True

    def check_num(self):
        self.wrong_pos = []
        for i in range(0, ROWS, 3):
            for j in range(0, ROWS, 3):
                three = [c[j:j+3] for c in self.answer[i:i+3]]
                nums = [c for d in three for c in d]
                wrong_num = self.check_repeat(nums)
                if wrong_num == []:
                    continue
                for k in range(i, i+3):
                    for l in range(j, j+3):
                        if self.answer[k][l] in wrong_num:
                            self.wrong_pos.append((k, l))
        for i in range(ROWS):
            wrong_num = self.check_repeat(self.answer[i])
            if wrong_num == []:
                continue
            for j in range(ROWS):
                if self.answer[i][j] in wrong_num:
                    self.wrong_pos.append((i, j))

        for j in range(ROWS):
            nums = [num[j] for num in self.answer]
            wrong_num = self.check_repeat(nums)
            if wrong_num == []:
                    continue
            for i in range(ROWS):
                if self.answer[i][j] in wrong_num:
                    self.wrong_pos.append((i, j))
        return self.wrong_pos == []

    def check_repeat(self, nums):
        wrong_num = []
        numset = set(nums)
        for num in numset:
            if num != 0 and nums.count(num) > 1:
                wrong_num.append(num)
        return wrong_num

    def input_num(self, key):
        if self.end: return
        if key > pygame.K_9:
            num = key - pygame.K_KP0
        else:
            num = key - pygame.K_0
        if self.select != (-1, -1):
            x, y = self.select
            if self.answer[x][y] == 0:
                self.blank_num -= 1
            self.answer[x][y] = num
            self.tip_num = num
            self.is_draw = True
            if self.check_num() and self.blank_num == 0:
                self.is_win = True

    def clear_num(self, key):
        if self.end: return
        x, y = self.select
        if self.select != (-1, -1) and self.answer[x][y] != 0:
            self.answer[x][y] = 0
            self.is_draw = True
            self.blank_num += 1
            self.check_num()

    def update(self, current_time):
        if self.end:
            return
        if self.start_time == 0:
            self.start_time = current_time
            time = 0
        else:
            time = (current_time - self.start_time) / 1000
        if self.is_win:
            title = "Sudoku ---- time: %.2f s  DONE!" % (time)
            self.is_draw = True
            self.draw(0)
            self.end = True
        else:
            title = "Sudoku ---- time: %.2f s" % (time)
        pygame.display.set_caption(title)

    def draw(self, current_time):
        if not self.is_draw:
            return
        self.is_draw = False
        self.screen.fill(0xffffff)
        if self.select != (-1, -1):
            i, j = self.select
            rect = pygame.Rect(j*SIDE, i*SIDE, SIDE, SIDE)
            self.screen.fill(0xf3b649, rect)
        if self.tip_num != -1:
            for i in range(ROWS):
                for j in range(ROWS):
                    if self.tip_num != self.answer[i][j]:
                        continue
                    rect = pygame.Rect(j*SIDE, i*SIDE, SIDE, SIDE)
                    self.screen.fill(0xf3b649, rect)

        for i, j in self.wrong_pos:
            rect = pygame.Rect(j*SIDE, i*SIDE, SIDE, SIDE)
            self.screen.fill(0xff2200, rect)

        for i in range(ROWS+1):
            x1, y1 = (0, i*SIDE), (SCREEN_WIDTH, i*SIDE)
            x2, y2 = (i*SIDE, 0), (i*SIDE, SCREEN_HEIGHT)
            if i % 3 == 0:
                pygame.draw.line(self.screen, 0x000000, x1, y1, 3)
                pygame.draw.line(self.screen, 0x000000, x2, y2, 3)
            else:
                pygame.draw.line(self.screen, 0x333333, x1, y1, 1)
                pygame.draw.line(self.screen, 0x333333, x2, y2, 1)

        for i in range(ROWS):
            for j in range(ROWS):
                if self.answer[i][j] == 0:
                    continue
                if self.blank[i][j]:
                    num = self.num_font.render(str(self.answer[i][j]), True, game.hex2rgb(0x0000ff))
                else:
                    num = self.num_font.render(str(self.answer[i][j]), True, game.hex2rgb(0x222232))
                rect = pygame.Rect(j*SIDE, i*SIDE, SIDE, SIDE)
                self.screen.blit(num, num.get_rect(center=rect.center))
        pygame.display.update()


if __name__ == '__main__':
    print('''
    Welcome to Sudoku!
    click LEFT MOUSE BUTTON to select a cell.
    press NUMBER KEYS to input a number.
    press BACKSPACE to clear a number.
    ''')
    sudoku = Sudoku("Sudoku", (SCREEN_WIDTH, SCREEN_HEIGHT))
    sudoku.run()
