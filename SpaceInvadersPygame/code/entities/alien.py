import random

import numpy as np
from audio.sounds import Sound
from collision.collision_layers import CollisionLayers, ObjectLayer
from collision.collision_strategy import BoundaryCollision
from design.change_design import ComponentToBeUpdated, Visitor
from entities.entity import Entity
from game_attributes import GameAttributes
from game_groups import GameGroups
from strategy.gun import DefaultGun


class GenericAlien(Entity, ComponentToBeUpdated):
    def __init__(self) -> None:
        Entity.__init__(
            self,
            collision_layers=CollisionLayers(
                object_name="Alien",
                object_layer=ObjectLayer.ALIEN,
                collidable_layers=[ObjectLayer.PLAYER_LASER, ObjectLayer.BLOCK],
            ),
        )
        self.groups = GameGroups().alien_horde1

        self.score_points = self.config.points.extra
        self.speed = self.config.speeds.alien
        self.direction = [0, 1]

    def change_momentum(self, momentum):
        self.momentum = momentum

    def action(self):
        self.move("simple_move")

    def accept(self, visitor: Visitor):
        pass


class Boss(Entity):
    def __init__(self):
        self.pos = [500, 50]
        self.image = self.design.get_boss_image()
        self.rect = self.image.get_rect(topleft=self.pos)


class AlienShooter(GenericAlien):
    def __init__(self) -> None:
        super().__init__()

        self.momentum = [1, 0]
        self.set_gun()

    def set_gun(self):
        laser_cooldown = 0
        collision_layer = CollisionLayers(
            object_name="Laser",
            object_layer=ObjectLayer.ALIEN_LASER,
            collidable_layers=[],
        )
        self.gun = DefaultGun(self, laser_cooldown, collision_layer)

        self.lasers = self.gun.lasers

    def alien_wall_collision(self):
        self.wall_collision = BoundaryCollision().handle_collision(self)
        if self.wall_collision != None:
            self.change_movement(self.groups)

    def change_movement(self, group):
        for entity in group:
            momentum = np.array(self.wall_collision) * np.array(entity.momentum)
            entity.change_momentum(momentum)
            self.advance(entity)

    def advance(self, alien):
        if self.wall_collision[0] == -1:
            alien.move("advance")

    def action(self):
        super().action()
        self.alien_wall_collision()


class AlienRed(AlienShooter):
    def __init__(self, x, y):
        super().__init__()
        self.pos = [x, y]
        self.image = self.design.get_alien_image("red")
        self.gun.set_color("red")
        self.groups = GameGroups().alien_red

        if self.game_attributes.level % 2 == 1:
            self.momentum = [-2, 0]

        self.rect = self.image.get_rect(topleft=self.pos)

        self.score_points = self.config.points.red

    def accept(self, visitor: Visitor):
        visitor.change_alien_red(self)


class AlienGreen(AlienShooter):
    def __init__(self, x, y):
        super().__init__()
        self.pos = [x, y]
        self.image = self.design.get_alien_image("green")
        self.gun.set_color("green")
        self.groups = GameGroups().alien_green
        if self.game_attributes.level % 2 == 1:
            self.momentum = [2, 0]
        elif self.game_attributes.level % 3 == 1:
            self.momentum = [-2, 0]

        self.rect = self.image.get_rect(topleft=self.pos)
        self.score_points = self.config.points.red

    def accept(self, visitor: Visitor):
        visitor.change_alien_green(self)


class AlienYellow(AlienShooter):
    def __init__(self, x, y):
        super().__init__()
        if self.game_attributes.level % 3 == 1:
            self.momentum = [0, 0]
        self.image = self.design.get_alien_image("yellow")
        self.gun.set_color("yellow")
        self.pos = [x, y]
        self.groups = GameGroups().alien_yellow
        self.image = self.design.get_alien_image("yellow")
        if self.game_attributes.level % 3 == 1:
            self.momentum = [0, 0]

        self.rect = self.image.get_rect(topleft=self.pos)
        self.score_points = self.config.points.red

    def accept(self, visitor: Visitor):
        visitor.change_alien_yellow(self)


class ExtraAlien(GenericAlien):
    def __init__(self, momentum) -> None:
        self.config = GameAttributes().config

        super().__init__()
        self.set_pos(momentum)

        momentum = self.config.get_option_dev("alien", self.momentum_name)
        self.image = self.design.get_alien_image("extra")
        self.rect = self.image.get_rect(topleft=self.pos)
        self.momentum = momentum

    def set_pos(self, momentum):
        alien_distance_to_border = self.config.get_option_dev(
            "alien", "distance_border"
        )
        screen_width = self.config.get_option_dev("screen", "width")
        if momentum == "right":
            x = screen_width + alien_distance_to_border
            self.momentum_name = "move_momentum_right"

        elif momentum == "left":
            x = -(alien_distance_to_border)
            self.momentum_name = "move_momentum_left"
        y = self.config.get_option_dev("offset", "extra_alien_y")
        self.pos = [x, y]

    def accept(self, visitor: Visitor):
        visitor.change_alien_extra(self)


def extra_alien_spawn(game):
    momentum_name = random.choice(["right", "left"])
    extra_alien = ExtraAlien(momentum_name)
    game.extra_alien_group.add(extra_alien)


class AlienShotsHandler:
    def __init__(self):
        self.laser_sound = Sound()
        self.game_groups = GameGroups()

    def alien_shoot_lasers(self):
        if self.game_groups.aliens:
            random_alien = random.choice(self.game_groups.aliens.sprites())
            random_alien.shoot()
            self.game_groups.alien_laser.add(random_alien.lasers)
            self.laser_sound.play_laser()
