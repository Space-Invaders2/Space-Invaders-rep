from unittest.mock import patch

from collision.collision_layers import ObjectLayer
from entities.alien import AlienShooter, GenericAlien


def test_generic_alien_init():
    gen_alien = GenericAlien()
    assert gen_alien.score_points == gen_alien.config.points.extra
    assert gen_alien.speed == gen_alien.config.speeds.alien
    assert gen_alien.direction == [0, 1]


def test_generic_alien_collision_layers_init():
    gen_alien = GenericAlien()
    coll_layers = gen_alien.collision_layers
    assert coll_layers.object_name == "Alien"
    assert coll_layers.object_layer == ObjectLayer.ALIEN
    assert ObjectLayer.BLOCK in coll_layers
    assert ObjectLayer.PLAYER_LASER in coll_layers


def test_change_momentum():
    alien = GenericAlien()
    test_momentum = [2, 3]
    alien.change_momentum(test_momentum)
    assert alien.momentum == test_momentum


def test_action():
    gen_alien = GenericAlien()
    with patch.object(gen_alien, "move") as mock_move:
        gen_alien.action()
        mock_move.assert_called_with("simple_move")


def test_alien_shooter_init():
    alien_shooter = AlienShooter()
    assert alien_shooter.momentum == [1, 0]
