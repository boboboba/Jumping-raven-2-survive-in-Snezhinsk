from block import Block
import pygame as pg

from physics.vec2 import Vec2


class Map:
    def __init__(self):
        self.blocks = dict()
        self.tile_size = 50

    def parse_from_text(self, text):
        x = 0
        y = 0
        size = 100
        for char in text:
            if char == '\n' or char == '\t' or char == '\r':
                x = 0
                y += 1
            elif char == '1':
                self.blocks.append(Block(x * size, y * size, size, size, sprite_path="floor.png"))
            x += 1

    def load_from_file(self, file):
        with open(file, 'r') as f:
            for line in f.readlines():
                rect = line.split(';')
                rect = [float(x) for x in rect[:4]] + [rect[4][:-1]]
                self.blocks[(rect[0], rect[1])] = Block(rect[0], rect[1], rect[2], rect[3], sprite_path=rect[4])

    def load_from_list(self, lines):
        for line in lines:
            rect = line.split(';')
            rect = [float(x) for x in rect[:4]] + [rect[4][:-1]]
            self.blocks[(rect[0], rect[1])] = Block(rect[0], rect[1], rect[2], rect[3], sprite_path=rect[4])

    def draw(self, screen, center):
        top_left = Vec2(0, 0) - center / 3

        image = pg.image.load('assets/textures/bg.png')
        image.set_alpha(128)
        image = pg.transform.scale(image, (1600, 1200))
        screen.blit(image, (top_left.x, top_left.y))
        for block in self.blocks.values() :
            block.draw(screen, center)

