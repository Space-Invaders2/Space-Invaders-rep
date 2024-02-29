import itertools
from unittest.mock import MagicMock, Mock, call, patch

import collision.collision_strategy as cs
import entities.alien as al
import game_objects.powerup as up
import numpy as np
import pygame
import pytest
from collision.collision_layers import CollisionLayers, ObjectLayer
from entities.player import Player
from game_objects.game_object import GameObject
from game_objects.laser import Laser
from game_objects.obstacle import Block
from pygame import sprite


class MockCollisionLayer:
    def __init__(self, object_name: str) -> None:
        self.object_name = object_name


@pytest.fixture
def mock_player():
    player_mock = Mock(Player)
    player_mock.sprite = Mock(pygame.sprite.GroupSingle)
    return player_mock


@pytest.fixture
def player_sprite():
    return Player(pos=(0, 0), speed=0)


@pytest.fixture
def red_alien_sprite():
    return al.AlienRed(x=0, y=0)


@pytest.fixture
def green_alien_sprite():
    return al.AlienGreen(x=0, y=0)


@pytest.fixture
def yellow_alien_sprite():
    return al.AlienYellow(x=0, y=0)


@pytest.fixture
def enemy_laser_sprite():
    coll_layer = CollisionLayers(
        object_layer=ObjectLayer.ALIEN_LASER, collidable_layers=[ObjectLayer.PLAYER]
    )
    return Laser(pos=(0, 0), momentum=[0, 0], collision_layers=coll_layer)


@pytest.fixture
def player_laser_sprite():
    coll_layer = CollisionLayers(
        object_layer=ObjectLayer.PLAYER_LASER, collidable_layers=[ObjectLayer.ALIEN]
    )
    return Laser(pos=(0, 0), momentum=[0, 0], collision_layers=coll_layer)


@pytest.fixture
def block_sprite():
    return Block(size=6, color=[0, 0, 0], pos=[0, 0])


@pytest.fixture
def life_powerup_sprite():
    return up.LifePowerup(pos=[0, 0])


@pytest.fixture
def immunity_powerup_sprite():
    return up.ImmunityPowerup(pos=[0, 0])


@pytest.fixture
def beam_powerup_sprite():
    return up.BeamPowerup(pos=[0, 0])


@pytest.fixture
def delayed_powerup_sprite():
    return up.DelayedPowerup(pos=[0, 0])


@pytest.fixture
def multi_powerup_sprite():
    return up.MultiPowerup(pos=[0, 0])


@pytest.fixture
def obj():
    mock_obj = Mock()
    mock_obj.rect = MagicMock()
    return mock_obj


@pytest.mark.parametrize(
    "alien_sprite",
    [
        "red_alien_sprite",
        "green_alien_sprite",
        "yellow_alien_sprite",
    ],
)
def test_player_alien_collision(request, player_sprite, alien_sprite):
    alien_group = sprite.Group(request.getfixturevalue(alien_sprite))
    player_group = sprite.GroupSingle(player_sprite)

    alien_group_initial_size = len(alien_group)
    player_initial_lives = player_sprite.lives

    collision_handler = cs.PlayerAlienCollision()
    collision_handler.handle_collision(player_group, alien_group)

    alien_group_final_size = len(alien_group)
    player_final_lives = player_sprite.lives

    assert (alien_group_final_size < alien_group_initial_size) == True
    assert (player_final_lives < player_initial_lives) == True


def test_player_laser_collision(player_sprite, enemy_laser_sprite):
    laser_group = sprite.Group(enemy_laser_sprite)
    player_group = sprite.GroupSingle(player_sprite)

    player_initial_lives = player_sprite.lives
    laser_group_initial_size = len(laser_group)

    collision_handler = cs.PlayerLaserCollision()
    collision_handler.handle_collision(player_group, laser_group)

    player_final_lives = player_sprite.lives
    laser_group_final_size = len(laser_group)

    assert player_final_lives == player_initial_lives - 1
    assert (laser_group_final_size < laser_group_initial_size) == True


@pytest.mark.parametrize(
    "alien_sprite",
    [
        "red_alien_sprite",
        "green_alien_sprite",
        "yellow_alien_sprite",
    ],
)
def test_alien_laser_collision(request, alien_sprite, player_laser_sprite):
    alien_group = sprite.Group(request.getfixturevalue(alien_sprite))
    laser_group = sprite.Group(player_laser_sprite)

    alien_group_initial_size = len(alien_group)
    laser_group_initial_size = len(laser_group)

    collision_handler = cs.AlienLaserCollision()
    collision_handler.handle_collision(alien_group, laser_group)

    alien_group_final_size = len(alien_group)
    laser_group_final_size = len(laser_group)

    assert (alien_group_final_size < alien_group_initial_size) == True
    assert (laser_group_final_size < laser_group_initial_size) == True


