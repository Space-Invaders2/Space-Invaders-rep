from abc import ABC, abstractmethod

import pygame
from config import ConfigDev
from game_attributes import GameAttributes, SingletonMeta


class Sound(metaclass=SingletonMeta):
    def __init__(self):
        pygame.mixer.init()
        design = GameAttributes().design
        self.config = GameAttributes().config
        self.explosion_sound = design.explosion_sound
        self.explosion_sound.set_volume(self.config.volumes.explosion_max)
        self.explosion_increment = self.config.volumes.explosion_max / 10
        self.laser_sound = design.laser_sound
        self.laser_sound.set_volume(self.config.volumes.laser_max)
        self.laser_increment = self.config.volumes.laser_max / 10

    def volume_up_sounds(self, config: ConfigDev):
        if config.volumes.explosion < config.volumes.explosion_max:
            config.volumes.explosion += self.explosion_increment
            self.explosion_sound.set_volume(config.volumes.explosion)

        if config.volumes.laser < config.volumes.laser_max:
            config.volumes.laser += self.laser_increment
            self.laser_sound.set_volume(config.volumes.laser)

        if config.volumes.sounds < 1:
            config.volumes.sounds += 0.1

    def volume_down_sounds(self, config: ConfigDev):
        if config.volumes.explosion > 0:
            config.volumes.explosion -= self.explosion_increment
            self.explosion_sound.set_volume(config.volumes.explosion)

        if config.volumes.laser > 0:
            config.volumes.laser -= self.laser_increment
            self.laser_sound.set_volume(config.volumes.laser)

        if config.volumes.sounds > 0:
            config.volumes.sounds -= 0.1

    def mute_unmute_sounds(self, config: ConfigDev):
        config.volumes.sound_on = not config.volumes.sound_on

    def play_laser(self):
        if self.config.volumes.sound_on:
            self.laser_sound.play()

    def play_explosion(self):
        if self.config.volumes.sound_on:
            self.explosion_sound.play()
