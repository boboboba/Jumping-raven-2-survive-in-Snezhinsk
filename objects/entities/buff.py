from objects.entities.entity import Entity


class Buff(Entity):
    def __init__(self, x, y, width, height, duration, sprite_path=None):
        super().__init__(x, y, width, height, sprite_path=sprite_path)
        self.duration = duration
        self.ended = False
        self.player = None

    def apply(self, player):
        self.player = player

    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.ended = True

    def delete(self):
        pass


class InvisibilityBuff(Buff):
    def apply(self, player):
        super().apply(player)
        self.player.invisible = True

    def update(self):
        super().update()
        self.player.invisible = True

    def delete(self):
        self.player.invisible = False


class SpeedBuff(Buff):
    def apply(self, player):
        super().apply(player)
        self.player.speed = 20

    def update(self):
        super().update()
        self.player.speed = 20

    def delete(self):
        self.player.speed = 10


class JumpBuff(Buff):
    def apply(self, player):
        super().apply(player)
        self.player.jump_force = (-Entity.GRAVITY * 40).y

    def update(self):
        super().update()
        self.player.jump_force = (-Entity.GRAVITY * 40).y

    def delete(self):
        self.player.jump_force = (-Entity.GRAVITY * 20).y
