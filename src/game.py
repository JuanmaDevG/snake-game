from __future__ import annotations

import pygame as pg
import time
from random import randint, choice
from collections import namedtuple
from enum import Enum
from pygame.math import Vector2

#TODO: futurely, calculate least common multiple in map constructor for perfect screen proportion on each box


class Direction(Enum):
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    UP = (0, -1)


INVERSE_DIRECTION: dict[Direction, Direction] = {
    Direction.RIGHT : Direction.LEFT,
    Direction.DOWN : Direction.UP,
    Direction.LEFT : Direction.RIGHT,
    Direction.UP : Direction.DOWN,
}


DIRECTION_FROM_KEY: dict[int, Direction] = {
    pg.K_UP : Direction.UP,
    pg.K_DOWN : Direction.DOWN,
    pg.K_LEFT : Direction.LEFT,
    pg.K_RIGHT : Direction.RIGHT,
    pg.K_w : Direction.UP,
    pg.K_a : Direction.LEFT,
    pg.K_s : Direction.DOWN,
    pg.K_d : Direction.RIGHT
}


class Point:
    def __init__(self, x: int, y: int, d: Direction = None):
        self.x, self.y = x, y
        if d:
            self.move(d)

    def __iter__(self):
        yield self.x
        yield self.y

    def __eq__(self, p: Point):
        return self.x == p.x and self.y == p.y

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def move(self, d: Direction):
        self.x += d.value[0]
        self.y += d.value[1]

    def get_pivot(self, d: Direction) -> Point:
        p = Point(*self)
        p.move(d)
        return p

    def reloc(self, x: int, y: int):
        self.x, self.y = x, y


class Snake:
    def __init__(self, start_point: Point, length: int = 2):
        self.direction = choice([Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP])
        self.points = [start_point]
        self.score = 0
        self.alive = True

        inv_direction = INVERSE_DIRECTION[self.direction]
        for i in range(length):
            self.points.append(Point(*self.points[i], inv_direction))


    def collide(self):
        head = self.points[0]
        for p in self.points[1:] :
            if head == p:
                self.alive = False
                return


    def redirect(self, d: Direction):
        if self.points[0].get_pivot(d) != self.points[1]:
            self.direction = d


    def move(self):
        backpoint = Point(*self.points[0])
        frontpoint = Point(0,0)
        self.points[0].move(self.direction)
        for p in self.points[1:]:
            backpoint.reloc(*p)
            p.reloc(*frontpoint)
            frontpoint.reloc(*backpoint)


    def eat(self, food: Point) -> bool :
        if self.points[0] == food:
            new_tailblock = self.points[len(self.points) -1] + (self.points[len(self.points) -1] - self.points[len(self.points) -2])
            self.points.append(new_tailblock)
            self.score += 1
            return True
        return False


class Map:
    def __init__(self):
        self.dynamic_resize()


    def dynamic_resize(self):
        px_width, px_height = pg.display.get_window_size()
        self.px_uiheight = px_height // 10
        self.px_boxwidth = (px_height if px_height < px_width else px_width) // 40
        self.width = px_width // self.px_boxwidth
        self.height = (px_height - self.px_uiheight) // self.px_boxwidth
        self.px_drawpoint = Point(
                (px_width % self.px_boxwidth) // 2,
                self.px_uiheight + ((px_height % self.px_boxwidth) // 2))
        self.cur_font = pg.font.Font(pg.font.get_default_font(), size=(self.px_uiheight // 2))
        draw_food.food_radius = self.px_boxwidth // 2


    def is_inbounds(self, p: Point) -> bool:
        if p.x >= 0 and p.x < self.width and p.y >= 0 and p.y < self.height:
            return True
        return False


    def repoint_inbounds(self, p: Point):
        if self.is_inbounds(p): return
        p.x = p.x % self.width
        p.y = p.y % self.height


    def repoint_snake(self, s: Snake):
        for p in s.points:
            self.repoint_inbounds(p)


    def get_px_loc(self, p: Point) -> Point:
        if not self.is_inbounds(p): return None
        return Point(self.px_drawpoint.x + (p.x * self.px_boxwidth), self.px_drawpoint.y + (p.y * self.px_boxwidth))


def reloc_food(food: Point, m: Map, *players: Snake):
    food.reloc(randint(0, m.width -1), randint(0, m.height -1))
    for pl in players:
        for p in pl.points:
            if food == p:
                food.reloc(randint(0, m.width -1), randint(0, m.height -1))


def draw_snake(sf: pg.Surface, m: Map, s: Snake):
    for p in s.points:
        p = m.get_px_loc(p)
        pg.draw.rect(sf, (255, 255, 0), pg.Rect(*p, m.px_boxwidth, m.px_boxwidth))


def draw_food(sf: pg.Surface, game_map: Map, food: Point):
    game_map.repoint_inbounds(food)
    food_loc = game_map.get_px_loc(food)
    food_loc.x += game_map.px_boxwidth // 2
    food_loc.y += game_map.px_boxwidth // 2
    pg.draw.circle(sf, (0, 0, 255), Vector2(*food_loc), draw_food.food_radius)


def main():
    pg.init()
    pg.font.init()
    pg.display.set_caption("Snake game")
    screen = pg.display.set_mode((800, 600), pg.RESIZABLE)
    game_map = Map()
    player = Snake(Point(randint(0, game_map.width -1), randint(0, game_map.height -1)))

    food = Point(0,0)
    reloc_food(food, game_map, player)

    while player.alive :
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key in DIRECTION_FROM_KEY:
                    player.redirect(DIRECTION_FROM_KEY[event.key])
            elif event.type == pg.VIDEORESIZE:
                game_map.dynamic_resize()
            elif event.type == pg.QUIT:
                pg.quit()
                exit()

        player.move()
        game_map.repoint_snake(player)
        player.collide()
        if player.eat(food):
            reloc_food(food, game_map, player)
        screen.fill("black")
        draw_snake(screen, game_map, player)
        draw_food(screen, game_map, food)
        pg.display.flip()
        time.sleep(0.25)

if __name__ == "__main__":
    main()
