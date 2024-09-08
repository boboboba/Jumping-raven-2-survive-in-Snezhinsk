from objects.entities.buff import Buff
from objects.entities.entity import Entity
import pygame as pg
from objects.hook import Hook
from physics.vec2 import Vec2
from other.constants import WIDTH, HEIGHT
from objects.entities.weapons import Gun, ShotGun, Rocket, Egg
from objects.entities.bullets import Grenade
from os.path import join
from other.constants import ROOT


class Player(Entity):
    def __init__(self, x, y, width, height, sprite_path=None):
        super().__init__(x, y, width, height, sprite_path)
        self.die_count = 0
        self.max_jumps = 2
        self.hp = 100 + 100
        self.player_image = None
        self.jumped_this_frame = False
        self.weapons = [
            Gun(0, 0, 50, join(ROOT, "assets", "weapons", "pistol.png")),
            ShotGun(0, 0, 50, join(ROOT, "assets", "weapons", "shotgun.png")),
            Rocket(0, 0, 75, join(ROOT, "assets", "weapons", "rpg.png")),
            Egg(0, 0, 50, ""),
        ]
        self.current_weapon = 0
        self.coldown = 30
        self.jump_count = 0
        self.state = "stand"
        self.right = True
        self.frames = 0
        if sprite_path is not None:
            self.load_images()
            self.load_animations()
            self.player_image = self.animations[self.state][0]

        self.buffs = []
        self.invisible = False
        self.hook = None
        self.speed = 300 / 30
        self.jump_force = (-Entity.GRAVITY * 20).y

    def update(self):
        super().update()
        self.coldown -= 1
        if self.hook:
            self.hook.update()
        if not self.is_landed:
            self.state = "jump"
        if self.is_landed:
            self.jump_count = 0
        if self.hp < -1:
            self.die_count += 1
            if self.die_count > 10:
                self.pashalka()
            self.alive = False
            self.hp = 100 + 100
        if self.hp < 200:
            self.hp += 8 / 60
        self.weapons[self.current_weapon].position = self.position + self.direction * 60
        self.weapons[self.current_weapon].direction = self.direction
        if self.position.length() > 10000:
            self.hp -= 1000

        for buff in self.buffs:
            if buff.ended:
                buff.delete()
                self.buffs.remove(buff)
            else:
                buff.update()

    def jump(self):
        if self.jump_count < self.max_jumps:
            self.velocity.y = self.jump_force
            self.jump_count += 1
            self.is_landed = False
        self.jumped_this_frame = True

    def go_right(self):
        self.velocity.x = max(self.speed, self.velocity.x)

    def go_left(self):
        self.velocity.x = -max(self.speed, self.velocity.x)

    def shoot(self):

        if self.coldown < 0:
            self.coldown = 30
            bullets = self.weapons[self.current_weapon].get_bullet()
            for bullet in bullets:
                bullet.team = self.team
            self.velocity += (
                -self.direction * self.weapons[self.current_weapon].kickback
            )
            return bullets
        return []

    def add_buff(self, buff):
        buff.alive = False

        self.buffs.append(buff)
        buff.apply(self)

    def act(self, other):
        from objects.entities.bullets import Bullet, BlowingBullet

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
            if other.team == self.team and self.team != -1:
                return
            if isinstance(other, BlowingBullet):
                if intersecting:
                    other.blowing = True
                    other.alive = False
                    self.hp -= other.damage
                if (
                    other.blowing
                    and (self.position - other.position).length() < other.radius
                ):
                    self.hp -= other.damage
            if isinstance(other, Grenade):
                if (
                    other.blowing
                    and (self.position - other.position).length() < other.radius
                ):
                    self.hp -= other.damage
            elif intersecting:
                other.alive = False
                self.hp -= other.damage

        elif isinstance(other, Buff):
            if intersecting:
                self.add_buff(other)

    def set_direction(self):
        self.direction = (
            Vec2(*pg.mouse.get_pos()) - Vec2(WIDTH, HEIGHT) / 2
        ).normalize()

    def load_images(self):
        pass
        # if self.assets_directory is not None:
        #     self.player_image = pg.image.load(self.assets_directory + r'/ворона.png')
        #     self.player_image = pg.transform.scale(self.player_image, (self.width, self.height))

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
                self.state = "run"
            if abs(self.velocity.x) < 1:
                self.state = "stand"
        else:
            self.state = "jump"

        if self.state in self.animations.keys():
            animation = self.animations[self.state]
        else:
            animation = self.animations["run"]
        self.frames += len(animation) / 10
        if self.frames >= len(animation):
            self.frames = 0
        if self.right:
            self.player_image = animation[int(self.frames)]
        else:
            self.player_image = pg.transform.flip(
                animation[int(self.frames)], True, False
            )

    def draw(self, screen, center):
        position, top_left, _ = self.convert_coordinates(center)
        if not self.invisible:
            hp_bar = (top_left - Vec2(0, 12)).tuple + (self.width * self.hp / 200, 12)
            color = (0, 255, 0) if self.team == 0 else (255, 0, 0)
            pg.draw.rect(screen, color, hp_bar)
            self.weapons[self.current_weapon].draw(screen, center)
            if self.sprite_path is not None:
                screen.blit(
                    self.player_image, (top_left.x, top_left.y, self.width, self.height)
                )

        if self.hook:
            self.hook.draw(screen, center)

    def update_from_wrap(self, wrap):
        super().update_from_wrap(wrap)
        self.state = wrap.state
        self.current_weapon = wrap.current_weapon
        self.invisible = wrap.invisible
        if not wrap.hook_end:
            self.hook = None
        elif not self.hook:
            self.hook = Hook(self, wrap.hook_end)

    def pashalka(self):
        коля = pg.image.load(join(ROOT, "assets", "player", "коля.jpg"))
        коля = pg.transform.scale(коля, (self.width, self.height))
        for key in self.animations.keys():
            self.animations[key] = [коля]
