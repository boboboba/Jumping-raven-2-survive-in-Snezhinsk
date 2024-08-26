import math


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, coefficient):
        return Vec2(self.x * coefficient, self.y * coefficient)

    def __rmul__(self, coefficient):
        return Vec2(self.x * coefficient, self.y * coefficient)

    def __truediv__(self, coefficient):
        return Vec2(self.x / coefficient, self.y / coefficient)

    def __floordiv__(self, coefficient):
        return Vec2(self.x // coefficient, self.y // coefficient)

    def __mod__(self, coefficient):
        return Vec2(self.x % coefficient, self.y % coefficient)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __eq__(self, other):
        if not isinstance(other, Vec2):
            return False

        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"(x: {self.x}, y: {self.y})"

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def normalize(self):
        length = self.length()
        return self / length if length != 0 else Vec2(0, 0)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def rotate(self, angle):
        sin = math.sin(angle)
        cos = math.cos(angle)

        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        return Vec2(x, y)

    @property
    def tuple(self):
        return (self.x, self.y)


