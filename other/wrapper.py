import sys

from objects.entities.buff import Buff, SpeedBuff, InvisibilityBuff, JumpBuff
from objects.hook import Hook
from objects.entities.player import Player
from objects.entities.bullets import Bullet, BlowingBullet


class Wrap:
    def __init__(self, obj):
        from objects.entities.player import Player
        from objects.entities.bullets import Bullet

        self.id = -1
        self.position = obj.position
        self.velocity = obj.velocity
        self.size = obj.size
        self.width = obj.width
        self.height = obj.height
        self.direction = obj.direction
        self.sprite_path = obj.sprite_path
        self.team = obj.team

        if isinstance(obj, Player):
            self.invisible = obj.invisible
            self.state = obj.state
            self.current_weapon = obj.current_weapon
            if obj.hook:
                self.hook_end = obj.hook.point
            else:
                self.hook_end = None
        elif isinstance(obj, Bullet):
            if isinstance(obj, BlowingBullet):
                self.radius = obj.radius
            self.damage = obj.damage
        elif isinstance(obj, Buff):
            self.duration = obj.duration

        self.type = type(obj).__name__

    def get_new(self):
        type = getattr(sys.modules[__name__], self.type)
        obj = None
        if issubclass(type, Player):
            obj = Player(
                self.position.x,
                self.position.y,
                self.width,
                self.height,
                self.sprite_path,
            )
            obj.state = self.state
            obj.load_images()
            obj.load_animations()
            if self.hook_end:
                obj.hook = Hook(obj, self.hook_end)
        elif issubclass(type, Bullet):
            obj = type(
                self.position.x,
                self.position.y,
                self.width,
                self.height,
                self.damage,
                self.sprite_path,
            )
            if issubclass(type, BlowingBullet):
                obj.radius = self.radius
        elif issubclass(type, Buff):
            obj = type(
                self.position.x,
                self.position.y,
                self.width,
                self.height,
                self.duration,
                sprite_path=self.sprite_path,
            )
        obj.velocity = self.velocity
        obj.team = self.team
        return obj
