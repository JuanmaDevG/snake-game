import pygame as pg
import time
import asyncio
from random import randint, choice
from collections import namedtuple
from enum import Enum
from __future__ import annotations
from pygame.math import Vector2

#TODO: futurely, calculate least common multiple in map constructor for perfect screen proportion on each box


class Direction(Enum):
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    UP = (0, -1)

    INVERSE: dict[Direction, Direction] = {
        Direction.RIGHT : Direction.LEFT,
        Direction.DOWN : Direction.UP,
        Direction.LEFT : Direction.RIGHT,
        Direction.UP : Direction.DOWN,
    }

    FROM_KEY: dict[int, Direction] = {
        pg.K_UP : Direction.UP,
        pg.K_DOWN : Direction.DOWN,
        pg.K_LEFT : Direction.LEFT,
        pg.K_DOWN : Direction.DOWN
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

    def move(d: Direction):
        self.x, self.y = direction.value

    def get_pivot(self, d: Direction) -> Point:
        p = Point(*self)
        p.move(d)
        return p

    def reloc(x: int, y: int):
        self.x, self.y = x, y


class Snake:
    def __init__(self, start_point: Point, length: int = 2):
        self.direction = choice([Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP])
        self.points = [start_point]
        self.score = 0
        self.alive = True

        inv_direction = Direction.INVERSE[self.direction]
        for i in range(length):
            self.points.append(Point(*self.points[i], inv_direction))


    def collide(self):
        head = self.points[0]
        for p in range(1, len(self.points)):
            if head == p:
                self.alive = False
                return
    

    def redirect(self, d: Direction):
        if self.points[0].get_pivot(d) != self.points[1]:
            self.direction = d


    def move(self):
        prevp = Point(*self.points[0])
        nextp = Point(0,0)
        self.points[0].move(self.direction)
        for p in self.points[1:]:
            nextp.reloc(*p)
            p.reloc(*prevp)
            prevp.reloc(*nextp)


class Map:
    def __init__(self, px_width: int, px_height: int):
        self.px_uiheight = px_height // 10
        self.px_boxwidth = (px_height if px_height < px_width else px_width) // 40
        self.width = px_width // px_boxwidth
        self.height = px_height // px_boxwidth
        self.px_drawpoint = Point((px_width % px_boxwidth) // 2, (px_height % px_boxheight) // 2)
        self.cur_font = pg.font.Font(pg.font.get_default_font(), size=(self.px_uiheight // 2))
        draw_food.food_radius = self.px_boxwidth // 2


    def dynamic_resize():
        px_width, px_height = pg.display.get_window_size()
        self.px_uiheight = px_height // 10
        self.px_boxwidth = (px_height if px_height < px_width else px_width) // 40
        self.width = px_width // px_boxwidth
        self.height = px_height // px_boxwidth
        self.map_drawpoint = Point((px_width % px_boxwidth) // 2, (px_height % px_boxheight) // 2)
        self.cur_font = pg.font.Font(pg.font.get_default_font(), size=(self.px_uiheight // 2))
        draw_food.food_radius = self.px_boxwidth // 2


    def repoint_inbounds(p: Point):
        if p.x >= 0 and p.x < self.width and p.y <= 0 and p.y < self.height:
            return
        p.x = p.x % self.width
        p.y = p.y % self.height


    def repoint_snake(s: Snake):
        for p in s.points:
            repoint_inbounds(p)


def reloc_food(food: Point, m: Map, *players: Snake):
    food.reloc(randint(0, m.width -1), randint(0, m.height -1))
    #TODO: food does not collide


def draw_arrow(sf: pg.Surface, box_loc: Point, d: Direction, m: Map):
def draw_snake(sf: pg.Surface, m: Map, s: Snake):
    for p in s.points:
        pg.draw.rect(sf, 
                     (255, 255, 0),
                     pg.Rect(m.px_drawpoint.x + (p.x * m.px_boxwidth),
                             m.px_drawpoint.y + (p.y * m.px_boxwidth),
                             m.px_boxwidth,
                             m.px_boxwidth))
    #Draw the direction arrow
    head = s.points[0]
    pg.draw.polygon(sf,
                    (255, 0, 0),
                    [Vector2(m.px_drawpoint.x + (p.x * m.px_boxwidth) + (m.px_boxwidth // 2),
                             m.px_drawpoint.y + (p.y * m.px_boxwidth) + 2),
                     Vector2(m.px_drawpoint.x + (p.x * m.px_boxwidth) + (m.px_boxwidth // 3),
                             m.px_drawpoint.y + (p.y * m.px_boxwidth) + (m.px_boxwidth -2)),
                     Vector2(m.px_drawpoint.x + (p.x * m.px_boxwidth) + ((m.px_boxwidth // 3) *2),
                             m.px_drawpoint.y + (p.y * m.px_boxwidth) + (m.px_boxwidth -2))])


def draw_food(sf: pg.Surface, food: Point):
    pg.draw.circle(sf, (0, 0, 255), Vector2(*food), draw_food.food_radius)


#TODO: make custom event to send event queue
async def run_player(sf: pg.Surface, player: Snake, game_map: Map, food: Point):
    draw_call = pygame.event.custom_type()
    while player.alive:
        await asyncio.sleep(0.5)
        player.move()
        if player.points[0] == food:
        pygame.event.post(draw_call)


async def main():
    pg.init()
    pg.font.init()
    pg.display.set_caption("Snake game")
    screen = pg.display.set_mode((800, 600))
    game_map = Map(*pg.display.get_window_size())
    player = Snake(Point(randint(0, game_map.width -1), randint(0, game_map.height -1)))
    draw_food.food_radius = game_map.px_boxwidth // 2

    #TODO: generate food does not collide with snake
    for player
    food = Point(randint(0, game_map.width -1), randint(

    for event in pg.event.wait():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        screen.fill("black")
        draw_snake(player)
        draw_food(

        pg.display.flip()


asyncio.run(main())
