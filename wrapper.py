from hook import Hook
from player import Player
from bullets import *

class Wrap:
    def __init__(self, obj):
        from player import Player
        from bullets import Bullet
        self.id = -1
        self.position = obj.position
        self.velocity = obj.velocity
        self.size = obj.size
        self.width = obj.width
        self.height = obj.height
        self.direction = obj.direction
        self.assets_directory = obj.assets_directory
        if obj.assets_directory == None:
            pass
        if isinstance(obj, Player):
            self.type = 'player'
            self.state = obj.state
            self.current_weapon = obj.current_weapon
            if obj.hook:
                self.hook_end = obj.hook.point
            else:
                self.hook_end = None
        elif isinstance(obj, Bullet):
            self.sprite_path = obj.sprite_path
            self.type = 'bullet'
            if isinstance(obj, BlowingBullet):
                self.type = 'bbullet'
            self.damage = obj.damage

    def get_new(self):
        if self.type == 'player':
            player = Player(self.position.x, self.position.y, self.width, self.height, self.assets_directory)
            player.state = self.state
            player.load_images()
            player.load_animations()
            if self.hook_end:
                player.hook = Hook(player, self.hook_end)
            return player
        elif self.type == 'bullet':
            bullet = Bullet(self.position.x, self.position.y, self.width, self.height, self.damage, self.sprite_path)
            bullet.velocity = self.velocity
            return bullet
        elif self.type == 'bbullet':
            bullet = BlowingBullet(self.position.x, self.position.y, self.width, self.height, self.damage, self.sprite_path)
            bullet.velocity = self.velocity
            return bullet

