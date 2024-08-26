class Hitbox:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def intersects(self, other) -> bool:
        return (max(self.x, other.x) <= min(self.x + self.width, other.x + other.width) and
                max(self.y, other.y) <= min(self.y + self.height, other.y + other.height))
