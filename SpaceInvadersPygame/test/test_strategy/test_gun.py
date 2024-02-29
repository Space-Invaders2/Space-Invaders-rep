import sys

import pytest

sys.path.append("code")  # noqa

from collision.collision_layers import CollisionLayers
from entities.entity import Entity
from strategy.gun import *


@pytest.fixture(scope="class")
def custom_config():
    layer = CollisionLayers("entity")
    entity = Entity()
    laser_cooldown = 777
    gun = DefaultGun(entity, laser_cooldown, layer)
    beam = BeamGun(gun)
    decorator = GunDecorator(gun)
    return {
        "entity": entity,
        "layer": layer,
        "laser_cooldown": laser_cooldown,
        "gun": gun,
        "decorator": decorator,
        "beam": beam,
    }


def test_gun_fineshed_recharging(custom_config):
    gun: Gun
    gun = custom_config["gun"]
    gun.set_laser_cooldown(0)
    assert gun.finished_recharging()


def test_laser_cooldown(custom_config):
    gun: Gun
    gun = custom_config["gun"]
    gun.set_laser_cooldown(3)
    assert gun.laser_cooldown == 3


def test_reduce_laser_cooldown(custom_config):
    gun: Gun
    gun = custom_config["gun"]
    gun.set_laser_cooldown(3)
    gun.reduce_laser_cooldown(0.5)
    assert gun.laser_cooldown != 3


def test_set_laser_speed(custom_config):
    gun: Gun
    gun = custom_config["gun"]
    gun.set_laser_speed(3)
    assert gun.laser_speed == 3


def test_set_laser_direction(custom_config):
    gun: Gun
    gun = custom_config["gun"]
    gun.set_laser_direction([3, 3])
    assert gun.laser_direction == [3, 3]


def test_default_gun(custom_config):
    gun: Gun
    entity = custom_config["entity"]
    layer = custom_config["layer"]
    gun = DefaultGun(entity, 0, layer)
    assert isinstance(gun, DefaultGun)


def test_directio_queue():
    ds = Gun.direction_queue([3])
    assert not isinstance(ds[0][0], list)
    ds = Gun.direction_queue([[3]])
    assert not isinstance(ds[0][0], list)


def test_defaultgun_shoot(custom_config):
    gun: Gun
    gun = custom_config["gun"]
    gun.set_laser_cooldown(0)
    assert gun.finished_recharging()
    gun.shoot([1, 1])
    assert gun.finished_recharging()
    gun.shoot([1, 1])
    assert len(gun.lasers) == 2


def test_set_color(custom_config):
    gun = custom_config["gun"]
    gun.set_color("black")
    assert gun.laser_color == "black"


def test_gun_decorator(custom_config):
    gun = custom_config["gun"]
    decorator = GunDecorator(gun)
    assert decorator != None


def test_gun_decorator(custom_config):
    gun = custom_config["gun"]
    decorator = GunDecorator(gun)
    assert decorator.gun == gun


def test_decorator_shoot(custom_config):
    decorator: GunDecorator
    decorator = custom_config["decorator"]
    direction: Direction
    direction = [1, 1]
    decorator.set_laser_cooldown(0)
    decorator.shoot([direction])
    assert len(decorator.gun.lasers) == 1


def test_reduce_laser_cooldown_decorator(custom_config):
    decorator: GunDecorator
    decorator = custom_config["decorator"]
    cooldown = custom_config["laser_cooldown"]
    decorator.reduce_laser_cooldown(0.5)
    assert decorator.gun.laser_cooldown != cooldown


def test_activate_decorator(custom_config):
    decorator: GunDecorator = custom_config["decorator"]
    decorator.activate()
    assert decorator.is_active()


def test_beam_gun(custom_config):
    cool_down = custom_config["laser_cooldown"]
    beam = custom_config["beam"]
    assert beam.gun.laser_cooldown == cool_down - 100
