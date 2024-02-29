from unittest.mock import patch

import pygame
import pytest
from collision.collision_layers import CollisionLayers
from game_objects.laser import Laser


@pytest.fixture(scope="session")
def custom_config():
    return {
        "POS": (10, 0),
        "MOMENTUM": 5,
        "HEIGHT_CONSTRAINT": 500,
        "DESTROY_CONDITION": 50,
    }


@pytest.fixture
def laser_object(custom_config):
    pos = custom_config["POS"]
    momentum = custom_config["MOMENTUM"]
    collision_layers = CollisionLayers()
    laser = Laser(pos, momentum, collision_layers)
    laser.height_y_constraint = custom_config["HEIGHT_CONSTRAINT"]
    laser.destroy_condition = custom_config["DESTROY_CONDITION"]
    return laser


def test_laser_init(laser_object, custom_config):
    assert laser_object.pos == custom_config["POS"]
    assert laser_object.momentum == custom_config["MOMENTUM"]
    assert isinstance(laser_object.laser_sound, pygame.mixer.Sound)


@pytest.mark.parametrize("rect_y", [-550, -500, 550, 600])
def test_destroy_out_of_bounds(laser_object, rect_y):
    laser_object.rect.y = rect_y
    with patch.object(laser_object, "kill") as mock_kill:
        laser_object.destroy()
        mock_kill.assert_called_once()


@pytest.mark.parametrize("rect_y", [499, -10, 0, 10, 549])
def test_destroy_in_bounds(laser_object, rect_y):
    laser_object.rect.y = rect_y
    with patch.object(laser_object, "kill") as mock_kill:
        laser_object.destroy()
        mock_kill.assert_not_called()


def test_action_calls_move(laser_object):
    with patch.object(laser_object, "move") as mock_move:
        laser_object.action()
        mock_move.assert_called_once_with("simple_move")
