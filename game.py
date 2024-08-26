import time
from html import entities

import pygame as pg

import bullets
from map import Map
from network import Network
from player import Player
from physics.vec2 import Vec2
from physics.hitbox import Hitbox
from network import Network
from bullets import Bullet
import copy
from hook import Hook
from game_object import GameObject
import threading
from os import listdir
from os.path import isfile, join

from wrapper import Wrap

MULTIPLAYER = True


class Game:
    def __init__(self, screen):
        with open('config.txt') as f:
            ip = f.readline()[:-1].split(':')[1]
            map = f.readline()[:-1].split(':')[1]
        if MULTIPLAYER:
            self.network = Network(ip)
            id, lines = self.network.connect()
            self.id = id
        self.map = Map()
        # self.map.parse_from_text(MAP)
        if MULTIPLAYER:
            self.map.load_from_list(lines)
        else:
            self.map.load_from_file(map)
        # self.player_textures = dict()
        # self.weapon_textures = dict()
        # self.block_textures = dict()

        self.running = True
        self.screen = screen
        self.player = Player(500, 0, 48, 48, assets_directory='assets/player')
        self.player.load_images()
        self.player.load_animations()
        self.players = dict()
        # self.players[self.id] = self.player
        self.bullets = []
        self.particles = []
        self.frames = 0

        self.thread = threading.Thread(target=self.receive)
        self.dead = False
        self.hook = None

    def run(self):
        clock = pg.time.Clock()
        if MULTIPLAYER:
            self.thread.start()
        while self.running:
            if len(self.bullets) > 0:
                pass
            self.act_entities(self.player, *self.players.values(), *self.bullets)
            self.get_particles()
            self.check_collisions([self.player])

            self.check_collisions(self.bullets)
            self.check_collisions(self.players.values())
            self.update_entities()
            self.controls(pg.event.get())

            self.frames = (self.frames + 1) % 60
            # if self.frames % 4 == 0 and MULTIPLAYER:
            #     self.receive()
            self.draw()
            pg.display.flip()
            clock.tick(90)

    def controls(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.dead = True
                # self.thread.is_alive = False
                quit()
            if event.type == pg.KEYDOWN:
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

                    sound = pg.mixer.Sound('assets/player/shoot.mp3')
                    # sound.play()

                if event.button == 3:
                    self.player.current_weapon = (self.player.current_weapon + 1) % len(self.player.weapons)

        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            self.player.velocity = Vec2(max(300 / 30, self.player.velocity.x), self.player.velocity.y)
        elif keys[pg.K_a]:
            self.player.velocity = Vec2(min(-300 / 30, self.player.velocity.x), self.player.velocity.y)
        else:
            self.player.velocity -= Vec2(1, 0) * self.player.velocity.dot(Vec2(1, 0)) / 10

    def check_collisions(self, entities):
        for entity in entities:
            entity.collide(self.map)

    def update_entities(self):
        for player in self.players.values():
            player.update()
        self.player.set_direction()
        self.player.update()
        for bullet in self.bullets:
            bullet.update()
            if not bullet.alive:
                self.bullets.remove(bullet)
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
        # print(len(self.players))
        # self.entities = self.network.send(self.player)
        while True:
            if self.dead:
                return
            time.sleep(50/1000)
            to_send = Wrap(self.player)
            to_send.id = self.id
            data = self.network.send(to_send)
            for wrap in data:
                if wrap.type == 'player':
                    if wrap.id not in self.players.keys():
                        self.players[wrap.id] = wrap.get_new()
                    else:
                        self.players[wrap.id].update_from_wrap(wrap)

                elif wrap.type == 'bullet' or wrap.type == 'bbullet':
                    bullet = wrap.get_new()
                    self.bullets.append(bullet)
                else:
                    raise ValueError

    def act_entities(self, *entities):
        for first in entities:
            for second in entities:
                first.act(second)

    def throw_hook(self, player):
        dx, dy = player.direction.x, player.direction.y
        hook_end = GameObject(player.position.x, player.position.y, 0, 0)
        for i in range(0, 300, 20):
            pos = hook_end.position // self.map.tile_size * self.map.tile_size + Vec2(self.map.tile_size / 2, self.map.tile_size / 2)
            if pos.tuple in self.map.blocks.keys():
                self.player.hook = Hook(player, Vec2(hook_end.position.x, hook_end.position.y))
                return
            hook_end.position.x += dx * 20
            hook_end.position.y += dy * 20

    # def load_textures(self):
    #     path = 'assets/blocks'
    #     for f in listdir(path):
    #         if isfile(join(path, f)):
    #             self.block_textures[f.replace('png', '')]

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.map.draw(self.screen, self.player.position)

        all = [*self.players.values(), self.player, *self.bullets]

        for obj in all:
            if obj is not None:
                obj.draw(self.screen, self.player.position)
        for particle in self.particles:
            particle.draw(self.screen, self.player.position)

        # minimap
