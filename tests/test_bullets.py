from objects.entities.bullets import Bullet
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


def test_collide(mocker):
    mocker.patch("pygame.image.load")
    mocker.patch("pygame.transform.scale")
    map = Map()
    map.load_from_list(["0;0", "25; 25; 50; 50;"], w_sprites=False)
    bullet = Bullet(0, 0, 30, 30, 50, 50)
    bullet.collide(map)
    assert not bullet.alive

    bullet = Bullet(100, 100, 30, 30, 50, 50)
    bullet.collide(map)
    assert bullet.alive


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
