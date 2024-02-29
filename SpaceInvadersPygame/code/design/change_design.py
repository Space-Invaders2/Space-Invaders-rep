from abc import ABC, abstractmethod

import pygame
from design.graphics import (
    AbstractDesignFactory,
    BlackWhiteDesignFactory,
    ChristmasDesignFactory,
    ClassicDesignFactory,
    ModernDesignFactory,
)
from game_attributes import GameAttributes


class ChangeDesign:
    def __init__(self):
        self.design_name = None
        self.designs = ["classic", "modern", "black_white", "christmas"]
        self.update = DesignUpdater()

    def create(self, design_name):
        if design_name == "classic":
            return ClassicDesignFactory()
        elif design_name == "modern":
            return ModernDesignFactory()
        elif design_name == "black_white":
            return BlackWhiteDesignFactory()
        elif design_name == "christmas":
            return ChristmasDesignFactory()

    def next_design(self, current: AbstractDesignFactory):
        try:
            index = self.designs.index(current.design_name)
        except ValueError:
            return self.design_name
        next_index = (index + 1) % len(self.designs)
        return self.designs[next_index]


class Visitor(ABC):
    @abstractmethod
    def change_music(self) -> None:
        pass

    @abstractmethod
    def change_player_sprite(self):
        pass

    @abstractmethod
    def change_alien_red(self):
        pass

    @abstractmethod
    def change_alien_green(self):
        pass

    @abstractmethod
    def change_alien_yellow(self):
        pass

    @abstractmethod
    def change_alien_extra(self):
        pass

    @abstractmethod
    def change_block_colour(self):
        pass

    @abstractmethod
    def change_powerup(self):
        pass


class DesignUpdater(Visitor):
    def change_music(self, music):
        GameAttributes().design.get_music()
        if not GameAttributes().config.volumes.music_on:
            pygame.mixer.music.stop()

    def change_player_sprite(self, player):
        player.image = GameAttributes().design.get_player_image()

    def change_alien_red(self, alien):
        alien.image = GameAttributes().design.get_alien_image("red")

    def change_alien_green(self, alien):
        alien.image = GameAttributes().design.get_alien_image("green")

    def change_alien_yellow(self, alien):
        alien.image = GameAttributes().design.get_alien_image("yellow")

    def change_alien_extra(self, alien):
        alien.image = GameAttributes().design.get_alien_image("extra")

    def change_block_colour(self, block):
        block.image.fill(GameAttributes().design.get_block_colour())

    def change_powerup(self, powerup, type):
        powerup.image = GameAttributes().design.get_powerup_image(type)


class ComponentToBeUpdated(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor):
        pass
