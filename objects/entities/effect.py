from physics.vec2 import Vec2
import pygame as pg

from objects.game_object import GameObject
from other.functions import load_animation


class Effect(GameObject):
    def __init__(self, x, y, width, height, animation_path="", lifetime=120):
        super().__init__(x, y, width, height)
        self.velocity = Vec2(0, 0)
        self.image = pg.Surface((width, height))
        if animation_path != "":
            self.animation = [
                pg.transform.scale(animation, (self.width, self.height))
                for animation in load_animation(animation_path)
            ]
        else:
            self.animation = []
        self.frames = 0
        self.lifetime = lifetime
        self.alive = True

    def update(self):
        self.position += self.velocity
        self.animate()
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.alive = False

    def animate(self):
        if not self.animation:
            return
        self.frames += 0.2
        if self.frames >= len(self.animation):
            self.alive = False
            self.frames = 0
        self.image = self.animation[int(self.frames)]

    def draw(self, screen, center):
        position, _, _ = self.convert_coordinates(center)
        rect = self.image.get_rect(center=position.tuple)
        screen.blit(self.image, rect)


class Particle(Effect):
    def __init__(self, x, y, width, height, lifetime=60):
        super().__init__(x, y, width, height, lifetime=lifetime)

    def update(self):
        self.position += self.velocity
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.alive = False
        self.width *= 0.9
        self.height *= 0.9
        if self.width < 1 or self.height < 1:
            self.alive = False
        self.image = pg.transform.scale(self.image, (self.width, self.height))
