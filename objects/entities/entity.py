import pygame as pg
from physics.vec2 import Vec2
from objects.game_object import GameObject
from os import listdir
from os.path import isfile, join


class Entity(GameObject):
    GRAVITY = Vec2(0, 0.6)

    def __init__(self, x, y, width, height, sprite_path=None):
        super().__init__(x, y, width, height)
        self.velocity = Vec2(0, 0)
        self.is_landed = False
        self.sprite_path = sprite_path
        self.direction = Vec2(1, 0)
        self.is_dead = False
        self.alive = True
        self.animations = dict()
        self.frames = 0
        self.team = 0
        self.sprite_path = sprite_path
        self.image = None
        self.load_images()

    def apply_forces(self):
        if not self.is_landed:
            self.velocity = self.velocity + Entity.GRAVITY

    def update(self):
        if self.velocity.length() > 25:
            self.velocity = self.velocity.normalize() * 25
        self.position += self.velocity
        self.apply_forces()
        self.animate()

    def move(self, dx, dy):
        self.position += Vec2(dx, dy)

    def load_images(self):
        if self.sprite_path is not None:
            self.image = pg.image.load(self.sprite_path)
            self.image = pg.transform.scale(self.image, (self.width, self.height))

    def delete_images(self):
        pass

    def load_animations(self):
        path = self.sprite_path + "/animations"
        images = [f for f in listdir(path) if isfile(join(path, f))]
        for image in images:
            sprite_sheet = pg.image.load(join(path, image)).convert_alpha()

            sprites = []
            for i in range(sprite_sheet.get_width() // 32):
                surface = pg.Surface((32, 32), pg.SRCALPHA, 32)
                rect = pg.Rect(i * 32, 0, 32, 32)
                surface.blit(sprite_sheet, (0, 0), rect)
                surface = pg.transform.scale(surface, (self.width, self.height))
                sprites.append(surface)
                # print(surface.get_width(), surface.get_height())

                self.animations[image.replace(".png", "")] = sprites

    def act(self, other):
        pass

    def collide(self, map):
        self.move(self.velocity.x, 0)
        for corner in self.corners:
            key = (
                corner // map.tile_size * map.tile_size
                + Vec2(map.tile_size / 2, map.tile_size / 2)
            ).tuple
            block = map.blocks.get(key)
            if block is not None:
                self.move(-self.velocity.x, 0)
                if self.velocity.x > 0:
                    self.position.x = block.top_left.x - self.width / 2 - 1
                else:
                    self.position.x = block.bottom_right.x + self.width / 2 + 1
                self.velocity.x = 0
                break
        else:
            self.move(-self.velocity.x, 0)

        self.move(0, self.velocity.y)
        for corner in self.corners:
            key = (
                corner // map.tile_size * map.tile_size
                + Vec2(map.tile_size / 2, map.tile_size / 2)
            ).tuple
            block = map.blocks.get(key)
            if block is not None:
                self.move(0, -self.velocity.y)
                if self.velocity.y > 0:
                    self.position.y = block.top_left.y - self.height / 2 - 1
                else:
                    self.position.y = block.bottom_right.y + self.height / 2 + 1
                self.velocity.y = 0
                break
        else:
            self.move(0, -self.velocity.y)

        self.move(0, 2)
        for corner in self.corners:
            key = (
                corner // map.tile_size * map.tile_size
                + Vec2(map.tile_size / 2, map.tile_size / 2)
            ).tuple
            block = map.blocks.get(key)
            if block is not None:
                self.is_landed = True
                break
        else:
            self.is_landed = False

        self.move(0, -2)

    def animate(self):
        self.frames += 1

    def draw(self, screen, center):
        if self.image is None:
            super().draw(screen, center)
            return
        pos, top_left, _ = self.convert_coordinates(center)
        rect = top_left.tuple + self.size.tuple
        if self.sprite_path is not None:
            screen.blit(self.image, rect)

    def update_from_wrap(self, wrap):
        self.position = wrap.position
        self.velocity = wrap.velocity
        self.direction = wrap.direction
        self.width = wrap.width
        self.height = wrap.height
        self.sprite_path = wrap.sprite_path
