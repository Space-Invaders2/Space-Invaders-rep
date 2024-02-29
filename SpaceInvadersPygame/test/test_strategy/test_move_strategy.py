import sys

import pytest

sys.path.append("code")  # noqa

from entities import entity as ent
from game_attributes import GameAttributes
from pygame import sprite as sp
from strategy import move_strategy as mv


@pytest.fixture(scope="class")
def custom_config():
    entity = ent.Entity()
    momentum = [2, 0]
    entity.momentum = momentum
    momentum2 = [3, 0]
    entity2 = ent.Entity()
    entity2.momentum = momentum2
    sprit_group = sp.Group()
    sprit_group.add(entity)
    sprit_group.add(entity2)
    single_group = sp.GroupSingle()
    single_group.add(entity)

    return {
        "entity": entity,
        "entity2": entity2,
        "momentum": momentum,
        "momentum2": momentum2,
        "group": sprit_group,
        "single_group": single_group,
    }


def test_pixel_movement(custom_config):
    entity: ent.Entity
    entity = custom_config["entity"]
    momentum = custom_config["momentum"]
    mv.MoveStrategy.pixel_movement(entity, momentum)
    assert entity.pos[0] == momentum[0]
    assert entity.pos[1] == momentum[1]


def test_update_position_single(custom_config):
    group: sp.GroupSingle
    group = custom_config["single_group"]
    momentum = custom_config["momentum"]
    mv.MoveStrategy.update_position(group.sprite, momentum)
    sprite = group.sprite
    assert sprite.pos[0] == momentum[0]
    assert sprite.pos[1] == momentum[1]


def test_update_position_group(custom_config):
    group = custom_config["group"]
    momentum = custom_config["momentum"]
    mv.MoveStrategy.update_position(group, momentum)
    for sprite in group:
        assert sprite.pos[0] == momentum[0]
        assert sprite.pos[1] == momentum[1]


def test_advance(custom_config):
    config = GameAttributes().config
    entity = custom_config["entity"]
    mv.Advance.handle_move(entity)
    assert entity.pos[0] == config.get_option_dev("alien", "advance")[0]
    assert entity.pos[1] == config.get_option_dev("alien", "advance")[1]


def test_simple_move(custom_config):
    config = GameAttributes().config
    entity = custom_config["entity"]
    momentum = custom_config["momentum"]
    mv.SimpleMove.handle_move(entity, momentum)
    assert entity.pos[0] == momentum[0]
    assert entity.pos[1] == momentum[1]


def test_no_move(custom_config):
    entity = custom_config["entity"]
    momentum = custom_config["momentum"]
    mv.NoMove.handle_move(entity, momentum)
    assert entity.pos[0] == 0
    assert entity.pos[1] == 0


def test_move_handler(custom_config):
    single_group = custom_config["single_group"]
    group = custom_config["group"]
    groups = [single_group, group]
    mv_handler = mv.MoveHandler(groups)
    mv_handler.handle_moves()
