import math
from unittest.mock import MagicMock, patch, ANY

import pygame as pg
import pytest

from objects.entities.player import Player
from objects.hook import Hook
from physics.vec2 import Vec2


@pytest.fixture
def hook(player):
    return Hook(player, Vec2(100, 100))
@pytest.fixture
@patch('pygame.image.load')
@patch('pygame.transform.scale')
@patch('objects.entities.player.Player.load_animations')
def player(mock_load_animations, _, __):
    player = MagicMock()
    player.convert_coordinates.return_value = (Vec2(100, 100), 0,0)
    player.velocity = Vec2(0,0 )
    return player

@patch('pygame.draw.line')
def test_draw(mock_draw, hook, player):
    center = Vec2(0, 0)
    hook.draw(MagicMock(), center)
    mock_draw.assert_called_once_with(ANY,ANY, (100, 100), (500, 400), ANY)

def test_update_within_distance(hook, player):
    player.position = Vec2(150, 150)
    hook.update()
    assert abs(player.velocity.x + math.sqrt(2)) < 1e-5
    assert abs(player.velocity.y + math.sqrt(2)) < 1e-5

def test_update_outside_distance(hook, player):
    player.position = Vec2(500, 500)
    hook.update()
    player.move.assert_called_once()
