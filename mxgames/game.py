#!python3
# -*- coding: utf-8 -*-
'''
@name: game
@author: Memory
@date: 2018/11/20
@document: 为游戏提供一个框架的基类
'''
import pygame
from pygame.locals import *
from sys import exit

FOUR_NEIGH = {"left": (0, -1), "right": (0, 1), "up": (-1, 0), "down": (1, 0)}
EIGHT_NEIGH = list(FOUR_NEIGH.values()) + [(1, 1), (1, -1), (-1, 1), (-1, -1)]
DIRECTION = {pygame.K_UP: "up", pygame.K_LEFT: "left", pygame.K_RIGHT: "right", pygame.K_DOWN: "down"}


def hex2rgb(color):
    b = color % 256
    color = color >> 8
    g = color % 256
    color = color >> 8
    r = color % 256
    return (r, g, b)


class Game(object):
    def __init__(self, title, size, fps=30):
        self.size = size
        pygame.init()
        self.screen = pygame.display.set_mode(size, 0, 32)
        pygame.display.set_caption(title)
        self.keys = {}
        self.keys_up = {}
        self.clicks = {}
        self.timer = pygame.time.Clock()
        self.fps = fps
        self.score = 0
        self.end = False
        self.fullscreen = False
        self.last_time = pygame.time.get_ticks()
        self.is_pause = False
        self.is_draw = True
        self.score_font = pygame.font.SysFont("Calibri", 130, True)

    def bind_key(self, key, action):
        if isinstance(key, list):
            for k in key:
                self.keys[k] = action
        elif isinstance(key, int):
            self.keys[key] = action

    def bind_key_up(self, key, action):
        if isinstance(key, list):
            for k in key:
                self.keys_up[k] = action
        elif isinstance(key, int):
            self.keys_up[key] = action

    def bind_click(self, button, action):
        self.clicks[button] = action

    def pause(self, key):
        self.is_pause = not self.is_pause

    def set_fps(self, fps):
        self.fps = fps

    def handle_input(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys.keys():
                self.keys[event.key](event.key)
            if event.key == pygame.K_F11:                           # F11全屏
                self.fullscreen = not self.fullscreen
                if self.fullscreen:
                    self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN, 32)
                else:
                    self.screen = pygame.display.set_mode(self.size, 0, 32)
        if event.type == pygame.KEYUP:
            if event.key in self.keys_up.keys():
                self.keys_up[event.key](event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in self.clicks.keys():
                self.clicks[event.button](*event.pos)

    def run(self):
        while True:
            for event in pygame.event.get():
                self.handle_input(event)
            self.timer.tick(self.fps)

            self.update(pygame.time.get_ticks())
            self.draw(pygame.time.get_ticks())

    def draw_score(self, color, rect=None):
        score = self.score_font.render(str(self.score), True, color)
        if rect is None:
            r = self.screen.get_rect()
            rect = score.get_rect(center=r.center)
        self.screen.blit(score, rect)

    def is_end(self):
        return self.end

    def update(self, current_time):
        pass

    def draw(self, current_time):
        pass


class Test(Game):
    def __init__(self, title, size, fps=30):
        super(Test, self).__init__(title, size, fps)
        self.bind_key(pygame.K_RETURN, self.press_enter)

    def press_enter(self):
        print("press enter")

    def draw(self, current_time):
        pass


def press_space(key):
    print("press space.")


def click(x, y):
    print(x, y)


def main():
    print(hex2rgb(0xfcf040))
    game = Test("game", (640, 480))
    game.bind_key(pygame.K_SPACE, press_space)
    game.bind_click(1, click)
    game.run()


if __name__ == '__main__':
    main()
