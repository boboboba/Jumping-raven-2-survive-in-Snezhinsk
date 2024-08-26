import math
from abc import ABC

import game_object
from bullets import *


class Weapon(game_object.GameObject):
    def __init__(self, x, y, width, sprite_path):
        super().__init__(x, y, width=width)
        self.sprite = None
        if sprite_path != '':
            sprite = pg.image.load(sprite_path)
            h = width * sprite.get_height() / sprite.get_width()
            self.sprite = pg.transform.scale(pg.image.load(sprite_path), (width, h))
        self.kickback = 0
        self.direction = Vec2(0, 0)
        self.dist = 30
        pass

    def get_bullet(self):
        pass

    def draw(self, screen, center):
        if not self.sprite:
            return
        angle = -math.atan2(self.direction.y, self.direction.x) / math.pi * 180
        pos, _,_ = self.convert_coordinates(center)
        rect = self.sprite.get_rect(center=pos.tuple)
        image = self.sprite
        if angle > 90 or angle < -90:
            image = pg.transform.flip(image, False, True)
            # angle =  -angle
        image = pg.transform.rotate(image, angle)


        screen.blit(image, rect)


class Gun(Weapon):
    def get_bullet(self):
        bullet_pos = self.position + self.direction * self.dist / 2
        bullet = Bullet(bullet_pos.x, bullet_pos.y, 30, 30, 100, sprite_path='assets/bullets/bullet.png')
        bullet.velocity = self.direction * 30
        return [bullet]

class ShotGun(Weapon):
    def get_bullet(self):
        bullets = []
        bullet_pos = self.position + self.direction * self.dist / 2
        bullet = Bullet(bullet_pos.x, bullet_pos.y, 10, 10, 30, sprite_path='assets/bullets/bullet.png')
        bullet.velocity = self.direction.rotate(-math.pi / 9) * 30
        bullets.append(bullet)

        bullet = Bullet(bullet_pos.x, bullet_pos.y, 10, 10, 30, sprite_path='assets/bullets/bullet.png')
        bullet.velocity = self.direction * 30
        bullets.append(bullet)

        bullet = Bullet(bullet_pos.x, bullet_pos.y, 10, 10, 30, sprite_path='assets/bullets/bullet.png')
        bullet.velocity = self.direction.rotate(math.pi / 9) * 30
        bullets.append(bullet)
        return bullets

class Rocket(Weapon):
    def __init__(self,x, y, width, sprite_path):
        super().__init__(x, y, width, sprite_path)
        self.kickback = 20
    def get_bullet(self):
        bullets = []
        bullet_pos = self.position + self.direction * self.dist / 2
        bullet = BlowingBullet(bullet_pos.x, bullet_pos.y, 50, 25, 150, sprite_path='assets/bullets/rocket.png')
        bullet.velocity = self.direction * 15
        bullets.append(bullet)

        return bullets

class Egg(Weapon):
    def get_bullet(self):
        bullets = []
        bullet_pos = self.position - self.direction * 60 + Vec2(0, 60)
        bullet = Grenade(bullet_pos.x, bullet_pos.y, 50, 50, 300, sprite_path='assets/bullets/egg.png')
        bullet.velocity = Vec2(3 * (random.randint(0,1)-.5) * 2, 0)
        bullets.append(bullet)
        return bullets

    def draw(self, screen, center):
        pass

class HealingWard:
    pass

class RequiemOfSouls:
    def pause(self):
        print('1000-6.999999994 ???????')
