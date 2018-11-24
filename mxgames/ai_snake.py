#!python3
# -*- coding: utf-8 -*-
'''
@name: AI Snake
@author: Memory&Xinxin
@date: 2018/11/24
@document: {"F11": 全屏,
            }
'''
from random import choice
from collections import OrderedDict
from mxgames import game
import pygame

ROWS = 14
SIDE = 16
WIDTH = (2*ROWS-1) * SIDE
SCREEN_SIZE = (WIDTH, WIDTH)

DIRE = [(0, -1), (0, 1), (-1, 0), (1, 0)]
LEFT_RIGHT = [(0, -1), (0, 1)]
UP_DOWN = [(-1, 0), (1, 0)]
COLOR = {"bg": 0x000000, "head": 0xff0000, "body": 0xffffff, "food": 0x00ff00}


class AI_Snake(game.Game):
    def __init__(self, title, size, rows, fps=50):
        super(AI_Snake, self).__init__(title, size, fps)
        self.rows = rows
        self.side = size[0] // (2*self.rows-1)
        self.snake = [(0, i) for i in range(2, 0, -1)]
        self.food = (3, 5)
        self.path = {}
        self.create_food()
        self.shortcut = 1
        self.path = self.update_path()
        self.step = 0
        self.last_step = 0
        self.bind_key(pygame.K_SPACE, self.pause)

    def pause(self, key):
        self.is_pause = not self.is_pause
        now = self.snake[0]
        last = now
        num = len(self.path)
        for i in range(num-1):
            for event in pygame.event.get():
                self.handle_input(event)
            self.draw_side(0x0000ff, *now)
            x, y = last[0] + now[0], last[1] + now[1]
            self.draw_side(0x0000ff, x, y, 1)
            last = now
            now = self.path[now]
            self.timer.tick(100)
        self.draw_side(0x0000ff, *now)

    def draw_side(self, color, x, y, rat=2):
        rect = pygame.Rect(y*self.side*rat, x*self.side*rat, self.side, self.side)
        self.screen.fill(color, rect)
        pygame.display.update(rect)

    def show_dead(self):
        print("Total time: %.2f s" % (pygame.time.get_ticks() / 1000))
        self.draw(0, True)
        self.end = True

    def create_food(self):
        if len(self.path) > 6:
            empty = list(self.path.keys())
            length = len(empty) // 3
            empty = empty[:length]
        else:
            empty = [(i, j) for i in range(self.rows) for j in range(self.rows) if (i, j) not in self.snake and (i, j) != self.food]

        if empty == []:
            self.show_dead()
            return
        self.food = choice(empty)
        while self.food in self.snake:
            self.food = choice(empty)

    def shortest(self, wall, head, food):
        walk = {}
        wait = OrderedDict()
        now = (-1, -1)
        last = now
        wait[head] = now

        while wait != {}:
            now, last = wait.popitem(last=False)
            walk[now] = last
            if now == food:
                break
            if last in walk:
                llast = walk[last]
                last_dire = (last[0]-llast[0], last[1]-llast[1])
                if last_dire in DIRE and last_dire != DIRE[0]:
                    DIRE.remove(last_dire)
                    DIRE.insert(0, last_dire)

            neigh = []
            for d in DIRE:
                to = (now[0]+d[0], now[1]+d[1])
                if not self.check_pos(to):
                    continue
                if to in walk or to in wait or to in wall:
                    continue
                neigh.append(to)

            for n in neigh:
                if n == self.food:
                    neigh.remove(n)
                    neigh.insert(0, n)
            for n in neigh:
                wait[n] = now

        if now != food:
            return None

        path = {}
        now = food
        while now != head:
            path[walk[now]] = now
            now = walk[now]

        return path

    def check_pos(self, to):
        result = to[0] < 0 or to[1] < 0 or to[0] >= self.rows or to[1] >= self.rows
        return not result

    def extension(self, path, now, wall):
        will = path[now]
        d1 = (now[0]-will[0], now[1]-will[1])

        if d1 in LEFT_RIGHT:
            dire = UP_DOWN
        else:
            dire = LEFT_RIGHT

        for d in dire:
            one = (now[0]+d[0], now[1]+d[1])
            two = (will[0]+d[0], will[1]+d[1])
            if one == two or not (self.check_pos(one) and self.check_pos(two)):
                continue
            if one in path or two in path or one in wall or two in wall:          # food, head 包不包括?
                continue
            d2 = (one[0]-two[0], one[1]-two[1])
            if d2 == d1:
                path[now] = one
                path[one] = two
                path[two] = will
                return True
        return False

    def longest(self, wall, head, food):
        path = self.shortest(wall, head, food)
        if path is None:
            return None
        now = head
        while now != food:
            if self.extension(path, now, wall):
                now = head
                continue
            now = path[now]
        return path

    def simluate(self, path):
        snake = list(self.snake)
        now = snake[0]
        while now != self.food:
            now = path[now]
            snake.insert(0, now)
            snake.pop()
        p = self.shortest(snake[:-1], snake[0], snake[-1])
        return p is not None and p != {}

    def update_path(self):
        p1, p2 = None, None
        if len(self.snake) > self.rows*(self.rows-2):
            p2 = self.longest(self.snake[:-1], self.snake[0], self.snake[-1])
            return p2

        p1 = self.shortest(self.snake[:-1], self.snake[0], self.food)
        if p1 is not None and p1 != {}:
            if self.simluate(p1):
                return p1
        p2 = self.longest(self.snake[:-1], self.snake[0], self.snake[-1])
        return p2

    def update(self, current_time):
        if self.end or self.is_pause:
            return
        if self.path == {}:
            self.path = self.update_path()
        if self.path is None or self.path == {}:
            self.show_dead()
            return
        next_head = self.path.pop(self.snake[0])
        self.snake.insert(0, next_head)
        self.step += 1
        if self.food == self.snake[0]:
            p = self.update_path()
            if p is None:
                self.snake.pop(0)
                self.step -= 1
                self.path = self.update_path()
            else:
                self.last_step = self.step
                print("Snake: %d , step: %d, average step: %.2f"%(len(self.snake), self.step, self.step/len(self.snake)))
                self.create_food()
                self.path = p
        else:
            self.snake.pop()
        # if self.step - self.last_step > 3*self.rows*self.rows:
        #     self.show_dead()
        #     return

        if self.path is not None and self.food not in list(self.path.keys()):
            self.path = self.update_path()

    def draw(self, current_time, end=False):
        if self.end or self.is_pause:
            return
        self.screen.fill(COLOR["bg"])
        last = self.snake[0]
        color = COLOR["head"] if end else COLOR["body"]
        self.draw_side(color, *last)
        for body in self.snake[1:]:
            self.draw_side(color, *body)
            x, y = last[0] + body[0], last[1] + body[1]
            self.draw_side(color, x, y, 1)
            last = body
            if end:
                self.timer.tick(self.fps)
        if not end:
            self.draw_side(COLOR["food"], *self.food)
        pygame.display.update()


if __name__ == '__main__':
    print('''
    Welcome to AI Snake!
    press SPACE to pause.
    ''')
    ha = AI_Snake("AI Snake", (SCREEN_SIZE), ROWS)
    ha.run()
