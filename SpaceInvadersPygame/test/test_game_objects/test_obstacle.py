from unittest.mock import patch

import pytest
from collision.collision_layers import ObjectLayer
from game_objects.obstacle import Block

parameters = [
    (1, (255, 255, 255), [100, 150]),
    (40, (255, 0, 0), [100, 150]),
    (50, (0, 0, 255), [100, 150]),
    (60, (0, 255, 0), [200, 250]),
    (1000, (0, 255, 0), [200, 250]),
    (50, (0, 255, 0), [500, 500]),
]


@pytest.mark.parametrize("size, color, pos", parameters)
def test_block_init(size, color, pos):
    x, y = pos
    block = Block(size, color, pos)

    assert block.pos == [x, y]
    assert block.rect.topleft == (x, y)


def test_block_collision_layers_init():
    block_object = Block(50, (0, 0, 0), [0, 0])
    coll_layers = block_object.collision_layers
    assert coll_layers.object_name == "Block"
    assert coll_layers.object_layer == ObjectLayer.BLOCK
    assert ObjectLayer.ALIEN in coll_layers
    assert ObjectLayer.PLAYER_LASER in coll_layers
    assert ObjectLayer.ALIEN_LASER in coll_layers
