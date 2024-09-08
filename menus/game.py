import sys
import time
from os.path import join

import pygame as pg

from objects.entities.buff import Buff
from objects.entities.bullets import Bullet
from objects.map.map import Map
from objects.entities.player import Player
from physics.vec2 import Vec2
from web_code.network import Network
from objects.hook import Hook
from objects.game_object import GameObject
import threading
from other.constants import ROOT

from other.wrapper import Wrap

MULTIPLAYER = True


class Game:
    def __init__(self, screen):
        with open(join(ROOT, "config.txt")) as f:
            ip = f.readline()[:-1].split(":")[1]
            map = f.readline().split(":")[1]
        self.team = -1
        if MULTIPLAYER:
            self.network = Network(ip)
            try:
                id, lines, team = self.network.connect()
            except TypeError:
                print("Server not found")
                sys.exit()
            self.id = id
            self.team = team
        self.map = Map()
        if MULTIPLAYER:
            self.map.load_from_list(lines)
        else:
            self.map.load_from_file(map)
        self.pressed_keys = []
        self.running = True
        self.screen = screen
        print(self.map.spawn_position)
        self.player = Player(
            self.map.spawn_position.x,
            self.map.spawn_position.y,
            48,
            48,
            sprite_path=join(ROOT, "assets", "player"),
        )
        self.player.team = self.team

        self.player.load_images()
        self.player.load_animations()
        self.players = dict()
        # self.players[self.id] = self.player
        self.bullets = []
        self.buffs = []
        self.particles = []
        self.frames = 0

        self.thread = threading.Thread(target=self.receive)
        self.dead = False
        self.hook = None

    def run(self):
        clock = pg.time.Clock()
        # self.team =
        if MULTIPLAYER:
            self.thread.start()
        while self.running:
            if self.dead:
                return
            self.act_entities(
                self.player, *self.players.values(), *self.bullets, *self.buffs
            )
            self.get_particles()
            self.check_collisions([self.player])

            self.check_collisions(self.bullets)
            self.check_collisions(self.players.values())
            self.update_entities()
            self.controls(pg.event.get())

            self.frames = (self.frames + 1) % 60
            if self.frames == 0:
                print(self.player.position)
            self.draw()
            pg.display.flip()
            clock.tick(60)

            self.easter_egg()

    def controls(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.dead = True
                # self.thread.is_alive = False
                quit()
            if event.type == pg.KEYDOWN:
                self.pressed_keys.append(event.unicode)
                if event.key == pg.K_SPACE:
                    self.player.jump()
                if event.key == pg.K_q:
                    self.throw_hook(self.player)
                if event.key == pg.K_ESCAPE:
                    self.running = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_q:
                    self.player.hook = None
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    bullets = self.player.shoot()
                    if MULTIPLAYER:
                        for bullet in bullets:
                            # bullet.delete_images()
                            self.network.send(Wrap(bullet))
                    for bullet in bullets:
                        self.bullets.append(bullet)
                        bullet.load_images()

                    # sound = pg.mixer.Sound("../assets/player/shoot.mp3")
                    # sound.play()

                if event.button == 3:
                    self.player.current_weapon = (self.player.current_weapon + 1) % len(
                        self.player.weapons
                    )

        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            self.player.go_right()
        elif keys[pg.K_a]:
            self.player.go_left()
        else:
            self.player.velocity -= Vec2(1, 0) * self.player.velocity.x / 10

    def check_collisions(self, entities):
        for entity in entities:
            entity.collide(self.map)

    def update_entities(self):
        for player in self.players.values():
            player.update()
        self.player.set_direction()
        self.player.update()
        if not self.player.alive:
            self.player.position = self.map.spawn_position
            self.player.alive = True
        for bullet in self.bullets:
            bullet.update()
            if not bullet.alive:
                self.bullets.remove(bullet)
        for buff in self.buffs:
            if not buff.alive:
                self.buffs.remove(buff)
        if self.hook is not None:
            self.hook.update()

        for particle in self.particles:
            particle.update()
            if not particle.alive:
                self.particles.remove(particle)

    def get_particles(self):
        for entity in [*self.players.values(), *self.bullets, self.player]:
            if entity is None:
                continue
            particle = entity.get_particle()
            if particle is not None:
                self.particles.append(particle)

    def receive(self):
        cycle = 0
        while True:
            if self.dead:
                return
            time.sleep(50 / 1000)
            to_send = Wrap(self.player)
            to_send.id = self.id
            try:
                data = self.network.send(to_send)
            except Exception:
                raise
            ids = []
            for wrap in data:
                obj = wrap.get_new()
                if isinstance(obj, Player):
                    ids.append(wrap.id)
                    if wrap.id not in self.players.keys():
                        self.players[wrap.id] = wrap.get_new()
                    else:
                        self.players[wrap.id].update_from_wrap(wrap)
                elif isinstance(obj, Bullet):
                    bullet = wrap.get_new()
                    self.bullets.append(bullet)
                elif isinstance(obj, Buff):
                    buff = wrap.get_new()
                    if len(self.buffs) < 6:
                        self.buffs.append(buff)
                else:
                    raise ValueError
            if cycle % 20 == 0:
                to_pop = []
                for key in self.players.keys():
                    if key not in ids:
                        to_pop.append(key)
                for key in to_pop:
                    self.players.pop(key)
            cycle += 1

    def act_entities(self, *entities):
        for first in entities:
            for second in entities:
                first.act(second)

    def throw_hook(self, player):
        dx, dy = player.direction.x, player.direction.y
        hook_end = GameObject(player.position.x, player.position.y, 0, 0)
        for i in range(0, 300, 20):
            pos = hook_end.position // self.map.tile_size * self.map.tile_size + Vec2(
                self.map.tile_size / 2, self.map.tile_size / 2
            )
            if pos.tuple in self.map.blocks.keys():
                self.player.hook = Hook(
                    player, Vec2(hook_end.position.x, hook_end.position.y)
                )
                return
            hook_end.position.x += dx * 20
            hook_end.position.y += dy * 20

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.map.draw(self.screen, self.player.position)

        all = [*self.players.values(), self.player, *self.bullets, *self.buffs]

        for obj in all:
            if obj is not None:
                obj.draw(self.screen, self.player.position)
        for particle in self.particles:
            particle.draw(self.screen, self.player.position)

        # minimap

    def easter_egg(self):
        anekdot = "aezakmi"
        if len("".join(self.pressed_keys)) > len(anekdot):
            self.pressed_keys = self.pressed_keys[1:]
        if "".join(self.pressed_keys) == anekdot:
            self.player.max_jumps = 999999
