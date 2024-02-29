from random import randint

import pygame
from collision.collision_layers import CollisionLayers, ObjectLayer
from design.change_design import ComponentToBeUpdated, Visitor
from game_attributes import GameAttributes
from game_objects.game_object import GameObject
from game_types import Position
from strategy.gun import BeamGun, DelayedGun, MultiGun


class Powerup(GameObject, ComponentToBeUpdated):
    def __init__(self, pos: Position, powerup_type: str):
        super().__init__(
            collision_layers=CollisionLayers(
                object_name="Powerup",
                object_layer=ObjectLayer.POWERUP,
                collidable_layers=[ObjectLayer.PLAYER_LASER],
            )
        )
        self.speed = 5
        self.pos = pos
        self.type = powerup_type
        self.image = self.design.get_powerup_image(self.type)
        self.rect = self.image.get_rect(center=pos)

        self.height_y_constraint = self.config.screen.height
        self.destroy_condition = self.config.get_option_dev("laser", "destroy")

    def destroy(self):
        some_variable = self.destroy_condition
        if (
            self.rect.y <= -some_variable
            or self.rect.y >= self.height_y_constraint + some_variable
        ):
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()

    def accept(self, visitor: Visitor):
        visitor.change_powerup(self, self.type)


class LifePowerup(Powerup):
    def __init__(self, pos):
        super().__init__(pos, powerup_type="life")

    def upgrade(self, player):
        if player.lives < GameAttributes().config.get_option_dev("player", "max_lives"):
            player.lives += 1


class ImmunityPowerup(Powerup):
    def __init__(self, pos):
        super().__init__(pos, powerup_type="immunity")
        self.activation_duration = 2000

    def upgrade(self, player):
        player.immunity = self.activation_duration


class BeamPowerup(Powerup):
    def __init__(self, pos):
        super().__init__(pos, powerup_type="beam")

    def upgrade(self, player):
        player.gun = BeamGun(player.gun)
        player.gun.activate()


class DelayedPowerup(Powerup):
    def __init__(self, pos):
        super().__init__(pos, powerup_type="delayed")

    def upgrade(self, player):
        player.gun = DelayedGun(player.gun)
        player.gun.activate()


class MultiPowerup(Powerup):
    def __init__(self, pos):
        super().__init__(pos, powerup_type="multi")

    def upgrade(self, player):
        player.gun = MultiGun(player.gun)
        player.gun.activate()
