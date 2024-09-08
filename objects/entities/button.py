import pygame as pg


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
                if (
                    self.x <= pg.mouse.get_pos()[0] <= self.x + self.width
                    and self.y <= pg.mouse.get_pos()[1] <= self.y + self.height
                ):
                    if self.onclick is not None:
                        self.onclick()
                        return True

    def draw(self, screen):
        if (
            self.x <= pg.mouse.get_pos()[0] <= self.x + self.width
            and self.y <= pg.mouse.get_pos()[1] <= self.y + self.height
        ):
            rect = (
                self.x - self.border_width,
                self.y - self.border_width,
                self.width + 2 * self.border_width,
                self.height + 2 * self.border_width,
            )
            pg.draw.rect(screen, self.border_color, rect)
        if self.sprite is not None:
            screen.blit(self.sprite, (self.x, self.y))
        else:
            pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        if self.text is not None:
            surf = self.font.render(self.text, True, (255, 255, 255))
            w = surf.get_width()
            h = surf.get_height()
            screen.blit(
                surf, (self.x + (self.width - w) / 2, self.y + (self.height - h) / 2)
            )
