import pygame as pg
from menus.game import Game
from other.constants import *
from menus.redactor import Redactor
from objects.entities.button import Button


class Menu:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.buttons = []
        self.font = pg.font.SysFont("Comic Sans", 18)

    def run(self):

        def game():
            game = Game(self.screen)
            game.run()

        def redactor():
            redactor = Redactor(self.screen)
            redactor.run()

        button = Button(300, 200, 200, 50, text="Play")
        button.onclick = game
        self.buttons.append(button)
        button = Button(300, 300, 200, 50, text="Redactor", color=(64, 64, 64))
        button.onclick = redactor
        self.buttons.append(button)
        button = Button(300, 400, 200, 50, text="Exit", color=(64, 64, 64))
        button.onclick = pg.quit
        self.buttons.append(button)
        clock = pg.time.Clock()
        while True:
            self.screen.fill((0, 0, 0))
            events = pg.event.get()
            for button in self.buttons:
                if button.update(events):
                    break
                button.draw(self.screen)

            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
            pg.display.flip()
            clock.tick(60)
