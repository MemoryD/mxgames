#!python3
# -*- coding: utf-8 -*-
'''
@name: AI Snake
@author: Memory&Xinxin
@date: 2018/11/24
@document: {"F11": 全屏,
            }
'''
from random import choice, randint
from collections import OrderedDict
from mxgames import game
import pygame

ROWS = 8
SIDE = 15
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
        self.step = 0
        self.last_step = 0
        self.snake = [(0, i) for i in range(2, 0, -1)]
        self.world = [[0 for i in range(self.rows)] for j in range(self.rows)]
        self.food = (3, 5)
        self.shortcut = {}
        self.is_shortcut = False
        self.path = {}
        self.init_snake()
        self.create_food()
        self.bind_key(pygame.K_SPACE, self.pause)

    def init_snake(self):
        path = self.build_circle([])
        while path is None:
            x = randint(0, self.rows-1)
            y = randint(0, self.rows-3)
            snake = [(x, i) for i in range(y, y+3)]
            path = self.build_circle(snake)
        self.snake = snake
        self.path = path

    def create_food(self):
        empty = [(i, j) for i in range(self.rows) for j in range(self.rows) if (i, j) not in self.snake and (i, j) != self.food]

        if empty == []:
            self.show_dead()
            return
        self.food = choice(empty)
        while self.food in self.snake:
            self.food = choice(empty)

    def show_dead(self):
        print("Total time: %.2f s" % (pygame.time.get_ticks() / 1000))
        self.draw(0, True)
        self.end = True

    # def cmp(self, now, to):
    #     food_num = self.world[self.food[0]][self.food[1]]
    #     to_num = self.world[to[0]][to[1]]
    #     now_num = self.world[now[0]][now[1]]
    #     if now_num < to_num < food_num:
    #         return True
    #     if to_num < food_num < now_num:
    #         return True
    #     return False

    def shortest(self, wall, head, food, func=None):
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

            for d in DIRE:
                to = (now[0]+d[0], now[1]+d[1])
                if not self.check_pos(to):
                    continue
                if to in walk or to in wait or to in wall:
                    continue
                # if func is not None and not func(now, to):
                #     continue
                wait[to] = now
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
            if self.extension(path, now, wall+[food]):
                now = head
                continue
            now = path[now]

        return path

    def build_circle(self, snake):
        if len(snake) < 3:
            return None
        wall = snake[1:-1]
        path = self.longest(wall, snake[0], snake[-1])
        if path is None or path is {}:
            return None
        if len(path) - 1 != self.rows * self.rows - len(snake):
            return None
        for i in range(1, len(snake)):
            path[snake[i]] = snake[i-1]

        num = 1
        now = snake[0]
        self.world[now[0]][now[1]] = num
        now = path[now]
        while now != snake[0]:
            num += 1
            self.world[now[0]][now[1]] = num
            now = path[now]

        return path

    def shortcut_ok(self, path):
        if path is None or path == {}:
            return False
        circle = False
        snake = list(self.snake)
        head = snake[0]
        last_num = self.world[head[0]][head[1]]
        while head != self.food:
            head = path[head]
            snake.insert(0, head)
            if head != self.food:
                snake.pop()
            tail = snake[-1]
            head_num = self.world[head[0]][head[1]]
            tail_num = self.world[tail[0]][tail[1]]

            if last_num > tail_num:
                if head_num < last_num:
                    if not circle:
                        circle = True
                    else:
                        return False
                if head_num > tail_num:
                    return False
            else:
                if head_num < last_num or head_num > tail_num:
                    return False
            last_num = self.world[head[0]][head[1]]
        return True

    def update(self, current_time):
        if self.end or self.is_pause:
            return
        if self.shortcut != {}:
            next_head = self.shortcut.pop(self.snake[0])
        else:
            next_head = self.path[self.snake[0]]
            self.is_shortcut = False

        self.snake.insert(0, next_head)
        self.step += 1
        if self.food == self.snake[0]:
            self.last_step = self.step
            print("Snake: %d , step: %d, average step: %.2f"%(len(self.snake), self.step, self.step/len(self.snake)))
            self.create_food()
            path = self.build_circle(self.snake)
            if path is not None:
                self.path = path
        else:
            self.snake.pop()

        if self.is_shortcut:
            return
        path = self.shortest(self.snake, self.snake[0], self.food)
        if self.shortcut_ok(path):
            self.shortcut = path
            self.is_shortcut = True

    def draw_side(self, color, x, y, rat=2):
        rect = pygame.Rect(y*self.side*rat, x*self.side*rat, self.side, self.side)
        self.screen.fill(color, rect)
        pygame.display.update(rect)

    def draw_path(self, path, head, food):
        '''测试使用
        '''
        now = head
        last = now

        while now != food:
            for event in pygame.event.get():
                self.handle_input(event)
            self.draw_side(0x0000ff, *now)
            x, y = last[0] + now[0], last[1] + now[1]
            self.draw_side(0x0000ff, x, y, 1)
            last = now
            now = path[now]
            self.timer.tick(30)
        x, y = last[0] + now[0], last[1] + now[1]
        self.draw_side(0x0000ff, x, y, 1)
        self.draw_side(0x0000ff, *now)

    def draw(self, current_time=0, end=False):
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
    snake = AI_Snake("AI Snake", (SCREEN_SIZE), ROWS)
    snake.run()
