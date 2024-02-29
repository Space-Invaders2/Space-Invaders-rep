import sys
from os import path

import pygame
from audio.music import Music
from audio.sounds import Sound
from collision.collision_layers import CollisionLayers, ObjectLayer
from collision.collision_strategy import CollisionHandler
from design.graphics import ClassicDesignFactory
from entities.alien import AlienShotsHandler
from game_attributes import GameAttributes, SingletonMeta
from game_groups import GameGroups
from game_objects.level import LevelCollection
from game_setup import SetupAlien, SetupObstacle, SetupPlayer
from pygame.sprite import Group
from strategy.gun import DefaultGun
from strategy.move_strategy import MoveHandler


class Game(metaclass=SingletonMeta):
    def __init__(self, design=ClassicDesignFactory()):
        self.game_attributes = GameAttributes(score=0, design=design)

        # Set groups
        self.game_groups = GameGroups()
        SetupObstacle().setup()
        self.block_group = self.game_groups.blocks

        self.extra_alien_group = pygame.sprite.GroupSingle()
        self.powerup_group = pygame.sprite.Group()

        SetupAlien().setup()
        self.alien_red_group: Group = self.game_groups.alien_red
        self.alien_green_group: Group = self.game_groups.alien_green
        self.alien_yellow_group: Group = self.game_groups.alien_yellow
        self.alien_horde1_group: Group = self.game_groups.alien_horde1
        self.alien_group: Group = self.game_groups.aliens
        self.alien_laser_group: Group = self.game_groups.alien_laser

        # Display setup
        self.setup_display()

        #  Objects setup
        self.player_name = None
        self.player_sprite = SetupPlayer().setup()
        self.player_group = self.game_groups.player
        self.player_laser_group = self.game_groups.player_laser
        self.levels = LevelCollection()

        # Collision setup
        self.groups = [
            self.alien_group,
            self.extra_alien_group,
            self.alien_laser_group,
            self.player_group,
            self.player_laser_group,
            self.powerup_group,
            self.block_group,
        ]

        self.collision_handler = CollisionHandler(self.groups)

        # Move setup
        self.move_handler = MoveHandler(self.groups)

        # Sound Settings
        self.music = Music(self.game_attributes)
        self.sound = Sound()

        self.new_game()

    @property
    def player_lives(self):
        return self.player_group.sprite.lives

    @property
    def design(self):
        return self.game_attributes.design

    @property
    def config(self):
        return self.game_attributes.config

    @property
    def level(self):
        return self.game_attributes.level

    def new_game(self):
        GameAttributes().scoreboard.score = 0
        GameAttributes().level = 0
        self.levels.nr = 0
        self.levels.alien_pattern = 0
        self.player_name = None
        self.player_sprite.gun = self.player_sprite.new_gun
        self.player_sprite.gun.set_laser_cooldown(
            self.config.get_option_dev("player", "laser_cooldown")
        )
        self.player_sprite.lives = self.config.get_option_dev("player", "lives")
        self.difficulty = self.game_attributes.config.get_option_dev(
            "game", "difficulty"
        )
        self.tick = (
            self.game_attributes.config.get_option_dev("game", "time_tick")
            + self.game_attributes.config.get_option_dev("game", "difficulty") * 2
        )
        GameAttributes().highscores.game_saved = False
        self.levels.group[
            self.levels.nr
        ].countdown = GameAttributes().config.get_option_dev("game", "countdown")
        self.levels.nr = 0

    def setup_display(self):
        self.screen_width = self.config.screen.width
        self.screen_height = self.config.screen.height
        dimensions = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(dimensions)
        self.font = self.design.get_font()
        self.deep_space = pygame.image.load(
            path.join(
                path.dirname(path.abspath(__file__)), "..", "graphics", "deep_space.png"
            )
        ).convert_alpha()

        self.deep_space = pygame.transform.scale(
            self.deep_space, (self.screen_width, self.screen_height)
        )

    def handle_moves(self):
        self.move_handler.handle_moves()

    def handle_collisions(self):
        self.collision_handler.handle_collisions()

    @staticmethod
    def exit_game():
        pygame.quit()
        sys.exit()

    # check if still needed
    def display_victory_screen(self):
        victory_surf = self.font.render("You Won", "False", "white")
        victory_rect = victory_surf.get_rect(
            center=(self.screen_width / 2, self.screen_height / 2)
        )
        self.screen.blit(victory_surf, victory_rect)

    def check_defeat(self) -> bool:
        return self.player_lives <= 0

    def check_game_end(self):
        if self.check_defeat():
            self.endscore = GameAttributes().scoreboard.score
            return True
        if self.levels.group[self.levels.nr].countdown <= 0:
            self.endscore = GameAttributes().scoreboard.score
            return True

    def display_level(self):
        if self.game_attributes.level > 0:
            level_surf = self.font.render(
                f"level {self.game_attributes.level}", "False", "white"
            )
            level_rect = level_surf.get_rect(
                center=(self.screen_width / 2, self.screen_height / 2)
            )
            self.screen.blit(level_surf, level_rect)

    def display_background(self):
        self.screen.blit(self.deep_space, (0, 0))

    def draw(self):
        self.display_background()
        self.player_laser_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.block_group.draw(self.screen)
        self.powerup_group.draw(self.screen)
        self.alien_group.draw(self.screen)
        self.alien_laser_group.draw(self.screen)
        self.extra_alien_group.draw(self.screen)

        self.player_sprite.display_lives(self.screen)
        GameAttributes().scoreboard.display_score(self.screen)
        self.display_level()

    def run(self):
        # Handles
        self.handle_moves()
        self.handle_collisions()

        # check level end
        self.levels.check_level_end(self)

        if self.check_game_end():
            for obj in self.alien_group:
                obj.kill()
            return False
        else:
            self.draw()


class GameSetup:
    def __init__(self):
        pygame.init()
        self.game_attributes = GameAttributes()
        config = self.game_attributes.config

        self.screen_width = config.screen.width
        self.screen_height = config.screen.height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.clock = pygame.time.Clock()

        self.start_game_variables()

        # events
        self.ALIEN_LASER = pygame.USEREVENT + 1
        pygame.time.set_timer(
            self.ALIEN_LASER, config.get_option_dev("laser", "spawn_alien")
        )

        self.EXTRA_ALIEN_SPAWN = pygame.USEREVENT + 2
        pygame.time.set_timer(
            self.EXTRA_ALIEN_SPAWN, config.get_option_dev("laser", "spawn_alien_extra")
        )

        self.alien_shoots = AlienShotsHandler()

    def start_game_variables(self):
        # Menu variables
        (
            self.game_paused,
            self.game_running,
            self.settings_open,
            self.sound_settings_open,
            self.highscore_open,
            self.game_over,
        ) = (False, False, False, False, False, False)
