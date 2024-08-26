import math
import sys

from entity import Entity
# from bullet import Bullet
import pygame as pg

from hook import Hook
from physics.vec2 import Vec2
from constants import WIDTH, HEIGHT
from weapons import *


class Player(Entity):
    def __init__(self, x, y, width, height, assets_directory=None):
        super().__init__(x, y, width, height, assets_directory)
        self.hp = 100 + 100
        self.player_image = None
        self.jumped_this_frame = False
        self.weapons = [ShotGun(0, 0, 50, 'assets/player/gun2.png'),
                        Gun(0, 0, 50, ''),
                        Rocket(0, 0, 75, 'assets/player/gun3.png'),
                        Egg(0, 0, 50, '')]
        self.current_weapon = 0
        self.coldown = 30
        self.jump_count = 0
        self.state = 'stand'
        self.right = True
        self.frames = 0
        if assets_directory is not None:
            self.load_images()
            self.load_animations()

        self.hook = None

    def update(self):
        super().update()
        self.coldown -= 1
        if self.hook:
            self.hook.update()
        if not self.is_landed:
            self.state = 'jump'
        if self.is_landed:
            self.jump_count = 0
        if self.hp < 0:
            self.position = Vec2(250, 100)
            self.hp = 100 + 100
        self.weapons[self.current_weapon].position = self.position + self.direction * 60
        self.weapons[self.current_weapon].direction = self.direction
        if self.position.length() > 10000:
            self.hp = -1

    def jump(self):
        if self.jump_count < 2:
            self.velocity = -Entity.GRAVITY * 20
            self.jump_count += 1
            self.is_landed = False
        self.jumped_this_frame = True

    def shoot(self):
        from bullets import Bullet
        if self.coldown <0:
            self.coldown = 30
            bullets = self.weapons[self.current_weapon].get_bullet()
            self.velocity += -self.direction * self.weapons[self.current_weapon].kickback
            return bullets
        return []

    def act(self, other):
        from bullets import Bullet, BlowingBullet
        if self is other:
            return
        intersecting = self.intersects(other)
        if isinstance(other, Player):
            if intersecting:
                vec = (self.position - other.position).normalize() * 5
                if vec.length() == 0:
                    vec = Vec2(1, 0)
                self.velocity = vec
        elif isinstance(other, Bullet):
            if isinstance(other, BlowingBullet):
                if intersecting:
                    other.blowing = True
                    self.hp -= other.damage
                if other.blowing and (self.position - other.position).length() < other.radius:
                    self.hp -= other.damage
            if isinstance(other, Grenade):
                if other.blowing and (self.position - other.position).length() < other.radius:
                    self.hp -= other.damage
            elif intersecting:
                self.hp -= other.damage


    def set_direction(self):
        self.direction = (Vec2(*pg.mouse.get_pos()) - Vec2(WIDTH, HEIGHT) / 2).normalize()

    def load_images(self):
        if self.assets_directory is not None:
            self.player_image = pg.image.load(self.assets_directory + r'/ворона.png')
            self.player_image = pg.transform.scale(self.player_image, (self.width, self.height))

            # self.gun_image = pg.image.load(self.assets_directory + r'/ган.png')
            # self.gun_image = pg.transform.scale(self.gun_image, (self.width, self.height))

    def delete_images(self):
        self.player_image = None
        self.gun_image = None

    def animate(self):
        if self.velocity.x > 0:
            self.right = True
        elif self.velocity.x < 0:
            self.right = False

        if self.is_landed:
            if self.velocity.x != 0:
                self.state = 'run'
            if abs(self.velocity.x) < 1:
                self.state = 'stand'
        else:
            self.state = 'jump'

        if self.state in self.animations.keys():
            animation = self.animations[self.state]
        else:
            animation = self.animations['run']
        self.frames += len(animation) / 10
        if self.frames >= len(animation):
            self.frames = 0
        if self.right:
            self.player_image = animation[int(self.frames)]
        else:
            self.player_image = pg.transform.flip(animation[int(self.frames)], True, False)

    def draw(self, screen, center):
        position, top_left, _ = self.convert_coordinates(center)
        hp_bar = (top_left - Vec2(0,12)).tuple + (self.width * self.hp/200, 12)
        pg.draw.rect(screen, (0, 255, 0), hp_bar)
        self.weapons[self.current_weapon].draw(screen,center)
        if self.assets_directory is not None:
            screen.blit(self.player_image, (top_left.x, top_left.y, self.width, self.height))

        if self.hook:
            self.hook.draw(screen, center)

    def update_from_wrap(self, wrap):
        super().update_from_wrap(wrap)
        self.state = wrap.state
        self.current_weapon = wrap.current_weapon
        if not wrap.hook_end:
            self.hook = None
        elif not self.hook:
            self.hook = Hook(self, wrap.hook_end)
