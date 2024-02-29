import pygame
from collision.collision_layers import CollisionLayers
from game_attributes import GameAttributes
from game_objects.game_object import GameObject
from pygame import Surface


class Laser(GameObject):
    def __init__(
        self,
        pos,
        momentum,
        collision_layers: CollisionLayers,
        laser_color: str = "white",
    ):
        super().__init__(collision_layers=collision_layers)
        self.momentum = momentum

        self.laser_sound = self.design.laser_sound
        self.laser_sound.set_volume(self.config.volumes.sounds)

        self.image = Surface(self.config.get_option_dev("laser", "size"))
        self.image.fill(laser_color)
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)
        self.height_y_constraint = self.config.screen.height
        self.destroy_condition = self.config.get_option_dev("laser", "destroy")

    def destroy(self):
        if (
            self.rect.y <= -self.destroy_condition
            or self.rect.y >= self.height_y_constraint + self.destroy_condition
            or self.rect.x < 0
            or self.rect.x > self.config.screen.width
        ):
            self.kill()

    def action(self):
        self.move("simple_move")
        self.destroy()

    def play_sound(self):
        if GameAttributes().config.volumes.sound_on:
            self.laser_sound.play()

    def set_color(self, color: str):
        self.image.fill(color)


class BigLaser(Laser):
    def __init__(
        self, pos, momentum, collision_layers: CollisionLayers, laser_color: str
    ):
        super().__init__(pos, momentum, collision_layers, laser_color)
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect(center=pos)