@pytest.mark.parametrize(
    "laser_sprite",
    [
        "player_laser_sprite",
        "enemy_laser_sprite",
    ],
)
def test_block_laser_collision(request, block_sprite, laser_sprite):
    laser_group = sprite.Group(request.getfixturevalue(laser_sprite))
    block_group = sprite.Group(block_sprite)

    laser_group_initial_size = len(laser_group)
    block_group_initial_size = len(block_group)

    collision_handler = cs.BlockLaserCollision()
    collision_handler.handle_collision(block_group, laser_group)

    laser_group_final_size = len(laser_group)
    block_group_final_size = len(block_group)

    assert (block_group_final_size < block_group_initial_size) == True
    assert (laser_group_final_size < laser_group_initial_size) == True


@pytest.mark.parametrize(
    "alien_sprite",
    [
        "red_alien_sprite",
        "green_alien_sprite",
        "yellow_alien_sprite",
    ],
)
def test_block_alien_collision(request, block_sprite, alien_sprite):
    alien_group = sprite.Group(request.getfixturevalue(alien_sprite))
    block_group = sprite.Group(block_sprite)

    alien_group_initial_size = len(alien_group)
    block_group_initial_size = len(block_group)

    collision_handler = cs.BlockAlienCollision()
    collision_handler.handle_collision(block_group, alien_group)

    alien_group_final_size = len(alien_group)
    block_group_final_size = len(block_group)

    assert (block_group_final_size < block_group_initial_size) == True
    assert (alien_group_final_size < alien_group_initial_size) == True


@pytest.mark.parametrize(
    "powerup_sprite",
    [
        "life_powerup_sprite",
        "immunity_powerup_sprite",
        "beam_powerup_sprite",
        "delayed_powerup_sprite",
        "multi_powerup_sprite",
    ],
)
@patch("collision.collision_strategy.GameGroups")
def test_powerup_laser_collision(
    mock_game_groups, request, powerup_sprite, player_laser_sprite
):
    mock_player_sprite = Mock(spec=pygame.sprite.Sprite)
    mock_game_groups.return_value.player.sprite = mock_player_sprite

    powerup_group = sprite.Group(request.getfixturevalue(powerup_sprite))
    laser_group = sprite.Group(player_laser_sprite)

    powerup_group_initial_size = len(powerup_group)
    laser_group_initial_size = len(laser_group)

    for powerup in powerup_group:
        powerup.upgrade = Mock()

    collision_handler = cs.PowerupLaserCollision()
    collision_handler.handle_collision(powerup_group, laser_group)

    powerup_group_final_size = len(powerup_group)
    laser_group_final_size = len(laser_group)

    assert (laser_group_final_size < laser_group_initial_size) == True
    assert (powerup_group_final_size < powerup_group_initial_size) == True

    for powerup in powerup_group:
        powerup.upgrade.assert_called_with(mock_player_sprite)


@pytest.mark.parametrize(
    "right,left,bottom,top,expected",
    [
        (700, 600, 500, 400, None),  # No Collision
        (100, 200, 300, 400, None),  # No Collision
        (799, 400, 400, 400, None),  # Almost Right Collision
        (400, 1, 400, 400, None),  # Almost Left Collision
        (400, 400, 599, 400, None),  # Almost Bottom Collision
        (400, 400, 400, 1, None),  # Almost Top Collision
        (800, 400, 400, 400, [-1, 1]),  # Exact Right Collision
        (400, 0, 400, 400, [-1, 1]),  # Exact Left Collision
        (400, 400, 600, 400, [1, -1]),  # Exact Bottom Collision
        (400, 400, 400, 0, [1, -1]),  # Exact Top Collision
        (801, 400, 400, 400, [-1, 1]),  # One Diff Right Collision
        (400, -1, 400, 400, [-1, 1]),  # One Diff Left Collision
        (400, 400, 601, 400, [1, -1]),  # One Diff Bottom Collision
        (400, 400, 400, -1, [1, -1]),  # One Diff Top Collision
        (973, 400, 400, 400, [-1, 1]),  # Any Right Collision
        (400, -73, 400, 400, [-1, 1]),  # Any Left Collision
        (400, 400, 766, 400, [1, -1]),  # Any Bottom Collision
        (400, 400, 400, -100, [1, -1]),  # Any Top Collision
    ],
)
@patch("collision.collision_strategy.GameAttributes")
def test_boundary_check_collision(
    mock_game_attributes, obj, right, left, bottom, top, expected
):
    obj.rect.right = right
    obj.rect.left = left
    obj.rect.bottom = bottom
    obj.rect.top = top

    mock_game_attributes.return_value.screen_width = 800
    mock_game_attributes.return_value.screen_height = 600

    boundary_collision = cs.BoundaryCollision()
    direction = boundary_collision.check_collision(obj)
    assert direction == expected


def test_boundary_collision_with_game_object():
    mock_game_object = Mock(GameObject)
    boundary_collision = cs.BoundaryCollision()

    with patch.object(boundary_collision, "check_collision") as mock_check_collision:
        boundary_collision.handle_collision(mock_game_object)
        mock_check_collision.assert_called_once_with(mock_game_object)


