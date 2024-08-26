import socket
import pygame as pg
from game import Game
from constants import *
from menu import Menu

def main():
    menu = Menu()
    menu.run()
    # pg.init()
    # screen = pg.display.set_mode((WIDTH, HEIGHT))
    # game = Game(screen)
    # game.run()

if __name__ == '__main__':
    main()
