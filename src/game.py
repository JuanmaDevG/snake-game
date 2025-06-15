import pygame as pg
import time
from dataclasses import dataclass
from random import randint
from collections import namedtuple

@dataclass
class Point:
    x: int = 0
    y: int = 0


class Map:
    def __init__(self, px_loc: Point, width, height, px_boxwidth):
        self.px_loc = px_loc
        self.width = width
        self.height = heigth
        self.px_boxwidth = px_boxwidth

    def dynamic_resize():
        width, height = pygame.display.get_window_size()


class Player:
    def __init__(self): #TODO: generate 3 points
        pass

Map = namedtuple('Map', ['width', 'height', 'px_loc', 'px_boxwidth']) #TODO: may be immutable


def make_map() -> Map:
    px_width, px_height = pg.display.get_window_size()
    proportion_factor


if __name__ == "__main__":
    global food_loc
    pg.init()
    pg.display.set_caption("Snake game")
    screen = pg.display.set_mode((800, 600))

    for event in pygame.event.wait():
        if event.type == pg.QUIT:
            exit()

        screen.fill("black")

        #TODO: render
        
        pg.display.flip()
        time.sleep(0.5)
