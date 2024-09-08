from objects.map.block import Block
import pygame as pg
from physics.vec2 import Vec2
from other.constants import ROOT
from os.path import join


class Map:
    def __init__(self):
        self.blocks = dict()
        self.tile_size = 50
        self.spawn_position = Vec2(0, 0)
        self.image = pg.image.load(join(ROOT, "assets", "textures", "sky.png"))
        self.image.set_alpha(128)
        self.image = pg.transform.scale(self.image, (800, 600))

    def load_from_file(self, file):
        with open(file, "r") as f:
            lines = f.readlines()
        self.load_from_list(lines)

    def load_from_list(self, lines, w_sprites=True):
        lines = lines.copy()
        spawn = [float(x) for x in lines.pop(0).split(";")]
        self.spawn_position = Vec2(spawn[0], spawn[1])
        for line in lines:
            rect = line.split(";")
            rect = [float(x) for x in rect[:4]] + [rect[4][:-1]]
            if not w_sprites:
                rect[4] = None
            self.blocks[(rect[0], rect[1])] = Block(
                rect[0], rect[1], rect[2], rect[3], sprite_path=rect[4]
            )

    def draw(self, screen, center: Vec2):
        x = (-(center // 2) % (self.image.get_width())).x
        y = (-(center // 2) % (self.image.get_height())).y
        top_left = Vec2(x, y)

        screen.blit(self.image, (top_left.x, top_left.y))
        screen.blit(self.image, (top_left.x - self.image.get_width(), top_left.y))
        screen.blit(self.image, (top_left.x, top_left.y - self.image.get_height()))
        screen.blit(
            self.image,
            (top_left.x - self.image.get_width(), top_left.y - self.image.get_height()),
        )
        for block in self.blocks.values():
            block.draw(screen, center)
