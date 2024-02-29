from entities.player import Player
from game_attributes import GameAttributes
from game_groups import GameGroups
from game_objects.obstacle import Block
from pygame import sprite


class Setup:
    def __init__(self) -> None:
        self.game_groups = GameGroups()
        self.game_attrs = GameAttributes()


class SetupPlayer(Setup):
    def setup(self) -> Player:
        player_init_pos = (
            self.game_attrs.screen_width / 2,
            self.game_attrs.screen_height,
        )
        player_init_speed = self.game_attrs.config.speeds.player

        player_sprite = Player(player_init_pos, player_init_speed)
        player_group = sprite.GroupSingle(player_sprite)
        player_laser_group = player_sprite.lasers

        self.game_groups.player = player_group
        self.game_groups.player_laser = player_laser_group

        return player_sprite


class SetupAlien(Setup):
    def setup(self):
        self.game_groups.alien_red = sprite.Group()
        self.game_groups.alien_green = sprite.Group()
        self.game_groups.alien_yellow = sprite.Group()
        self.game_groups.alien_horde1 = sprite.Group()
        self.game_groups.aliens = sprite.Group()
        self.game_groups.alien_laser = sprite.Group()


class SetupObstacle(Setup):
    def setup(self):
        blocks = sprite.Group()
        self.game_groups.blocks = blocks

    def create_single_block(self, game, pos):
        block = Block(game.block_size, game.config.get_option_dev("colour", "red"), pos)
        self.game_groups.blocks.add(block)

    def remove_obstacles(self):
        for element in self.game_groups.blocks:
            element.kill()
