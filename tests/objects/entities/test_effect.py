import pytest
import pygame as pg
from unittest.mock import Mock, patch, MagicMock
from objects.entities.effect import Effect, Particle
from objects.entities.player import Player
from physics.vec2 import Vec2
import other.functions



@pytest.fixture
def screen():
    return pg.Surface((800, 600))

@pytest.fixture
@patch('other.functions.load_animation')
@patch('pygame.Surface')
@patch('pygame.image.load')
@patch('pygame.transform.scale')
def effect(mock_load, _, __, ___):
    # mock_load.return_value = [MagicMock(), MagicMock(), MagicMock()]
    return Effect(x=100, y=100, width=50, height=50, lifetime=120, animation_path="path")

@patch('other.functions.load_animation')
@patch('pygame.Surface')
@patch('pygame.image.load')
@patch('pygame.transform.scale')
def test_effect_initialization(mock_scale, mock_load, mock_surface, mock_load_animation):
    mocks = [MagicMock(), MagicMock(), MagicMock()]
    mock_load_animation.return_value = mocks
    mock_load.return_value = MagicMock()
    effect =    Effect(x=100, y=100, width=50, height=50, lifetime=120, animation_path="path")

    assert effect.position.x == 100
    assert effect.position.y == 100
    assert effect.width == 50
    assert effect.height == 50
    assert effect.lifetime == 120
    assert effect.alive is True
    assert mock_scale.call_count == 1

def test_effect_update(effect):
    effect.velocity = Vec2(5, 0)
    effect.update()
    assert effect.position.x == 105
    assert effect.lifetime == 119


def test_effect_lifetime(effect):
    effect.lifetime = 2

    effect.update()
    assert effect.alive is True
    effect.update()
    assert effect.alive is False

def test_effect_animate(effect):
    effect.animation = [pg.Surface((50, 50)), pg.Surface((50, 50))]
    effect.frames = 0.8
    effect.animate()
    assert effect.frames == 1.0
    assert effect.image.get_size() == (50, 50)

def test_particle_initialization():
    particle = Particle(x=100, y=100, width=50, height=50, lifetime=60)
    assert particle.position.x == 100
    assert particle.position.y == 100
    assert particle.width == 50
    assert particle.height == 50
    assert particle.lifetime == 60
    assert particle.alive is True

def test_particle_update():
    particle = Particle(x=100, y=100, width=50, height=50, lifetime=60)
    particle.velocity = Vec2(5, 0)
    particle.update()
    assert particle.position.x == 105
    assert particle.width == 45
    assert particle.height == 45
    assert particle.lifetime == 59

def test_particle_lifetime():
    particle = Particle(x=100, y=100, width=50, height=50, lifetime=2)
    particle.update()
    assert particle.alive is True
    particle.update()
    assert particle.alive is False


    particle = Particle(x=100, y=100, width=10, height=10, lifetime=999999)
    for i in range(50):
        particle.update()
    assert particle.alive is False

def test_particle_scale():
    particle = Particle(x=100, y=100, width=50, height=50, lifetime=60)
    particle.update()
    assert particle.image.get_size() == (45, 45)
    particle.update()
    assert particle.image.get_size() == (40, 40)