def test_boundary_collision_with_game_object():
    mock_game_object = Mock(GameObject)
    boundary_collision = cs.BoundaryCollision()

    with patch.object(boundary_collision, "check_collision") as mock_check_collision:
        boundary_collision.handle_collision(mock_game_object)
        mock_check_collision.assert_called_once_with(mock_game_object)


def test_boundary_collision_with_sprites():
    mock_sprites = [Mock(pygame.sprite.Sprite) for _ in range(5)]
    boundary_collision = cs.BoundaryCollision()

    mock_group = Mock(pygame.sprite.Group)
    mock_group.sprites.return_value = mock_sprites

    with patch.object(boundary_collision, "check_collision") as mock_check_collision:
        boundary_collision.handle_collision(mock_group)

        mock_check_collision.assert_called_once()


def test_boundary_collision_with_none():
    mock_obj = Mock(pygame.sprite.Group)
    mock_obj.sprites.return_value = []
    boundary_collision = cs.BoundaryCollision()

    with patch.object(boundary_collision, "check_collision") as mock_check_collision:
        mock_check_collision.return_value = None
        empty_collision = boundary_collision.handle_collision(mock_obj)
        mock_check_collision.assert_not_called()

    assert empty_collision is None


@pytest.mark.parametrize("coll_layer_name", ["player", "object", "duck", "test"])
def test_get_sprite_class_with_group_single(coll_layer_name):
    mock_sprite = Mock(pygame.sprite.Sprite)
    mock_sprite.collision_layers = MockCollisionLayer(coll_layer_name)

    group_single = pygame.sprite.GroupSingle(sprite=mock_sprite)
    ch = cs.CollisionHandler(groups=[group_single])
    obj_class = ch.get_sprite_class(group_single)

    assert obj_class == coll_layer_name


@pytest.mark.parametrize("coll_layer_name", ["blocks", "laser", "aliens", "ducks"])
def test_get_sprite_class_with_group(coll_layer_name):
    mock_sprites = [Mock(pygame.sprite.Sprite) for _ in range(5)]
    for mock_sprite in mock_sprites:
        mock_sprite.collision_layers = MockCollisionLayer(coll_layer_name)

    group = pygame.sprite.Group(mock_sprites)
    ch = cs.CollisionHandler(groups=[group])
    obj_class = ch.get_sprite_class(group)

    assert obj_class == coll_layer_name


@pytest.mark.parametrize("group_split", [2, 3, 4, 5, 10])
def test_handle_collisions(group_split):
    mock_sprites = [Mock(pygame.sprite.Sprite) for _ in range(20)]
    group_splits = np.array_split(mock_sprites, group_split)
    mock_groups = [group.tolist() for group in group_splits]
    ch = cs.CollisionHandler(mock_groups)

    with patch.object(ch, "get_sprite_class") as mock_get_sprite_class:
        with patch.object(ch, "process_collision") as mock_process_collision:
            ch.handle_collisions()

            expected_combinations = list(itertools.combinations(mock_groups, 2))
            for group1, group2 in expected_combinations:
                class1 = mock_get_sprite_class(group1)
                class2 = mock_get_sprite_class(group2)
                mock_process_collision.assert_any_call(
                    (class1, class2), (group1, group2), symmetric=True
                )


def test_process_forward_collision():
    mock_class1 = "class1"
    mock_class2 = "class2"

    mock_group1 = MagicMock()
    mock_group2 = MagicMock()
    mock_groups = [mock_group1, mock_group2]

    class_pair = (mock_class1, mock_class2)
    group_pair = (mock_group1, mock_group2)

    mock_strategy = MagicMock()
    mock_strategy.handle_collision = MagicMock()

    ch = cs.CollisionHandler(mock_groups)
    ch.class_collision_dict = {class_pair: mock_strategy}

    ch.process_collision(class_pair, group_pair, symmetric=False)
    mock_strategy.handle_collision.assert_called_once_with(mock_group1, mock_group2)


def test_process_reverse_collision():
    mock_class1 = "class1"
    mock_class2 = "class2"
    mock_group1 = MagicMock()
    mock_group2 = MagicMock()

    class_pair = (mock_class1, mock_class2)
    group_pair = (mock_group1, mock_group2)

    reverse_class_pair = class_pair[::-1]
    reverse_group_pair = group_pair[::-1]

    mock_strategy = MagicMock()
    mock_strategy.handle_collision = MagicMock()

    ch = cs.CollisionHandler([mock_group1, mock_group2])
    ch.class_collision_dict = {reverse_class_pair: mock_strategy}

    ch.process_collision(class_pair, group_pair, symmetric=False)
    mock_strategy.handle_collision.assert_not_called()

    ch.process_collision(class_pair, group_pair, symmetric=True)
    mock_strategy.handle_collision.assert_called_once_with(*reverse_group_pair)
