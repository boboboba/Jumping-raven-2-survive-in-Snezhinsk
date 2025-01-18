from os.path import join
from traceback import print_tb

from objects.game_object import GameObject
import pygame as pg

from other.constants import ROOT


class Block(GameObject):
    TEXTURE_PATH = join(ROOT, "assets", "textures")

    def __init__(self, x, y, width, height, sprite_path=""):
        super().__init__(x, y, width, height)
        self.local_path = sprite_path
        self.sprite = None
        if sprite_path != "":
            self.sprite = pg.image.load(self.sprite_path)
            self.sprite = pg.transform.scale(self.sprite, (width, height))

    @property
    def sprite_path(self):
        return join(ROOT, self.local_path)
    def draw(self, screen, center):
        if self.sprite is None:
            super().draw(screen, center)
            return
        _, top_left, _ = self.convert_coordinates(center)
        screen.blit(self.sprite, (top_left.x, top_left.y, self.width, self.height))
