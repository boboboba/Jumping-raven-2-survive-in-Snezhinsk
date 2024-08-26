import pickle

import pygame as pg

from block import Block
from game import Game
from constants import *
from physics.vec2 import Vec2
from os import listdir
from os.path import isfile, join


class Menu:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.buttons = []
        self.font = pg.font.SysFont("Comic Sans", 18)
        # self.game = Game(screen)

    def run(self):

        def game():
            game = Game(self.screen)
            game.run()

        def redactor():
            redactor = Redactor(self.screen)
            redactor.run()

        button = Button(300, 200, 200, 50, text='Play')
        button.onclick = game
        self.buttons.append(button)
        button = Button(300, 300, 200, 50, text='Redactor', color=(64, 64, 64))
        button.onclick = redactor
        self.buttons.append(button)
        clock = pg.time.Clock()
        while True:
            self.screen.fill((0, 0, 0))
            events = pg.event.get()
            for button in self.buttons:
                button.update(events)
                button.draw(self.screen)

            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
            pg.display.flip()
            clock.tick(60)


class Button:
    def __init__(self, x, y, width, height, text=None, color=None, sprite=None):
        self.sprite = None
        if sprite is not None:
            self.sprite = pg.transform.scale(pg.image.load(sprite), (width, height))
        self.color = color if color is not None else (128, 128, 128)
        self.border_color = (255, 255, 255, 0)
        self.active_border_color = (0, 0, 128)
        self.border_width = 5
        self.text = text
        self.onclick = None
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.font = pg.font.SysFont("Comic Sans", 18)

    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONUP:
                if (self.x <= pg.mouse.get_pos()[0] <= self.x + self.width
                        and self.y <= pg.mouse.get_pos()[1] <= self.y + self.height):
                    if self.onclick is not None:
                        self.onclick()
    def draw(self, screen):
        if (self.x <= pg.mouse.get_pos()[0] <= self.x + self.width
                and self.y <= pg.mouse.get_pos()[1] <= self.y + self.height):
            rect = (self.x - self.border_width,
                    self.y - self.border_width,
                    self.width + 2 * self.border_width,
                    self.height + 2 * self.border_width)
            pg.draw.rect(screen, self.border_color, rect)
        if self.sprite is not None:
            screen.blit(self.sprite, (self.x, self.y))
        else:
            pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        if self.text is not None:
            surf = self.font.render(self.text, True, (255, 255, 255))
            w = surf.get_width()
            h = surf.get_height()
            screen.blit(surf, (self.x + (self.width - w) / 2, self.y + (self.height - h) / 2))


