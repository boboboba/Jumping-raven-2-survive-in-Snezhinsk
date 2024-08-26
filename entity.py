import pygame as pg
from physics.vec2 import Vec2
from physics.hitbox import Hitbox
from game_object import GameObject
from os import listdir
from os.path import isfile, join


class Entity(GameObject):
    GRAVITY = Vec2(0, .6)

    def __init__(self, x, y, width, height, assets_directory=None):
        super().__init__(x, y, width, height)
        self.velocity = Vec2(0, 0)
        self.is_landed = False
        self.assets_directory = assets_directory
        self.direction = Vec2(1, 0)
        self.is_dead = False
        self.animations = dict()
        self.frames = 0

    def apply_forces(self):
        if not self.is_landed:
            self.velocity = self.velocity + Entity.GRAVITY

    def update(self):
        self.position += self.velocity
        self.apply_forces()
        if self.velocity.length() > 25:
            self.velocity = self.velocity.normalize() * 25
        self.animate()

    def move(self, dx, dy):
        self.position += Vec2(dx, dy)

    def load_images(self):
        pass

    def delete_images(self):
        pass

    def load_animations(self):
        path = self.assets_directory + '/animations'
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
            key = (corner // map.tile_size * map.tile_size + Vec2(map.tile_size / 2, map.tile_size / 2)).tuple
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
            key = (corner // map.tile_size * map.tile_size + Vec2(map.tile_size / 2, map.tile_size / 2)).tuple
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
            key = (corner // map.tile_size * map.tile_size + Vec2(map.tile_size / 2, map.tile_size / 2)).tuple
            block = map.blocks.get(key)
            if block is not None:
                self.is_landed = True
                break
        else:
            self.is_landed = False

        self.move(0, -2)

        # for corner in self.corners:
        #     if corner in map.keys():

        # for block in map.blocks.values():
        #     if not self.intersects(block):
        #         dx = self.velocity.x
        #         self.move(dx, 0)
        #         if self.intersects(block) and self.bottom_right.y != block.top_left.y:
        #             self.move(-dx, 0)
        #             if dx > 0:
        #                 self.position.x = block.top_left.x - self.width / 2 - 1
        #             else:
        #                 self.position.x = block.bottom_right.x + self.width / 2 + 1
        #             self.velocity.x = 0
        #         else:
        #             self.move(-dx, 0)
        #
        #     elif self.intersects(block):
        #         dot = self.velocity.y
        #         self.is_landed = True
        #         if dot > 0:
        #             self.position.y = block.top_left.y - self.height / 2
        #             self.velocity.y = 0
        #
        #         elif dot < 0 and self.position.y > block.position.y:
        #             if not self.bottom_right.y == block.top_left.y:
        #                 self.position.y = block.bottom_right.y + self.height / 2 + 1
        #                 self.velocity.y = 0

    def animate(self):
        self.frames += 1

    # def draw(self, screen, center):
    #     screen_position = self.position - center + Vec2(800, 600) / 2
    #
    #     print(screen_position.x, screen_position.y)
    #     # print(self.position.x, self.position.y)
    #     # pg.quit()
    #     pg.draw.rect(screen, (0, 255, 0), (screen_position.x, screen_position.y, self.hitbox.width, self.hitbox.height))

    def update_from_string(self, string):
        # id;type;x;y;velx;vely;dirx;diry;sprite
        data = string.split(';')
        self.position = Vec2(float(data[2]), float(data[3]))
        self.velocity = Vec2(float(data[4]), float(data[5]))

    def convert_to_string(self, id):
        return ''

    def update_from_wrap(self, wrap):
        # from wrapper import Wrap
        self.position = wrap.position
        self.velocity = wrap.velocity
        self.direction = wrap.direction
        self.width = wrap.width
        self.height = wrap.height
        self.assets_directory = wrap.assets_directory
