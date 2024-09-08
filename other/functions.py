import pygame as pg


def load_animation(file_name):
    sprite_sheet = pg.image.load(file_name).convert_alpha()

    sprites = []
    for i in range(sprite_sheet.get_width() // sprite_sheet.get_height()):
        surface = pg.Surface((32, 32), pg.SRCALPHA, 32)
        rect = pg.Rect(i * 32, 0, 32, 32)
        surface.blit(sprite_sheet, (0, 0), rect)
        sprites.append(surface)
    return sprites
