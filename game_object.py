from physics.hitbox import Hitbox
from physics.vec2 import Vec2
import pygame as pg
from constants import WIDTH, HEIGHT


class GameObject:
    def __init__(self, x, y, width=0, height=0):
        self.position = Vec2(x, y)
        self.hitbox = Hitbox(x, y, width, height)
        self.size = Vec2(width, height)
        self.width = width
        self.height = height

    @property
    def top_left(self):
        return self.position - Vec2(self.hitbox.width, self.height) / 2

    @property
    def bottom_right(self):
        return self.position + Vec2(self.hitbox.width, self.height) / 2

    @property
    def corners(self):
        return [Vec2(self.top_left.x, self.top_left.y),
                Vec2(self.top_left.x, self.bottom_right.y),
                Vec2(self.bottom_right.x, self.bottom_right.y),
                Vec2(self.bottom_right.x, self.top_left.y)]

    def intersects(self, other) -> bool:
        return (max(self.top_left.x, other.top_left.x) <= min(self.bottom_right.x, other.bottom_right.x) and
                max(self.top_left.y, other.top_left.y) <= min(self.bottom_right.y, other.bottom_right.y))

    def collide_point(self, x, y):
        return self.top_left.x <= x <= self.bottom_right.x and self.top_left.y <= y <= self.bottom_right.y

    def draw(self, screen, center):
        position, top_left, bottom_right = self.convert_coordinates(center)
        pg.draw.rect(screen, (255, 255, 0), (top_left.x, top_left.y,
                                             self.width, self.height))

    def convert_coordinates(self, center):
        position = self.position - center + Vec2(WIDTH, HEIGHT) / 2
        top_left = position - self.size / 2
        bottom_right = position + self.size / 2

        return position, top_left, bottom_right

    def get_particle(self):
        return None
