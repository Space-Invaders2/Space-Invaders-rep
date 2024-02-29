import random
from abc import ABC, abstractmethod

import numpy as np
import pygame
from collision.collision_layers import CollisionLayers
from game_attributes import GameAttributes
from game_objects.laser import Laser
from game_types import Direction


class Gun(ABC):
    def __init__(self, laser_cooldown: int) -> None:
        self.config = GameAttributes().config
        self.lasers = pygame.sprite.Group()

        self.laser_cooldown = laser_cooldown
        self.config = GameAttributes().config
        self.last_shot_time = 0
        self.laser_direction = None
        self.laser_speed = self.config.get_option_dev("gun1", "laser_speed")

    @abstractmethod
    def shoot(self, directions: Direction):
        pass

    def finished_recharging(self) -> bool:
        time_since_last_shot = pygame.time.get_ticks() - self.last_shot_time
        return time_since_last_shot >= self.laser_cooldown

    def set_laser_cooldown(self, laser_cooldown: int):
        self.laser_cooldown = laser_cooldown

    def reduce_laser_cooldown(self, reduction_factor: int):
        self.laser_cooldown = max(0, self.laser_cooldown - reduction_factor)

    def set_laser_speed(self, laser_speed: int) -> None:
        self.laser_speed = laser_speed

    def set_laser_direction(self, laser_direction: Direction):
        self.laser_direction = laser_direction

    @staticmethod
    def direction_queue(ds):
        return ds if isinstance(ds[0], list) else [ds]


class DefaultGun(Gun):
    def __init__(
        self,
        entity,
        laser_cooldown: int,
        collision_layers: CollisionLayers,
        laser_color="white",
        laser_class=Laser,
    ) -> None:
        super().__init__(laser_cooldown)
        self.entity = entity
        self.collision_layers = collision_layers
        self.laser_color = laser_color
        self.laser_class = laser_class

    def shoot(self, directions: Direction) -> None:
        if self.finished_recharging():
            pos = self.entity.rect.center

            for direction in self.direction_queue(directions):
                laser_momentum = direction * np.array(self.laser_speed)
                shot_laser = self.laser_class(
                    pos, laser_momentum, self.collision_layers, self.laser_color
                )

                self.lasers.add(shot_laser)
                self.last_shot_time = pygame.time.get_ticks()

            shot_laser.play_sound()

    def set_color(self, color: str) -> None:
        self.laser_color = color


class GunDecorator(Gun):
    def __init__(self, gun: Gun) -> None:
        self._gun = gun

        self.active_duration = 1000
        self.activation_time = 0

    @property
    def gun(self) -> Gun:
        return self._gun

    def shoot(self, direction: Direction) -> None:
        self._gun.shoot(directions=direction)

    def set_laser_cooldown(self, laser_cooldown: int):
        return self._gun.set_laser_cooldown(laser_cooldown)

    def reduce_laser_cooldown(self, laser_cooldown: int):
        return self._gun.reduce_laser_cooldown(laser_cooldown)

    def activate(self):
        self.activation_time = pygame.time.get_ticks()

    def is_active(self) -> bool:
        ticks = pygame.time.get_ticks()
        time_active = ticks - self.activation_time
        return time_active < self.active_duration


class BeamGun(GunDecorator):
    def __init__(self, gun):
        super().__init__(gun)
        self.active_duration = 10000
        self.gun.reduce_laser_cooldown(100)

    def shoot(self, direction: Direction) -> None:
        self.gun.shoot(direction)


class DelayedGun(GunDecorator):
    def __init__(self, gun: Gun) -> None:
        super().__init__(gun)
        self.active_duration = 30000
        self.x = 0
        self.y = random.uniform(0.25, 0.75)

    def shoot(self, direction: Direction) -> None:
        if self.is_active():
            directions = [[self.x, -self.y]] + self.direction_queue(direction)
            self.gun.shoot(directions)
        else:
            self.gun.shoot(direction)


class MultiGun(GunDecorator):
    def __init__(self, gun: Gun) -> None:
        super().__init__(gun)
        self.active_duration = 25000
        self.x = random.uniform(0, 0.75)
        self.y = 1

    def shoot(self, direction: Direction) -> None:
        if self.is_active():
            directions = [[-self.x, -self.y], [self.x, -self.y]] + self.direction_queue(
                direction
            )
            self.gun.shoot(directions)
        else:
            self.gun.shoot(direction)


class EmptyGun:
    def __init__(self) -> None:
        self.lasers = pygame.sprite.Group()

    def shoot(self):
        print("pew")
