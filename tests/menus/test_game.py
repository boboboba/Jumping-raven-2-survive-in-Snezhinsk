import threading
import time

import pygame
import pytest
from unittest.mock import MagicMock, patch
from menus.game import Game
from objects.entities.player import  Player
from objects.map.map import Map
from physics.vec2 import Vec2


@pytest.fixture
def mock_pygame():
    with patch('pygame.image.load', return_value=MagicMock()), \
         patch('pygame.transform.scale', return_value=MagicMock()), \
         patch('pygame.transform.rotate', return_value=MagicMock()), \
         patch('pygame.draw.rect', return_value=None), \
         patch('pygame.event.get', return_value=None), \
         patch('pygame.display', return_value=None), \
         patch('pygame.mouse.get_pos', return_value=(100, 100)):
        yield

@pytest.fixture
@patch('objects.entities.entity.Entity.load_animations')
def mock_game(mock_load_animations, mock_pygame):
    screen = MagicMock()  # Создаем мок экрана
    game = Game(screen)
    return game

def test_game_initialization(mock_game, mock_pygame):
    game = mock_game
    assert game.team == -1  # Проверяем, что команда по умолчанию -1
    assert isinstance(game.map, Map)  # Проверяем, что карта инициализирована
    assert isinstance(game.player, Player)  # Проверяем, что игрок инициализирован
    assert game.player.position == game.map.spawn_position  # Проверяем позицию игрока

@patch('menus.game.Game.controls')
@patch('menus.game.Game.draw')
def test_game_run(_, __, mock_game, mock_pygame):
    game = mock_game
    def kill():
        time.sleep(1)
        game.dead = True
    thread = threading.Thread(target=kill)
    thread.start()
    game.run()  # Запускаем игру
    assert game.running is False  # Проверяем, что игра завершилась

@patch('pygame.key.get_pressed')
@patch('menus.game.Game.throw_hook')
def test_game_controls_keydown(mock_throw_hook, _, mock_game):
    game = mock_game
    events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_SPACE),
              MagicMock(type=pygame.KEYDOWN, key=pygame.K_q),
              MagicMock(type=pygame.KEYDOWN, key=pygame.K_e),]
    game.controls(events)  # Передаем события управления
    assert game.player.velocity.y < -1
    assert game.player.jump_count == 1
    assert not game.player.is_landed
    mock_throw_hook.assert_called_once()

@patch('objects.entities.player.Player.shoot', return_value=[MagicMock(name='1'),
                                                       MagicMock(name='2')])
@patch('web_code.network.Network')
@patch('pygame.key.get_pressed')
def test_game_controls_mouse(mock_player_shoot, _, mock_network, mock_game):
    game = mock_game
    events = [MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1),
              MagicMock(type=pygame.MOUSEBUTTONDOWN, button=3),]
    game.controls(events)  # Передаем события управления

    mock_player_shoot.assert_called_once()
    assert game.bullets.__len__() == 2
    assert game.player.current_weapon == 1

def test_game_check_collisions(mock_game):
    game = mock_game
    entity = MagicMock()  # Создаем мок-объект для проверки коллизий
    game.check_collisions([entity])  # Проверяем коллизии

    entity.collide.assert_called_once_with(game.map)  # Проверяем, что метод collide был вызван

@patch('objects.entities.entity.Entity.update')
def test_game_update_entities(mock_update, mock_game):
    game = mock_game
    game.players = {1:MagicMock()}
    game.update_entities()
    mock_update.assert_called_once()

def test_game_throw_hook(mock_game):
    game = mock_game
    game.player.position = Vec2(-10, -20)
    game.player.direction = Vec2(1, 1)
    game.map.blocks = {(25,25): 123}

    game.throw_hook(game.player)  # Вызываем метод броска крюка

    assert game.player.hook is not None  # Проверяем, что крюк был создан

def test_game_easter_egg(mock_game):
    game = mock_game
    game.pressed_keys = list("aezakmi")  # Устанавливаем нажатые клавиши
    game.easter_egg()  # Проверяем Easter Egg

    assert game.player.max_jumps == 999999  # Проверяем, что максимальное количество прыжков увеличилось

@patch('objects.map.map.Map.draw')
def test_game_draw(mock_map_draw, mock_game):
    game = mock_game
    game.draw()  # Вызываем метод отрисовки

    game.screen.fill.assert_called_once_with((0, 0, 0))  # Проверяем, что экран был очищен
    mock_map_draw.assert_called_once_with(game.screen, game.player.position)  # Проверяем, что карта отрисована
