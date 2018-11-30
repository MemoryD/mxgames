#!python3
# -*- coding: utf-8 -*-
'''
@name: Schulte
@author: Memory&Xinxin
@date: 2018/11/29
@document: {"F11": 全屏,
            "鼠标左键": 打开一个格子,
            }
'''
import pygame
from mxgames import game
from random import shuffle

SIDE = 80
SCREEN_WIDTH = 5 * SIDE + 2
SCREEN_HEIGHT = 5 * SIDE + 2


class Schulte(game.Game):
    def __init__(self, title, size, fps=20):
        super(Schulte, self).__init__(title, size, fps)
        num = [i for i in range(1, 26)]
        shuffle(num)
        self.num = []
        for i in range(5):
            self.num.append(num[i*5:(i+1)*5])
        self.next_num = 1
        self.start_time = 0
        self.wrong = (-1, -1)
        self.correct = (-1, -1)
        self.num_font = pygame.font.SysFont("Calibri", 50)
        self.bind_click(1, self.click)

    def click(self, x, y):
        if self.end:
            return
        if self.start_time == 0:
            self.start_time = pygame.time.get_ticks()
        i, j = y // SIDE, x // SIDE
        if self.num[i][j] == self.next_num:
            self.next_num += 1
            self.correct = (i, j)
            self.wrong = (-1, -1)
        else:
            self.correct = (-1, -1)
            self.wrong = (i, j)
        self.is_draw = True

    def update(self, current_time):
        if self.end:
            return
        if self.next_num > 25:
            self.next_num = 25
            self.end = True

        if self.start_time == 0:
            time = 0
        else:
            time = (pygame.time.get_ticks() - self.start_time) / 1000
        title = "Schulte ---- next: %d   time: %.2f s" % (self.next_num, time)
        pygame.display.set_caption(title)

    def draw(self, current_time):
        if not self.is_draw:
            return
        self.is_draw = False
        self.screen.fill(0xffffff)

        for i in range(6):
            x1, y1 = (0, i*SIDE), (SCREEN_WIDTH, i*SIDE)
            x2, y2 = (i*SIDE, 0), (i*SIDE, SCREEN_HEIGHT)
            pygame.draw.line(self.screen, 0x000000, x1, y1, 2)
            pygame.draw.line(self.screen, 0x000000, x2, y2, 2)

        if self.wrong != (-1, -1):
            i, j = self.wrong
            rect = pygame.Rect(j*SIDE+1, i*SIDE+1, SIDE-1, SIDE-1)
            self.screen.fill(0xff2222, rect)
        elif self.correct != (-1, -1):
            i, j = self.correct
            rect = pygame.Rect(j*SIDE+1, i*SIDE+1, SIDE-1, SIDE-1)
            self.screen.fill(0x00ff00, rect)

        for i in range(5):
            for j in range(5):
                num = self.num_font.render(str(self.num[i][j]), True, (0, 0, 0))
                rect = pygame.Rect(j*SIDE, i*SIDE, SIDE, SIDE)
                self.screen.blit(num, num.get_rect(center=rect.center))

        pygame.display.update()


if __name__ == '__main__':
    print('''
    Welcome to Schulte!
    click LEFT MOUSE BUTTON to play game.
    press F11 to fullscreen.
    ''')
    sculte = Schulte("Schulte", (SCREEN_WIDTH, SCREEN_HEIGHT))
    sculte.run()
