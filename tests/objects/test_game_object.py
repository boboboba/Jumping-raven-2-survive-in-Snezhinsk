from objects.game_object import GameObject
from physics.vec2 import Vec2
from other.constants import WIDTH, HEIGHT
import pygame


def test_init():
    x = 200
    y = 300
    width = 50
    height = 60
    game_object = GameObject(x, y, width, height)
    assert game_object.position == Vec2(x, y)
    assert game_object.width == width
    assert game_object.height == height
    assert game_object.size == Vec2(width, height)


def test_get_points():
    game_object = GameObject(100, 200, 30, 70)
    assert game_object.top_left == Vec2(85, 165)
    assert game_object.bottom_right == Vec2(115, 235)
    assert game_object.corners == [
        Vec2(85, 165),
        Vec2(85, 235),
        Vec2(115, 235),
        Vec2(115, 165),
    ]


def test_intersect():
    game_object1 = GameObject(100, 100, 100, 100)
    game_object2 = GameObject(50, 0, 100, 150)
    assert game_object1.intersects(game_object2)
    game_object2.position = Vec2(0, 0)
    assert game_object1.intersects(game_object2)
    game_object2.position = Vec2(123123, 123123)
    assert not game_object1.intersects(game_object2)


def test_convert_coordinates():
    game_object = GameObject(100, 100, 100, 100)
    assert game_object.convert_coordinates(Vec2(0, 0)) == (
        Vec2(WIDTH / 2 + 100, HEIGHT / 2 + 100),
        Vec2(WIDTH / 2 + 50, HEIGHT / 2 + 50),
        Vec2(WIDTH / 2 + 150, HEIGHT / 2 + 150),
    )
    assert game_object.convert_coordinates(Vec2(-2000, 500)) == (
        Vec2(WIDTH / 2 + 2100, HEIGHT / 2 - 400),
        Vec2(WIDTH / 2 + 2050, HEIGHT / 2 - 450),
        Vec2(WIDTH / 2 + 2150, HEIGHT / 2 - 350),
    )


def test_draw(mocker):
    mocker.patch("pygame.draw.rect")
    game_object = GameObject(100, 100, 50, 50)
    screen = 1
    center = Vec2(200, 200)
    game_object.draw(screen, center)
    pygame.draw.rect.assert_called_once_with(screen, (255, 255, 0), (275, 175, 50, 50))


def test_get_particle():
    game_object = GameObject(100, 100, 100, 100)
    assert game_object.get_particle() is None