class Redactor:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.start = None
        self.end = None
        self.current_block = 0
        self.map_area = pg.Rect(WIDTH // 4, 50, WIDTH // 3 * 4, HEIGHT)
        self.tile_size = 25
        path = join('assets', 'blocks')
        self.images_paths = [join(path, f)
                             for f in listdir(path) if isfile(join(path, f))]
        self.images = [pg.transform.scale(
            pg.image.load(image_path), (self.tile_size, self.tile_size))
            for image_path in self.images_paths]

        self.blocks = []
        self.center = Vec2(WIDTH // 2, HEIGHT // 2)
        self.mode = 'place'

    def run(self):
        clock = pg.time.Clock()
        button = Button(0, 0, 200, 50, text='Save')
        button.onclick = self.save
        self.buttons.append(button)
        self.add_buttons()
        def place():
            self.mode = 'place'
        def delete():
            self.mode = 'delete'
        button = Button(205, 0, 200, 50, text='Delete')
        button.onclick = delete
        self.buttons.append(button)
        button = Button(410, 0, 200, 50, text='Place')
        button.onclick = place
        self.buttons.append(button)
        button = Button(615, 0, 200, 50, text='Load map')
        button.onclick = self.load
        self.buttons.append(button)
        self.add_buttons()
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return
                if event.type == pg.QUIT:
                    pg.quit()
            if pg.mouse.get_pressed(3)[0] and self.map_area.collidepoint(pg.mouse.get_pos()):
                pos = pg.mouse.get_pos()
                x = (pos[0] + self.center.x - WIDTH / 2) // self.tile_size * self.tile_size + self.tile_size / 2
                y = (pos[1] + self.center.y - HEIGHT / 2) // self.tile_size * self.tile_size + self.tile_size / 2
                for placed_block in self.blocks:
                    if Vec2(x, y) == placed_block.position:
                        self.blocks.remove(placed_block)
                if self.mode == 'place':
                    block = Block(x, y, self.tile_size, self.tile_size, self.images_paths[self.current_block])
                    block.sprite = self.images[self.current_block]
                    self.blocks.append(block)

            if pg.key.get_pressed()[pg.K_LEFT]:
                self.center.x -= 4
            if pg.key.get_pressed()[pg.K_RIGHT]:
                self.center.x += 4
            if pg.key.get_pressed()[pg.K_UP]:
                self.center.y -= 4
            if pg.key.get_pressed()[pg.K_DOWN]:
                self.center.y += 4

            for button in self.buttons:
                button.update(events)
            self.draw()

            pg.display.flip()
            clock.tick(60)

    def add_buttons(self):
        button_size = 32
        rect = (0, 50, WIDTH // 4, HEIGHT)
        count_horizontal = rect[2] // (button_size +5)
        count_vertical = 16
        spacing_horizontal = (rect[2] - count_horizontal * button_size) // (count_horizontal + 1)
        spacing_vertical = (rect[3] - count_vertical * button_size) // (count_vertical + 1)

        current_block = 0
        for y in range(rect[1] + spacing_vertical,
                       rect[1] + rect[3] - (count_vertical + 1),
                       spacing_vertical + button_size):
            for x in range(rect[0] + spacing_horizontal,
                           rect[0] + rect[2] - (count_horizontal + 1),
                           spacing_horizontal + button_size):
                if current_block >= len(self.images):
                    return
                button = Button(x, y, button_size, button_size)
                button.sprite = pg.transform.scale(self.images[current_block], (button_size, button_size))

                def change_block(current_block=current_block):
                    self.current_block = current_block

                button.onclick = change_block
                self.buttons.append(button)
                current_block += 1

    def draw(self):

        self.screen.fill((0, 0, 0))
        # grid
        for i in range(self.tile_size - self.center.y % self.tile_size, HEIGHT, self.tile_size):
            pg.draw.line(self.screen, (64, 64, 64), (0, i), (WIDTH, i), )
        for i in range(self.tile_size - self.center.x % self.tile_size, WIDTH, self.tile_size):
            pg.draw.line(self.screen, (64, 64, 64), (i, 0), (i, HEIGHT), )
        for block in self.blocks:
            block.draw(self.screen, self.center)
        pg.draw.rect(self.screen, (0, 0, 255), (0, 0, WIDTH / 4, HEIGHT))
        for button in self.buttons:
            button.draw(self.screen)

        if self.start is not None:
            pg.draw.rect(self.screen, (255, 255, 255),
                         (self.start.x, self.start.y, (self.end - self.start).x, (self.end - self.start).y))

        mouse_pos = pg.mouse.get_pos()
        pos = ((mouse_pos[0] + self.center.x % self.tile_size) // self.tile_size * self.tile_size - self.center.x % self.tile_size,
               (mouse_pos[1] + self.center.y % self.tile_size) // self.tile_size * self.tile_size - self.center.y % self.tile_size)
        if self.map_area.collidepoint(pos) and self.mode == 'place':
            self.screen.blit(self.images[self.current_block], pos)


    def save(self):
        with open('map.txt', 'w') as f:
            for block in self.blocks:
                f.write(';'.join(
                    str(x * 2) for x in [block.position.x, block.position.y, block.width, block.height]) + f';{block.sprite_path}' + '\n')

    def load(self):
        with open('map.txt', 'r') as f:
            self.blocks = []
            for line in f.readlines():
                x,y,w,h,sprite = line.split(';')
                x =float(x)/2
                y =float(y)/2
                w =float(w)/2
                h =float(h)/2
                sprite = sprite[:-1]
                block = Block(x,y,w,h,sprite_path=sprite)
                self.blocks.append(block)
