from unittest.mock import MagicMock, patch, mock_open
import pytest
from objects.map.map import Map
from physics.vec2 import Vec2


@pytest.fixture
def map_instance():
    return Map()

@pytest.fixture
def mock_screen():
    return MagicMock()

@pytest.fixture
def mock_block():
    with patch('objects.map.block.Block', autospec=True) as MockBlock:
        yield MockBlock

def test_initialization(map_instance):
    assert map_instance.tile_size == 50
    assert map_instance.spawn_position == Vec2(0, 0)
    assert isinstance(map_instance.blocks, dict)
    assert map_instance.image is not None

@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_load_from_file(mock_scale, mock_load, map_instance):
    mock_image = MagicMock()
    mock_load.return_value = mock_image
    mock_scale.return_value = mock_image

    test_file_content = "100;200\n0;0;50;50;path/to/sprite.png\n"
    with patch('builtins.open', mock_open(read_data=test_file_content)):
        map_instance.load_from_file('dummy_path.txt')

    assert map_instance.spawn_position == Vec2(100, 200)
    assert (0, 0) in map_instance.blocks
    assert map_instance.blocks[(0, 0)].width == 50
    assert map_instance.blocks[(0, 0)].height == 50
    assert map_instance.blocks[(0, 0)].sprite_path.endswith("path/to/sprite.png")

@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_load_from_list(mock_load, mock_scale, map_instance):
    lines = ["100;200\n", "0;0;50;50;path/to/sprite.png\n"]
    map_instance.load_from_list(lines)

    assert map_instance.spawn_position == Vec2(100, 200)
    assert (0, 0) in map_instance.blocks
    assert map_instance.blocks[(0, 0)].width == 50
    assert map_instance.blocks[(0, 0)].height == 50
    assert map_instance.blocks[(0, 0)].sprite_path.endswith("path/to/sprite.png")

def test_draw(map_instance, mock_screen, mock_block):
    map_instance.blocks[(0, 0)] = mock_block.return_value
    center = Vec2(400, 300)

    map_instance.draw(mock_screen, center)

    assert mock_screen.blit.call_count == 4
    mock_block.return_value.draw.assert_called_once_with(mock_screen, center)