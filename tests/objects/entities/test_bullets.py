from scapy.contrib.isis import isis_lspid2str

from objects.entities.bullets import Bullet, BlowingBullet, Grenade
from objects.entities.effect import Particle
from objects.map.map import Map
from physics.vec2 import Vec2


def test_init(mocker):
    mocker.patch("objects.entities.Entity.__init__")
    bullet = Bullet(0, 0, 30, 30, 50)
    assert bullet.damage == 50
    assert bullet.lifetime == 0


def test_update(mocker):
    mocker.patch("objects.entities.Entity.update")
    bullet = Bullet(0, 0, 30, 30, 50)
    bullet.velocity = Vec2(10, 0)
    bullet.update()
    assert bullet.direction == Vec2(1, 0)
    assert bullet.lifetime > 0

    bullet = Grenade(0, 0, 30, 30, 50)
    bullet.velocity = Vec2(10, 0)
    bullet.lifetime = 299
    bullet.update()
    assert bullet.blowing



def test_collide(mocker):
    mocker.patch("pygame.image.load")
    mocker.patch("pygame.transform.scale")
    map = Map()
    map.load_from_list(["0;0", "25; 25; 50; 50;"], w_sprites=False)
    bullet = Bullet(0, 0, 30, 30, 50)
    bullet.collide(map)
    assert bullet.blowing

    bullet = Bullet(100, 100, 30, 30, 50)
    bullet.collide(map)
    assert not bullet.blowing

def test_collide_grenade(mocker):
    mocker.patch("pygame.image.load")
    mocker.patch("pygame.transform.scale")
    map = Map()
    map.load_from_list(["0;0", "25; 25; 50; 50;"], w_sprites=False)
    bullet = Grenade(-60, -60, 30, 30, 50)
    bullet.velocity = Vec2(10, 10)
    bullet.collide(map)
    assert not bullet.intersects(list(map.blocks.values())[0])

def test_get_particle(mocker):
    mocker.patch("other.functions.load_animation")
    bullet = BlowingBullet(0, 0, 30, 30, 50)
    particle = bullet.get_particle()
    assert isinstance(particle, Particle)

    bullet = Grenade(0, 0, 30, 30, 50)
    bullet.blowing = True
    particle = bullet.get_particle()
    assert isinstance(particle, Particle)




def test_draw(mocker):
    mock_entity_draw = mocker.patch("objects.entities.entity.Entity.draw")
    mocker.patch(
        "pygame.transform.rotate", return_value=mocker.Mock(return_value="rect")
    )
    mocker.patch("objects.entities.entity.Entity.load_images")
    bullet = Bullet(0, 0, 30, 30, 30)
    bullet.draw("screen", "center")
    mock_entity_draw.assert_called_once_with("screen", "center")

    bullet = Bullet(0, 0, 30, 30, 30, sprite_path="image")
    mock_screen = mocker.Mock()
    bullet.draw(mock_screen, "rect")


