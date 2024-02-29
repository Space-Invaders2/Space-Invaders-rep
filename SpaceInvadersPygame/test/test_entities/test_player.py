import pytest
from collision.collision_layers import ObjectLayer
from entities.player import Player


@pytest.fixture(scope="session")
def custom_config():
    return {
        "POS": (50, 50),
        "SPEED": 500,
        "MAX_RIGHT_CONSTRAINT": 100,
        "MIN_LEFT_CONSTRAINT": 0,
    }


@pytest.fixture
def player_entity(custom_config):
    pos = custom_config["POS"]
    speed = custom_config["SPEED"]
    player = Player(pos, speed)
    return player


def test_player_init(player_entity, custom_config):
    pos = custom_config["POS"]
    assert player_entity.pos[0] == pos[0]
    assert player_entity.pos[1] < pos[1]
    assert player_entity.speed == custom_config["SPEED"]


def test_player_collision_layers_init(player_entity):
    coll_layers = player_entity.collision_layers
    assert coll_layers.object_name == "Player"
    assert coll_layers.object_layer == ObjectLayer.PLAYER
    assert ObjectLayer.ALIEN_LASER in coll_layers
    assert ObjectLayer.ALIEN in coll_layers


@pytest.mark.parametrize("pos", [-1000, -500, 0, 50, 99, 100, 101, 1000])
def test_player_constraint_right_boundary(player_entity, custom_config, pos):
    player_entity.max_x_constraint = custom_config["MAX_RIGHT_CONSTRAINT"]
    player_entity.pos[0] = pos
    player_entity.constraint()
    assert player_entity.pos[0] <= player_entity.max_x_constraint


@pytest.mark.parametrize("pos", [-1000, -500, -100, -10, -1, 0, 15, 75, 100, 500, 1000])
def test_player_constraint_left_boundary(player_entity, custom_config, pos):
    min_left_constraint = custom_config["MIN_LEFT_CONSTRAINT"]
    player_entity.pos[0] = pos
    player_entity.constraint()
    assert player_entity.pos[0] >= min_left_constraint
