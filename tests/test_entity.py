from objects.map.map import Map
from physics.vec2 import Vec2
from objects.entities.entity import Entity


def test_init(mocker):
    mock_load_images = mocker.patch("objects.entities.entity.Entity.load_images")
    entity = Entity(100, 100, 200, 200, sprite_path="path")
    assert entity.velocity == Vec2(0, 0)
    assert entity.is_landed == False
    assert entity.sprite_path == "path"
    assert entity.direction == Vec2(1, 0)
    assert not entity.is_dead
    assert entity.alive
    assert entity.animations == dict()
    assert entity.frames == 0
    assert entity.team == 0
    assert entity.image is None
    mock_load_images.assert_called_once()


def test_apply_forces():
    entity = Entity(100, 100, 200, 200)
    entity.apply_forces()
    assert entity.velocity == Entity.GRAVITY
    entity = Entity(100, 100, 200, 200)
    entity.is_landed = True
    entity.apply_forces()
    assert entity.velocity == Vec2(0, 0)


def test_update(mocker):
    mocker.patch("objects.entities.entity.Entity.animate")
    entity = Entity(100, 100, 200, 200)
    entity.velocity = Vec2(10, 10)
    entity.update()
    assert entity.position == Vec2(110, 110)

    entity = Entity(100, 100, 200, 200)
    entity.velocity = Vec2(100, 100)
    entity.update()

    assert entity.velocity.length() <= 26
    assert (Vec2(100, 100) - entity.position).length() <= 26


def test_move():
    entity = Entity(100, 100, 200, 200)
    entity.move(100, 100)
    assert entity.position == Vec2(200, 200)


def test_load_images(mocker):
    mock_load_image = mocker.patch("pygame.image.load", return_value="image")
    mock_transform = mocker.patch(
        "pygame.transform.scale", return_value="transformed_image"
    )
    entity = Entity(100, 100, 200, 200)
    entity.image = None
    entity.load_images()
    assert entity.image is None
    entity.sprite_path = "path"
    entity.image = None
    entity.load_images()
    mock_load_image.assert_called_once_with("path")
    mock_transform.assert_called_once_with("image", (200, 200))
    assert entity.image == "transformed_image"


def test_collide_right(mocker):
    mocker.patch("pygame.image.load")
    mocker.patch("pygame.transform.scale")
    mocker.patch("objects.entities.entity.Entity.animate")
    map = Map()
    map.load_from_list(["0;0", "125; 125; 50; 50;"], w_sprites=False)
    entity = Entity(75, 125, 49, 49)
    entity.velocity = Vec2(10, 0)
    entity.collide(map)
    entity.update()
    assert not entity.intersects(list(map.blocks.values())[0])
    assert entity.bottom_right.x < 100
    assert abs(entity.velocity.x) < 1e-5


def test_collide_left(mocker):
    mocker.patch("pygame.image.load")
    mocker.patch("pygame.transform.scale")
    map = Map()
    map.load_from_list(["0;0", "125; 125; 50; 50;"], w_sprites=False)
    entity = Entity(175, 125, 49, 49)
    entity.velocity = Vec2(-10, 0)
    entity.collide(map)
    assert not entity.intersects(list(map.blocks.values())[0])
    assert entity.top_left.x > 150
    assert abs(entity.velocity.x) < 1e-5


def test_collide_top(mocker):
    mocker.patch("pygame.image.load")
    mocker.patch("pygame.transform.scale")
    map = Map()
    map.load_from_list(["0;0", "125; 125; 50; 50;"], w_sprites=False)
    entity = Entity(100, 175, 49, 49)
    entity.velocity = Vec2(0, -10)
    entity.collide(map)
    assert not entity.intersects(list(map.blocks.values())[0])
    assert entity.bottom_right.y > 174
    assert abs(entity.velocity.y) < 1e-9


def test_collide_bottom(mocker):
    mocker.patch("pygame.image.load")
    mocker.patch("pygame.transform.scale")
    map = Map()
    map.load_from_list(["0;0", "125; 125; 50; 50;"], w_sprites=False)
    entity = Entity(100, 75, 49, 49)
    entity.velocity = Vec2(0, 10)
    entity.collide(map)
    assert not entity.intersects(list(map.blocks.values())[0])
    assert entity.bottom_right.y < 100
    assert abs(entity.velocity.y) < 1e-9


def test_draw(mocker):
    mocker.patch("pygame.image.load", return_value="image")
    mocker.patch("pygame.transform.scale", return_value="image")
    screen = mocker.Mock()

    entity = Entity(100, 100, 50, 50, sprite_path="path")
    center = Vec2(0, 0)
    entity.draw(screen, center)
    screen.blit.assert_called_once_with("image", (475, 375, 50, 50))
