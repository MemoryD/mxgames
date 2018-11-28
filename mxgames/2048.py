#!python3
# -*- coding: utf-8 -*-
'''
@name: 2048
@author: Memory&Xinxin
@date: 2018/11/21
@document: {"F11": 全屏,
            "方向键": 移动方块
            }
'''
import pygame
from mxgames import game
from random import choice

ROWS = 4
COLOR = {2: 0xd6ecf0, 4: 0xf3e398, 8: 0x6e9b87, 16: 0xD1ABC0, 32: 0x8fa8a5,
        64: 0x59777f, 128: 0xb8d3a8, 256: 0xA2A3A2, 512: 0x465D4B, 1024: 0xbaa19d,
        2048: 0xd3977b, 4096: 0xb36d61, 8192: 0x73222b, "bg": 0x1f1f1f, "num": (10, 10, 10)}
ALL_INDEX = [(i, j) for i in range(ROWS) for j in range(ROWS)]


class Game_2048(game.Game):
    def __init__(self, title, size, fps=30):
        super(Game_2048, self).__init__(title, size, fps)
        self.world = [[0 for i in range(4)] for j in range(4)]
        self.side = size[0] // ROWS
        self.font = pygame.font.SysFont('consolas', 54)
        self.bind_key(list(game.DIRECTION.keys()), self.move)
        self.create()
        self.create()

    def create(self):
        empty = [(i, j) for i in range(ROWS) for j in range(ROWS) if self.world[i][j] == 0]
        if empty != []:
            x, y = choice(empty)
            self.world[x][y] = choice([2, 2, 4])

    def transposition(self, opt):
        if opt == 'down':
            for i in range(3):
                for j in range(3-i):
                    self.world[i][j], self.world[3-j][3-i] = self.world[3-j][3-i], self.world[i][j]
        elif opt == 'up':
            for i in range(1, 4):
                for j in range(i):
                    self.world[i][j], self.world[j][i] = self.world[j][i], self.world[i][j]
        elif opt == 'right':
            for i in range(4):
                for j in range(2):
                    self.world[i][j], self.world[i][3-j] = self.world[i][3-j], self.world[i][j]

    def move(self, key):
        is_move = False
        direction = game.DIRECTION[key]
        self.transposition(direction)
        temp_world = []
        for x in range(ROWS):
            row = [i for i in self.world[x] if i != 0]
            if len(row) > 1:
                for i in range(len(row)-1):
                    if row[i] == row[i+1]:
                        row[i+1] += row[i]
                        row.pop(i)
                        break
            row.extend([0, 0, 0, 0])
            row = row[0:4]
            temp_world.append(row)
            if row != self.world[x]:
                is_move = True

        self.world = temp_world
        self.transposition(direction)
        if is_move:
            self.is_draw = True
            self.create()

    def draw(self, current_time):
        if not self.is_draw:
            return
        self.is_draw = False
        self.screen.fill(COLOR["bg"])
        for i, j in ALL_INDEX:
            if self.world[i][j] != 0:
                rect = pygame.Rect(j*self.side, i*self.side, self.side, self.side)
                num = self.font.render(str(self.world[i][j]), True, COLOR["num"])
                r = num.get_rect(center=rect.center)
                self.screen.fill(COLOR[self.world[i][j]], rect)
                self.screen.blit(num, r)

        pygame.display.update()


if __name__ == '__main__':
    print('''
    Welcome to 2048!
    press ARROW KEYS to play game.
    press F11 to fullscreen.
    ''')
    game_2048 = Game_2048("2048", (480, 480))
    game_2048.run()