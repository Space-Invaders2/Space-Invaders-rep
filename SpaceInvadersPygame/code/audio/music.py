import pygame
from config import ConfigDev
from design.change_design import ComponentToBeUpdated, Visitor
from game_attributes import GameAttributes


class Music(ComponentToBeUpdated):
    def __init__(self, game_attributes: GameAttributes):
        game_attributes.design.get_music()
        pygame.mixer.music.set_volume(game_attributes.config.volumes.music)
        pygame.mixer.music.play(loops=-1)

    def volume_up_music(self, config: ConfigDev):
        if config.volumes.music < 1:
            config.volumes.music += 0.1
            pygame.mixer.music.set_volume(config.volumes.music)

    def volume_down_music(self, config: ConfigDev):
        if config.volumes.music > 0:
            config.volumes.music -= 0.1
            pygame.mixer.music.set_volume(config.volumes.music)

    def mute_unmute_music(self, config: ConfigDev):
        if config.volumes.music_on:
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.set_volume(config.volumes.music)
            pygame.mixer.music.play(loops=-1)

        config.volumes.music_on = not config.volumes.music_on

    def accept(self, visitor: Visitor):
        visitor.change_music(self)
