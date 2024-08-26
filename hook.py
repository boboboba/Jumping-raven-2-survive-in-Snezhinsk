import math

from game_object import GameObject
import pygame as pg

from physics.vec2 import Vec2


class Hook(GameObject):
    def __init__(self, player, point):
        super().__init__(point.x, point.y, 0, 0)
        self.player = player
        self.point = point
        self.is_bebra = False

    def update(self):
        vec = (self.point - self.player.position)
        length = vec.length()
        # if self.is_bebra:
        self.player.velocity += vec.normalize() * 2
        if length > 300:
            self.player.move(vec.normalize().x * 10, vec.normalize().y * 10)

    def draw(self, screen, center):
        # player_pos = self.player.position - center + Vec2(800, 600) / 2
        player_pos, _, _ = self.player.convert_coordinates(center)
        point, _, _ = self.convert_coordinates(center)

        pg.draw.line(screen, (255, 255, 255), (player_pos.x, player_pos.y), (point.x, point.y), 10)