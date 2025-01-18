import pytest
from unittest.mock import Mock

from objects import Entity
from objects.entities.buff import Buff, InvisibilityBuff, SpeedBuff, JumpBuff  # Замените your_module на реальный модуль

@pytest.fixture
def player():
    mock_player = Mock()
    mock_player.invisible = False
    mock_player.speed = 10
    mock_player.jump_force = 0
    return mock_player

def test_buff_initialization():
    buff = Buff(x=0, y=0, width=10, height=10, duration=5)
    assert buff.duration == 5
    assert not buff.ended
    assert buff.player is None

def test_invisibility_buff_apply(player):
    invisibility_buff = InvisibilityBuff(x=0, y=0, width=10, height=10, duration=5)
    invisibility_buff.apply(player)
    assert invisibility_buff.player == player
    assert player.invisible is True

def test_speed_buff_apply(player):
    speed_buff = SpeedBuff(x=0, y=0, width=10, height=10, duration=5)
    speed_buff.apply(player)
    assert speed_buff.player == player
    assert player.speed == 20

def test_jump_buff_apply(player):
    jump_buff = JumpBuff(x=0, y=0, width=10, height=10, duration=5)
    jump_buff.apply(player)
    assert jump_buff.player == player
    assert jump_buff.player.jump_force == (-Entity.GRAVITY * 40).y

def test_buff_update(player):
    buff = Buff(x=0, y=0, width=10, height=10, duration=2)
    buff.apply(player)
    buff.update()
    assert buff.duration == 1
    assert buff.ended is False

    buff.update()
    assert buff.duration == 0
    assert buff.ended is True

def test_invisibility_buff_update(player):
    invisibility_buff = InvisibilityBuff(x=0, y=0, width=10, height=10, duration=2)
    invisibility_buff.apply(player)
    invisibility_buff.update()
    assert invisibility_buff.duration == 1
    assert player.invisible is True

    invisibility_buff.update()
    assert invisibility_buff.duration == 0
    assert invisibility_buff.ended is True
    assert player.invisible is True  # Убедимся, что игрок остается невидимым

def test_speed_buff_update(player):
    speed_buff = SpeedBuff(x=0, y=0, width=10, height=10, duration=2)
    speed_buff.apply(player)
    speed_buff.update()
    assert speed_buff.duration == 1
    assert player.speed == 20

    speed_buff.update()
    assert speed_buff.duration == 0
    assert speed_buff.ended is True
    assert player.speed == 20  # Убедимся, что скорость остается увеличенной

def test_jump_buff_update(player):
    jump_buff = JumpBuff(x=0, y=0, width=10, height=10, duration=2)
    jump_buff.apply(player)
    jump_buff.update()
    assert jump_buff.duration == 1
    assert jump_buff.player.jump_force == (-Entity.GRAVITY * 40).y

    jump_buff.update()
    assert jump_buff.duration == 0
    assert jump_buff.ended is True
    assert jump_buff.player.jump_force == (-Entity.GRAVITY * 40).y  # Убедимся, что сила прыжка остается увеличенной

def test_invisibility_buff_delete(player):
    invisibility_buff = InvisibilityBuff(x=0, y=0, width=10, height=10, duration=5)
    invisibility_buff.apply(player)
    invisibility_buff.delete()
    assert player.invisible is False

def test_speed_buff_delete(player):
    speed_buff = SpeedBuff(x=0, y=0, width=10, height=10, duration=5)
    speed_buff.apply(player)
    speed_buff.delete()
    assert player.speed == 10

def test_jump_buff_delete(player):
    jump_buff = JumpBuff(x=0, y=0, width=10, height=10, duration=5)
    jump_buff.apply(player)
    jump_buff.delete()
    assert jump_buff.player.jump_force == (-Entity.GRAVITY * 20).y
