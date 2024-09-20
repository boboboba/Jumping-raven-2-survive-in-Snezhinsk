import pygame as pg
from tkinter import filedialog

from objects.map.block import Block
from other.constants import *
from physics.vec2 import Vec2
from os import listdir
from os.path import isfile, join
from objects.entities.button import Button


class Redactor:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.current_block = 0
        self.map_area = pg.Rect(WIDTH // 4, 50, WIDTH // 3 * 4, HEIGHT)
        self.tile_size = 25
        path = join(ROOT, "assets", "blocks")
        self.images_paths = [
            join(path, f) for f in listdir(path) if isfile(join(path, f))
        ]
        spawn_image = pg.transform.scale(
            pg.image.load(join(ROOT, "assets", "player", "spawn.png")),
            (self.tile_size, self.tile_size),
        )
        self.spawn = Block(
            512.5,
            312.5,
            self.tile_size,
            self.tile_size,
            sprite_path=join("../assets", "player", "spawn.png"),
        )
        self.images = [spawn_image] + [
            pg.transform.scale(
                pg.image.load(image_path), (self.tile_size, self.tile_size)
            )
            for image_path in self.images_paths
        ]

        self.blocks = []
        self.center = Vec2(WIDTH // 2, HEIGHT // 2)
        self.mode = "place"
        self.scale = 0.5

    def run(self):
        clock = pg.time.Clock()
        button = Button(0, 0, 200, 50, text="Save")
        button.onclick = self.save
        self.buttons.append(button)
        self.add_buttons()

        def place():
            self.mode = "place"

        def delete():
            self.mode = "delete"

        button = Button(205, 0, 200, 50, text="Delete")
        button.onclick = delete
        self.buttons.append(button)
        button = Button(410, 0, 200, 50, text="Place")
        button.onclick = place
        self.buttons.append(button)
        button = Button(615, 0, 200, 50, text="Load map")
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
            if pg.mouse.get_pressed(3)[0] and self.map_area.collidepoint(
                pg.mouse.get_pos()
            ):
                pos = pg.mouse.get_pos()
                x = (
                    pos[0] + self.center.x - WIDTH / 2
                ) // self.tile_size * self.tile_size + self.tile_size / 2
                y = (
                    pos[1] + self.center.y - HEIGHT / 2
                ) // self.tile_size * self.tile_size + self.tile_size / 2

                for placed_block in self.blocks:
                    if Vec2(x, y) == placed_block.position:
                        self.blocks.remove(placed_block)
                if self.current_block == 0:
                    self.spawn = Block(
                        x,
                        y,
                        self.tile_size,
                        self.tile_size,
                        self.images_paths[self.current_block - 1],
                    )
                    self.spawn.sprite = self.images[self.current_block]
                elif self.mode == "place" and self.spawn.position != Vec2(x, y):
                    block = Block(
                        x,
                        y,
                        self.tile_size,
                        self.tile_size,
                        self.images_paths[self.current_block - 1],
                    )
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
        count_horizontal = rect[2] // (button_size + 5)
        count_vertical = 16
        spacing_horizontal = (rect[2] - count_horizontal * button_size) // (
            count_horizontal + 1
        )
        spacing_vertical = (rect[3] - count_vertical * button_size) // (
            count_vertical + 1
        )

        current_block = 0
        for y in range(
            rect[1] + spacing_vertical,
            rect[1] + rect[3] - (count_vertical + 1),
            spacing_vertical + button_size,
        ):
            for x in range(
                rect[0] + spacing_horizontal,
                rect[0] + rect[2] - (count_horizontal + 1),
                spacing_horizontal + button_size,
            ):
                if current_block >= len(self.images):
                    return
                button = Button(x, y, button_size, button_size)
                button.sprite = pg.transform.scale(
                    self.images[current_block], (button_size, button_size)
                )

                def change_block(current_block=current_block):
                    self.current_block = current_block

                button.onclick = change_block
                self.buttons.append(button)
                current_block += 1

    def draw(self):

        self.screen.fill((0, 0, 0))
        # grid
        for i in range(
            self.tile_size - self.center.y % self.tile_size, HEIGHT, self.tile_size
        ):
            pg.draw.line(
                self.screen,
                (64, 64, 64),
                (0, i),
                (WIDTH, i),
            )
        for i in range(
            self.tile_size - self.center.x % self.tile_size, WIDTH, self.tile_size
        ):
            pg.draw.line(
                self.screen,
                (64, 64, 64),
                (i, 0),
                (i, HEIGHT),
            )
        for block in self.blocks:
            block.draw(self.screen, self.center)
        if self.spawn is not None:
            self.spawn.draw(self.screen, self.center)
        pg.draw.rect(self.screen, (0, 0, 255), (0, 0, WIDTH / 4, HEIGHT))
        for button in self.buttons:
            button.draw(self.screen)

        mouse_pos = pg.mouse.get_pos()
        pos = (
            (mouse_pos[0] + self.center.x % self.tile_size)
            // self.tile_size
            * self.tile_size
            - self.center.x % self.tile_size,
            (mouse_pos[1] + self.center.y % self.tile_size)
            // self.tile_size
            * self.tile_size
            - self.center.y % self.tile_size,
        )
        if self.map_area.collidepoint(pos) and self.mode == "place":
            self.screen.blit(self.images[self.current_block], pos)

    def save(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension="txt",
            initialdir=join("../assets", "maps"),
            filetypes=(("TXT files", "*.txt"),),
        )
        if filepath == "":
            return
        with open(filepath, "w") as f:
            f.write(
                ";".join((str(x / self.scale) for x in self.spawn.position.tuple))
                + "\n"
            )
            for block in self.blocks:
                f.write(
                    ";".join(
                        str(x / self.scale)
                        for x in [
                            block.position.x,
                            block.position.y,
                            block.width,
                            block.height,
                        ]
                    )
                    + f";{block.sprite_path}"
                    + "\n"
                )

    def load(self):
        filepath = filedialog.askopenfilename(
            initialdir=join("../assets", "maps"), filetypes=(("TXT files", "*.txt"),)
        )
        if filepath == "":
            return
        with open(filepath, "r") as f:
            self.blocks = []
            first = True
            for line in f.readlines():
                if first:
                    x, y = (float(i) * self.scale for i in line.split(";"))
                    self.spawn = Block(
                        x,
                        y,
                        self.tile_size,
                        self.tile_size,
                        sprite_path=join("../assets", "player", "spawn.png"),
                    )
                    first = False
                    continue
                x, y, w, h, sprite = line.split(";")
                x = float(x) * self.scale
                y = float(y) * self.scale
                w = float(w) * self.scale
                h = float(h) * self.scale
                sprite = sprite[:-1]
                block = Block(x, y, w, h, sprite_path=sprite)
                self.blocks.append(block)
