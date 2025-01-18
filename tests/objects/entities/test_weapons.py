import pytest
from unittest.mock import patch, MagicMock
from objects.entities.weapons import Gun, ShotGun, Rocket, Egg
from physics.vec2 import Vec2

@pytest.fixture
def mock_pygame():
    with patch('pygame.image.load', return_value=MagicMock()), \
         patch('pygame.transform.scale', return_value=MagicMock()), \
         patch('pygame.transform.rotate', return_value=MagicMock()), \
         patch('pygame.transform.flip', return_value=MagicMock()):
        yield

def test_gun_get_bullet(mock_pygame):
    gun = Gun(0, 0, 50, "path/to/sprite.png")
    gun.direction = Vec2(1, 0)
    bullets = gun.get_bullet()

    assert len(bullets) == 1
    assert bullets[0].position == Vec2(0, 0) + Vec2(1, 0) * (gun.dist / 2)
    assert bullets[0].velocity == Vec2(50, 0)

def test_shotgun_get_bullet(mock_pygame):
    shotgun = ShotGun(0, 0, 50, "path/to/sprite.png")
    shotgun.direction = Vec2(1, 0)
    bullets = shotgun.get_bullet()

    assert len(bullets) == 5
    for bullet in bullets:
        assert Vec2(1,0).dot(bullet.direction) > 0

def test_rocket_get_bullet(mock_pygame):
    rocket = Rocket(0, 0, 50, "path/to/sprite.png")
    rocket.direction = Vec2(1, 0)
    bullets = rocket.get_bullet()

    assert len(bullets) == 1
    assert bullets[0].position == rocket.position + rocket.direction * (rocket.dist / 2)
    assert bullets[0].velocity == rocket.direction * 15

def test_egg_get_bullet(mock_pygame):
    egg = Egg(0, 0, 50, "path/to/sprite.png")
    egg.direction = Vec2(1, 0)  # Установим направление
    bullets = egg.get_bullet()

    assert len(bullets) == 1
    assert bullets[0].position == egg.position - egg.direction * 60 + Vec2(0, 60)


def test_gun_draw(mock_pygame):
    gun = Gun(0, 0, 50, "path/to/sprite.png")
    gun.direction = Vec2(1, 0)
    screen = MagicMock()
    center = Vec2(100, 100)

    gun.draw(screen, center)
    screen.blit.assert_called_once()


