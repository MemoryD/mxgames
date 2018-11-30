#!python3
# -*- coding: utf-8 -*-
'''
@name: Snake
@author: Memory&Xinxin
@date: 2018/11/27
@document: {"F11": 全屏,
            "方向键": 控制方块的移动，
            "空格": 暂停
            }
'''
import pygame
from mxgames import game
from random import choice, randint

GAME_ROW = 20
GAME_COL = 14
SIDE = 25
TETRIS_CODE = [[102, 102, 102, 102], [15, 8738, 15, 8738],
              [1094, 116, 1570, 46], [550, 71, 1604, 226],
              [612, 99, 612, 99], [1122, 54, 1122, 54],
              [114, 610, 39, 562]]
MOVE = {pygame.K_LEFT: (0, -1), pygame.K_RIGHT: (0, 1), pygame.K_DOWN: (1, 0)}
SCORE = {0: 0, 1: 10, 2: 30, 3: 50, 4: 80}
COLOR = [0xff2222, 0x11ff11, 0xffcc33, 0x6677ff, 0xff32ff, 0x33ffff]    # 颜色


class Tetris(object):
    def __init__(self):
        self.shape = TETRIS_CODE[randint(0, 6)]
        self.color = choice(COLOR)
        self.pos = [0, 5]
        self.dire = randint(0, 3)
        self.tetris = self.decode(self.shape[self.dire])

    def decode(self, code):
        tetris = []
        x, y = self.pos[0], self.pos[1]
        y = min(max(y, 0), GAME_COL-4)
        x = min(max(x, 0), GAME_ROW-1)
        self.pos = [x, y]
        for i in range(x, x+4):
            for j in range(y, y+4):
                if code % 2 == 1:
                    tetris.append((i, j))
                code = code // 2
                if code == 0:
                    return tetris

    def get_tetris(self):
        return self.tetris

    def check_pos(self, x, y, world):
        if x < 0 or y < 0 or x >= GAME_ROW or y >= GAME_COL:
            return False
        if world[x][y] > 0:
            return False
        return True

    def move(self, key, world):
        if key not in MOVE:
            return False
        tetris = list(self.tetris)
        for i in range(len(tetris)):
            x, y = MOVE[key][0]+tetris[i][0], MOVE[key][1]+tetris[i][1]
            if not self.check_pos(x, y, world):
                return False
            tetris[i] = (x, y)
        self.pos[0] += MOVE[key][0]
        self.pos[1] += MOVE[key][1]
        self.tetris = tetris
        return True

    def transfer(self, key):
        self.dire = (self.dire + 1) % 4
        self.tetris = self.decode(self.shape[self.dire])


class World(game.Game):
    def __init__(self, title, size, fps=30):
        super(World, self).__init__(title, size, fps)
        self.side = SIDE
        self.speed = 600
        self.world = [[0 for i in range(GAME_COL)] for j in range(GAME_ROW)]
        self.tetris = Tetris()
        self.next = Tetris()
        self.dire = -1
        self.is_down = False
        self.move_time = pygame.time.get_ticks()
        self.bind_key(list(MOVE.keys()), self.move)
        self.bind_key(pygame.K_UP, self.transfer)
        self.bind_key(pygame.K_SPACE, self.pause)
        self.bind_key_up(list(MOVE.keys()), self.unmove)

    def move(self, key):
        if key == pygame.K_DOWN:
            self.is_down = True
        else:
            self.dire = key
            self.is_down = False

    def unmove(self, key):
        self.dire = -1

    def transfer(self, key):
        if self.end or self.is_pause:
            return
        self.tetris.transfer(key)
        self.is_draw = True
        self.is_down = False

    def create_next(self):
        self.dire = -1
        self.is_down = False
        for x, y in self.tetris.get_tetris():
            self.world[x][y] = self.tetris.color
        score = 0
        world = []
        for i in range(GAME_ROW):
            row = self.world[i]
            filrow = list(filter(lambda x: x == 0, row))
            if filrow == []:
                world.insert(0, [0 for j in range(GAME_COL)])
                score += 1
            else:
                world.append(row)
        self.world = world
        self.score += SCORE[score]
        row = self.world[0]
        filrow = list(filter(lambda x: x > 0, row))
        if filrow != []:
            self.end = True
            self.is_draw = True
            return True
        self.tetris = self.next
        self.next = Tetris()

    def update(self, current_time):
        if self.end or self.is_pause:
            return

        if self.is_down:
            if not self.tetris.move(pygame.K_DOWN, self.world):
                self.create_next()
            self.is_draw = True
            self.last_time = current_time
            return

        if current_time < self.move_time + 80:
            return

        self.move_time = current_time
        if self.tetris.move(self.dire, self.world):
            self.is_draw = True

        if current_time < self.last_time + self.speed:
            return
        self.last_time = current_time
        self.is_draw = True

        if not self.tetris.move(pygame.K_DOWN, self.world):
            self.create_next()

    def draw_side(self, color, x, y):
        rect = pygame.Rect(y*self.side, x*self.side, self.side, self.side)
        self.screen.fill(0xffffff, rect)
        rect = pygame.Rect(y*self.side+1, x*self.side+1, self.side-2, self.side-2)
        self.screen.fill(color, rect)
        pygame.display.update(rect)

    def draw(self, current_time):
        if not self.is_draw:
            return
        self.is_draw = False

        self.screen.fill(0x000000)
        self.draw_score((0x3c, 0x3c, 0x3c))
        for i in range(GAME_ROW):
            for j in range(GAME_COL):
                if self.world[i][j] > 0:
                    self.draw_side(self.world[i][j], i, j)
        tetris = self.tetris.get_tetris()
        for x, y in tetris:
            self.draw_side(self.tetris.color, x, y)

        if self.end:
            self.draw_score((0x3c, 0x3c, 0x3c))
        pygame.display.update()


if __name__ == '__main__':
    print('''
    Welcome to Tetris!
    press ARROW KEYS to play game.
    press SPACE to pause.
    ''')
    world = World("Tetris", (350, 500))
    world.run()
