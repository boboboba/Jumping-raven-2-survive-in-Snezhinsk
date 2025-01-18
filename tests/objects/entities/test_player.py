import pytest
from unittest.mock import patch, MagicMock
from objects.entities.player import Player
from objects.entities.buff import Buff
from objects.entities.bullets import Bullet, BlowingBullet  # Замените `your_module` на фактическое имя вашего модуля
from physics.vec2 import Vec2
from other.constants import WIDTH, HEIGHT

@pytest.fixture
def mock_pygame():
    with patch('pygame.image.load', return_value=MagicMock()), \
         patch('pygame.transform.scale', return_value=MagicMock()), \
         patch('pygame.transform.rotate', return_value=MagicMock()), \
         patch('pygame.draw.rect', return_value=None), \
         patch('pygame.mouse.get_pos', return_value=(100, 100)):
        yield

# @patch('objects.entities.player.Player.load_animations')
def test_player_initialization(mock_pygame):
    def mock_load_animations(self):
        self.animations['stand'] = [MagicMock()]
        self.animations['jump'] = [ MagicMock()]
    Player.load_animations =mock_load_animations
    mock_load_animations.side_effect = mock_load_animations
    player = Player(100, 100, 50, 50, "path/to/sprite.png")

    assert player.hp == 200
    assert player.max_jumps == 2
    assert len(player.weapons) == 4  # Проверяем, что 4 оружия инициализированы
    assert player.current_weapon == 0

def test_player_jump(mock_pygame):
    player = Player(100, 100, 50, 50)
    player.jump()  # Выполняем прыжок

    assert player.velocity.y == player.jump_force
    assert player.jump_count == 1
    assert not player.is_landed

def test_player_double_jump(mock_pygame):
    player = Player(100, 100, 50, 50)
    player.jump()
    player.jump()  # Выполняем второй прыжок

    assert player.jump_count == 2
    assert player.velocity.y == player.jump_force

def test_player_shoot(mock_pygame):
    player = Player(100, 100, 50, 50)
    player.coldown = 0
    bullets = player.shoot()  # Пытаемся стрелять

    assert player.coldown == 30
    assert len(bullets) == 1

def test_player_add_buff(mock_pygame):
    player = Player(100, 100, 50, 50)
    buff = Buff(100, 100, 10, 10, 50)
    player.add_buff(buff)

    assert len(player.buffs) == 1  # Проверяем, что буст добавлен
    assert buff.alive == False  # Проверяем, что буст не активен

def test_player_act_with_bullet(mock_pygame):
    player = Player(100, 100, 50, 50)
    bullet = Bullet(90, 90, 10, 10, 20)  # Создаем пулю
    bullet.team = -1  # Устанавливаем команду пули

    player.act(bullet)  # Игрок взаимодействует с пулей

    assert player.hp == 180  # Проверяем, что здоровье уменьшилось на урон пули

def test_player_act_with_buff(mock_pygame):
    player = Player(100, 100, 50, 50)
    buff = Buff(100, 100, 10, 10, 50)  # Создаем буст
    buff.apply = MagicMock()  # Замена метода apply

    player.act(buff)  # Игрок взаимодействует с бустом

    assert len(player.buffs) == 1  # Проверяем, что буст добавлен
    buff.apply.assert_called_once_with(player)  # Проверяем, что метод apply был вызван

def test_act_with_player(mock_pygame):
    player1 = Player(100, 100, 50, 50)
    player2 = Player(110, 110, 50, 50)

    player1.act(player2)  # Игрок взаимодействует с бустом
    player2.act(player1)  # Игрок взаимодействует с бустом

    assert player1.velocity.dot(player2.velocity) < 0 # Проверяем, что буст добавлен
    assert player1.velocity.length() > 0
    assert player2.velocity.length() > 0

def test_player_set_direction(mock_pygame):
    player = Player(100, 100, 50, 50)
    player.set_direction()  # Устанавливаем направление

    assert player.direction.length() > 0  # Проверяем, что направление установлено

def test_player_update(mock_pygame):
    player = Player(100, 100, 50, 50)
    player.update()  # Обновляем игрока

    assert player.coldown == 29  # Проверяем, что кулдаун уменьшился
    assert player.hp == 200  # Проверяем, что здоровье игрока не изменилось

def test_player_die(mock_pygame):
    player = Player(100, 100, 50, 50)
    bullet = Bullet(100, 100, 50, 50, 1000)
    bullet.team = 123123412
    player.act(bullet)
    assert player.hp < 0
    player.update()
    assert player.alive == False
    assert bullet.alive == False

def test_player_die_by_blowing(mock_pygame):
    player = Player(100, 100, 50, 50)
    bullet = BlowingBullet(130, 130, 1, 1, 1000)
    bullet.team = 123123412
    bullet.blowing = True
    player.act(bullet)
    assert player.hp < 0
    player.update()
    assert player.alive == False

def test_player_draw(mock_pygame):
    player = Player(100, 100, 50, 50)
    screen = MagicMock()
    center = Vec2(100, 100)

    player.draw(screen, center)  # Проверяем, что метод draw не вызывает ошибок
    screen.blit.assert_called_once()
