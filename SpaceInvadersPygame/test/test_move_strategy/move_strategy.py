import sys

import pytest

sys.path.append("code")  # noqa

from entities import entity as ent
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
        "sprit_group": sprit_group,
        "single_group": single_group,
    }


def test_move_strategy_interface(custom_config):
    entity: ent.Entity
    entity = custom_config["entity"]
    momentum = custom_config["momentum"]
    mv.MoveStrategy.pixel_movement(entity, momentum)
    assert entity.pos[0] == momentum[0]
    assert entity.pos[1] == momentum[1]
