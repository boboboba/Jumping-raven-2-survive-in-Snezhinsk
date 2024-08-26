import math
import random

from pygame import Vector2

import entity
from entity import Entity
import pygame as pg
from physics.vec2 import Vec2
from effect import *
from os import listdir
from os.path import isfile, join


class Bullet(Entity):
    def __init__(self, x, y, width, height, damage, sprite_path=None):
        super().__init__(x, y, width, height)
        self.sprite_path = sprite_path
        self.damage = damage
        self.lifetime = 0
        self.image = None
        self.load_images()
        self.alive = True
        if self.sprite_path is not None:
            self.image = pg.image.load(self.sprite_path)
            self.image = pg.transform.scale(self.image, (self.hitbox.width, self.hitbox.height))
        # self.velocity = Vector2(100, 0) / 60

    def update(self):
        super().update()
        # print('x:', self.position.x,'y:',self.position.y)
        self.direction = self.velocity.normalize().normalize()
        self.lifetime += 1
        if self.lifetime > 300:
            self.alive = False

    def act(self, other):
        from player import Player
        if isinstance(other, Player) and self.intersects(other):
            self.alive = False

    def load_images(self):
        if self.sprite_path is not None:
            self.image = pg.image.load(self.sprite_path)
            self.image = pg.transform.scale(self.image, (self.hitbox.width, self.hitbox.height))

    def delete_images(self):
        self.image = None

    def draw(self, screen, center):
        if self.image is None:
            super().draw(screen, center)
            return
        angle = -math.atan2(self.direction.y, self.direction.x) / math.pi * 180
        rotated_image = pg.transform.rotate(self.image, angle)
        pos, top_left, _ = self.convert_coordinates(center)
        rect = rotated_image.get_rect(center=pos.tuple)
        if self.sprite_path is not None:
            screen.blit(rotated_image,
                        rect)

class BlowingBullet(Bullet):
    def __init__(self, x, y, width, height, damage, sprite_path=None):
        super().__init__(x, y, width, height, damage, sprite_path=sprite_path)
        self.radius = 400
        self.blowing = False

    def update(self):
        super().update()
        self.velocity -= Entity.GRAVITY / 4*3
        self.direction = self.velocity.normalize()
        self.frames += 1

    def collide(self, map):
        for corner in self.corners:
            if (corner // map.tile_size * map.tile_size + Vec2(map.tile_size / 2, map.tile_size / 2)).tuple in map.blocks.keys():
                self.blowing = True

    def act(self, other):
        self.alive = not self.blowing

    def get_particle(self):
        if self.blowing:
            return Effect(self.position.x, self.position.y, 400, 400, animation_path=join('assets', 'particles', 'explosion-1.png'))
        if self.frames % 1 == 0:
            surf = pg.Surface((9,9))
            surf.fill((255,255,255))
            pos = self.position - self.direction * self.width / 2 + Vec2(1,0).rotate(random.random() * 5) * 5
            effect = Particle(pos.x, pos.y, 9,9, lifetime=60)
            effect.velocity = Vec2(self.direction.x, self.direction.y).rotate((random.random() - .5) * math.pi)
            effect.image = surf
            return effect

class Grenade(Bullet):
    def __init__(self, x, y, width, height, damage, sprite_path=None):
        super().__init__(x, y, width, height, damage, sprite_path=sprite_path)
        self.radius = 400
        self.blowing = False

    def update(self):
        super().update()
        self.velocity -= Entity.GRAVITY / 4 * 3
        self.direction = self.velocity.normalize()
        self.frames += 1
        if self.lifetime > 299:
            self.blowing = True

    def act(self, other):
        pass
    def collide(self, map):
        for corner in self.corners:
            if (corner // map.tile_size * map.tile_size + Vec2(map.tile_size / 2, map.tile_size / 2)).tuple in map.blocks.keys():
                self.alive = False
        self.move(self.velocity.x, 0)
        for corner in self.corners:
            key = (corner // map.tile_size * map.tile_size + Vec2(map.tile_size / 2, map.tile_size / 2)).tuple
            block = map.blocks.get(key)
            if block is not None:
                self.move(-self.velocity.x, 0)
                if self.velocity.x < 0:
                    sign = -1
                elif self.velocity.x > 0:
                    sign = 1
                else:
                    sign = 0
                self.velocity.x *= -1 * .8
                self.velocity.y *= .7
                break
        else:
            self.move(-self.velocity.x, 0)

        self.move(0, self.velocity.y)
        for corner in self.corners:
            key = (corner // map.tile_size * map.tile_size + Vec2(map.tile_size / 2, map.tile_size / 2)).tuple
            block = map.blocks.get(key)
            if block is not None:
                self.move(0, -self.velocity.y)
                if self.velocity.y < 0:
                    sign = -1
                elif self.velocity.y > 0:
                    sign = 1
                else:
                    sign = 0
                self.velocity.y = min(-sign * 3, self.velocity.y * .5)
                self.velocity.x *= .7

                break
        else:
            self.move(0, -self.velocity.y)

    def get_particle(self):
        if self.blowing:
            return Effect(self.position.x, self.position.y, 400, 400, animation_path=join('assets', 'particles', 'explosion-1.png'))

    def draw(self, screen, center):
        if self.image is None:
            super().draw(screen, center)
            return
        pos, top_left, _ = self.convert_coordinates(center)
        rect = self.image.get_rect(center=pos.tuple)
        if self.sprite_path is not None:
            screen.blit(self.image,
                        rect)
