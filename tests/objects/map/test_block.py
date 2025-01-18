import pytest
from unittest.mock import MagicMock, patch
from objects.map.block import Block
from physics.vec2 import Vec2
from os.path import join
from other.constants import ROOT
import pygame as pg

@pytest.fixture
@patch('pygame.image.load')
@patch('pygame.transform.scale')
def block_instance(mock_load, mock_scale):
    return Block(100, 100, 50, 50, "path/to/sprite.png")

@pytest.fixture
def mock_screen():
    return MagicMock()

@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_initialization(mock_scale, mock_load):
    mock_image = MagicMock()
    mock_load.return_value = mock_image
    mock_scale.return_value = mock_image
    block_instance = Block(100, 100, 50, 50, "path/to/sprite.png")


    assert block_instance.position == Vec2(100, 100)
    assert block_instance.width == 50
    assert block_instance.height == 50
    assert block_instance.local_path == "path/to/sprite.png"
    assert block_instance.sprite is not None
    mock_load.assert_called_once_with(block_instance.sprite_path)
    mock_scale.assert_called_once_with(mock_image, (50, 50))

@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_initialization_without_sprite(mock_scale, mock_load):
    block = Block(100, 100, 50, 50)

    assert block.sprite is None
    assert block.local_path == ""

def test_sprite_path(block_instance):
    expected_path = join(ROOT, "path/to/sprite.png")
    assert block_instance.sprite_path == expected_path

@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_draw_with_sprite(mock_scale, mock_load, mock_screen):
    mock_image = MagicMock()
    mock_load.return_value = mock_image
    mock_scale.return_value = mock_image

    center = Vec2(0, 0)
    block_instance = Block(100, 100, 50, 50, "path/to/sprite.png")
    block_instance.draw(mock_screen, Vec2(400, 300))

    mock_screen.blit.assert_called_once_with(mock_image, (75, 75, 50, 50))

@patch('pygame.image.load')
@patch('pygame.transform.scale')
@patch('pygame.draw.rect')
def test_draw_without_sprite(mock_load, mock_scale, mock_draw_rect, mock_screen):
    block = Block(100, 100, 50, 50)

    center = Vec2(0, 0)
    block.draw(mock_screen, center)

    assert mock_draw_rect.call_count == 0