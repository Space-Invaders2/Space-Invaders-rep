import pygame
from collision.collision_layers import CollisionLayers, ObjectLayer
from design.change_design import ComponentToBeUpdated, Visitor
from strategy.gun import DefaultGun

from .entity import Entity


class Player(Entity, ComponentToBeUpdated):
    def __init__(self, pos, speed):
        collision_layers = CollisionLayers(
            object_name="Player",
            object_layer=ObjectLayer.PLAYER,
            collidable_layers=[ObjectLayer.ALIEN_LASER, ObjectLayer.ALIEN],
        )
        super().__init__(collision_layers=collision_layers)

        self.image = self.design.get_player_image()
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = [pos[0], pos[1] - self.rect.height]
        self.max_x_constraint = self.game_attributes.screen_width - self.rect.width

        self.lives = self.config.get_option_dev("player", "lives")
        self.immunity = -1
        self.speed = speed
        self.ready = True
        self.direction = [0, -1]

        self.laser_cooldown = self.config.get_option_dev("player", "laser_cooldown")
        self.gun = DefaultGun(
            self,
            self.laser_cooldown,
            CollisionLayers(
                object_name="Laser",
                object_layer=ObjectLayer.PLAYER_LASER,
                collidable_layers=[ObjectLayer.ALIEN],
            ),
        )
        self.new_gun = self.gun
        self.lasers = self.gun.lasers
        self.laser_time = 0

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            momentum = [self.speed, 0]
        elif keys[pygame.K_LEFT]:
            momentum = [-self.speed, 0]
        else:
            momentum = [0, 0]
        self.momentum = momentum

        if keys[pygame.K_SPACE] and self.ready:
            super().shoot()

    def constraint(self):
        def right_boundary(x):
            return min(x, self.max_x_constraint)

        def left_boundary(x):
            return max(0, x)

        def constraint_boundary(x):
            return left_boundary(right_boundary(x))

        self.pos[0] = constraint_boundary(self.pos[0])
        self.rect.left = self.pos[0]

    def action(self):
        self.get_input()
        self.move("simple_move")
        self.constraint()

    def display_lives(self, screen: pygame.Surface) -> None:
        life_width = self.image.get_size()[0]
        life_spacing = 10

        self.lives_x_start_pos = screen.get_size()[0] - (
            (life_width + life_spacing) * self.lives
        )
        for life in reversed(range(self.lives)):
            x = self.lives_x_start_pos + (life * (life_width + life_spacing))
            screen.blit(self.image, (x, 8))

    def verify_immunity(self):
        if self.immunity >= 0:
            self.immunity -= 1

    def accept(self, visitor: Visitor):
        visitor.change_player_sprite(self)
