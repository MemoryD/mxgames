#!python3
# -*- coding: utf-8 -*-
'''
@name: Snake
@author: Memory&Xinxin
@date: 2018/11/21
@document: {"F11": 全屏,
            "方向键": 控制蛇的方向
            }
'''
import pygame
from mxgames import game
from random import randint, choice

ROWS = 50
COLOR = {"bg": 0x000000, "head": 0xffffff, "body": 0xffffff, "food": 0x00ff00}
SPEED = 120


class Snake(game.Game):
    def __init__(self, title, size, rows, speed, fps=30):
        super(Snake, self).__init__(title, size, fps)
        self.rows = rows
        self.speed = speed
        self.side = size[0] // self.rows
        self.food = (20, 20)
        self.last_food = self.food
        self.snake = [(25, i) for i in range(16, 12, -1)]
        self.screen.fill(COLOR["bg"])
        pygame.display.update()
        self.draw_snake(COLOR["head"], *self.snake[0])
        for body in self.snake[1:]:
            self.draw_snake(COLOR["body"], *body)
        self.direction = ["right"]
        self.next_head = self.snake[0]
        self.bind_key(list(game.DIRECTION.keys()), self.input)

    def create_food(self):
        self.last_food = self.food
        empty = [(i, j) for i in range(self.rows) for j in range(self.rows) if (i, j) not in self.snake and (i, j) != self.food]
        if empty == []:
            self.show_dead()
            self.end = True
            return
        self.food = choice(empty)

    def draw_snake(self, color, x, y):
        rect = pygame.Rect(y*self.side, x*self.side, self.side, self.side)
        self.screen.fill(color, rect)
        pygame.display.update(rect)

    def show_dead(self):
        timer = pygame.time.Clock()
        for body in self.snake:
            self.draw_snake(0xff0000, *body)
            timer.tick(8)

    def input(self, key):
        d1 = game.FOUR_NEIGH[game.DIRECTION[key]]
        d2 = game.FOUR_NEIGH[self.direction[0]]
        if (d1[0]+d2[0],  d1[1]+d2[1]) == (0, 0):
            return
        self.direction.append(game.DIRECTION[key])

    def move(self):
        to = game.FOUR_NEIGH[self.direction[0]]
        self.next_head = (self.snake[0][0]+to[0], self.snake[0][1]+to[1])
        x, y = self.next_head
        if x < 0 or y < 0 or x >= ROWS or y >= ROWS:
            return False
        if self.next_head in self.snake:
            return False
        return True

    def update(self, current_time):
        if current_time < self.last_time + self.speed or self.end:
            return
        self.last_time = current_time
        if self.food == self.snake[0]:
            self.create_food()

        if not self.move():
            self.show_dead()
            self.end = True
            return
        self.draw_snake(COLOR["body"], *self.snake[0])
        self.draw_snake(COLOR["head"], *self.next_head)
        self.draw_snake(COLOR["food"], *self.food)
        if self.last_food != self.snake[-1]:
            self.draw_snake(COLOR["bg"], *self.snake[-1])
            self.snake.pop()
        else:
            self.last_food = (-1, -1)
        self.snake.insert(0, self.next_head)

        if len(self.direction) > 1:
            self.direction.pop(0)


if __name__ == '__main__':
    print('''
    Welcome to Snake!
    press ARROW KEYS to play game.
    ''')
    snake = Snake("snake", (500, 500), ROWS, SPEED)
    snake.run()