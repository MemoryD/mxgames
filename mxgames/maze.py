#!python3
# -*- coding: utf-8 -*-
'''
@name: Maze
@author: Memory&Xinxin
@date: 2018/11/30
@document: {"F11": 全屏,
            "方向键": 控制人物移动,
            }
'''
import pygame
from mxgames import game
from random import choice

ROWS = 30
COLUMS = 30
SIDE = 22
SCREEN_WIDTH = COLUMS * SIDE
SCREEN_HEIGHT = ROWS * SIDE
FOUR_NEIGH = {pygame.K_UP: (-1, 0), pygame.K_LEFT: (0, -1), pygame.K_RIGHT: (0, 1), pygame.K_DOWN: (1, 0)}
DIRE = {pygame.K_LEFT: pygame.K_RIGHT, pygame.K_RIGHT: pygame.K_LEFT,
        pygame.K_UP: pygame.K_DOWN, pygame.K_DOWN: pygame.K_UP}


class Cell(object):
    def __init__(self, screen, rect):
        self.screen = screen
        self.rect = rect
        self.walls = {key: False for key in FOUR_NEIGH}

        self.visited = 0
        self.type = 'nothing'

    def draw(self):
        if self.type == 'end':
            self.screen.fill(0x11ff11, self.rect)
        elif self.type == 'body':
            pygame.draw.circle(self.screen, 0xff1122, self.rect.center, (SIDE - 4) // 2)

        if not self.walls[pygame.K_LEFT]:
            start = (self.rect.left, self.rect.top)
            end = (self.rect.left, self.rect.top + self.rect.height)
            pygame.draw.line(self.screen, 0x000000, start, end, 2)

        if not self.walls[pygame.K_RIGHT]:
            start = (self.rect.left + self.rect.width - 2, self.rect.top)
            end = (self.rect.left + self.rect.width - 2, self.rect.top + self.rect.height)
            pygame.draw.line(self.screen, 0x000000, start, end, 2)

        if not self.walls[pygame.K_UP]:
            start = (self.rect.left, self.rect.top)
            end = (self.rect.left + self.rect.width, self.rect.top)
            pygame.draw.line(self.screen, 0x000000, start, end, 2)

        if not self.walls[pygame.K_DOWN]:
            start = (self.rect.left, self.rect.top + self.rect.height - 2)
            end = (self.rect.left + self.rect.width, self.rect.top + self.rect.height - 2)
            pygame.draw.line(self.screen, 0x000000, start, end, 2)


class Maze(game.Game):
    def __init__(self, title, size, fps=15):
        super(Maze, self).__init__(title, size, fps)
        self.maze = []
        for i in range(ROWS):
            row = []
            for j in range(COLUMS):
                rect = pygame.Rect(j*SIDE, i*SIDE, SIDE, SIDE)
                row.append(Cell(self.screen, rect))
            self.maze.append(row)
        self.init_maze()

        self.body = (0, 0)
        self.bind_key(list(FOUR_NEIGH.keys()), self.move)
        self.start_time = pygame.time.get_ticks()

    def init_maze(self):
        history = [(0, 0)]
        while history:
            r, c = choice(history)
            self.maze[r][c].visited = True
            history.remove((r, c))
            check = []
            for key in FOUR_NEIGH:
                x, y = r + FOUR_NEIGH[key][0], c + FOUR_NEIGH[key][1]
                if x < 0 or y < 0 or x >= ROWS or y >= COLUMS:
                    continue
                if self.maze[x][y].visited == 1:
                    check.append(key)
                elif self.maze[x][y].visited == 0:
                    history.append((x, y))
                    self.maze[x][y].visited = 2
            if len(check):
                dire = choice(check)
                x, y = r + FOUR_NEIGH[dire][0], c + FOUR_NEIGH[dire][1]
                self.maze[r][c].walls[dire] = True
                self.maze[x][y].walls[DIRE[dire]] = True

        self.maze[0][0].walls[pygame.K_LEFT] = True
        self.maze[ROWS-1][COLUMS-1].walls[pygame.K_RIGHT] = True
        self.maze[0][0].type = "body"
        self.maze[ROWS-1][COLUMS-1].type = "end"

    def move(self, key):
        if self.end:
            return
        r, c = self.body
        x, y = r + FOUR_NEIGH[key][0], c + FOUR_NEIGH[key][1]
        if self.maze[r][c].walls[key] and self.maze[x][y].walls[DIRE[key]]:
            self.body = (x, y)
            self.maze[r][c].type = "nothing"
            self.maze[x][y].type = "body"
            self.is_draw = True

    def update(self, current_time):
        if self.end:
            return
        r, c = self.body
        if (r, c) == (ROWS-1, COLUMS-1):
            self.draw(0)
            self.end = True
        time = (pygame.time.get_ticks() - self.start_time) / 1000
        title = "Maze ---- time: %.2f s" % (time)
        pygame.display.set_caption(title)

    def draw(self, current_time):
        if not self.is_draw or self.end:
            return
        self.is_draw = False
        self.screen.fill(0xffffff)
        for i in range(ROWS):
            for j in range(COLUMS):
                self.maze[i][j].draw()
        pygame.display.update()


if __name__ == '__main__':
    print('''
    Welcome to Maze!
    press ARROW KEYS to play game.
    press F11 to fullscreen.
    ''')
    maze = Maze("Maze", (SCREEN_WIDTH, SCREEN_HEIGHT))
    maze.run()
