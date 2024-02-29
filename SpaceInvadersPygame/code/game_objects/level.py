from abc import ABC, abstractmethod
from random import randint

import numpy as np
from entities.alien import *
from game_objects.powerup import *
from game_objects.powerup import (
    BeamPowerup,
    DelayedPowerup,
    ImmunityPowerup,
    LifePowerup,
    MultiPowerup,
)
from strategy.alien_creation_strategy import AlienFormations

from .obstacle import Block, ObstacleShape


class LevelCollection:
    def __init__(self):
        self.group = [
            Level_1(),
            Level_6(),
            Level_7(),
            Level_2(),
            Level_3(),
            Level_4(),
            Level_5(),
        ]
        self.nr = 0
        self.alien_pattern = 0
        self.random = False
        self.items_random = False

    def check_level_end(self, game) -> None:
        if len(game.alien_horde1_group) == 0:
            for laser in game.player_laser_group:
                laser.kill()
            for laser in game.alien_laser_group:
                laser.kill()

            self.reset_level(game)
            self.go_to_next_level(game)

    def reset_level(self, game):
        for element in game.extra_alien_group:
            element.kill()
        for element in game.powerup_group:
            element.kill()

        self.group[self.nr].setup_powerup(game, GameAttributes().difficulty)

        self.group[self.nr].countdown = GameAttributes().config.get_option_dev(
            "game", "countdown"
        )

        self.group[self.nr].refill_blocks(game)
        self.group[self.nr].alien_positions.create_aliens(
            game, GameAttributes().difficulty
        )

        game.player_sprite.pos = [
            game.config.screen.width / 2,
            game.config.screen.height - game.player_sprite.rect.height,
        ]

    def go_to_next_level(self, game):
        GameAttributes().level += 1
        if not game.levels.random:
            self.nr = (self.nr + 1) % len(self.group)
        else:
            self.nr = (self.nr + randint(1, len(self.group) - 1)) % len(self.group)


class Level(ABC):
    def __init__(self):
        self.obstacle = ObstacleShape()
        self.countdown = GameAttributes().config.get_option_dev("game", "countdown")
        self.config = GameAttributes().config
        self.alien_positions = AlienFormations()

    @abstractmethod
    def setup_obstacles(self, game):
        pass

    def create_obstacle(self, game, start, shape):
        pos = [0, 0]
        for row_index, row in enumerate(shape):
            for col_index, col in enumerate(row):
                if col == "X":
                    pos[0] = start[0] + col_index * game.block_size
                    pos[1] = start[1] + row_index * game.block_size
                    self.create_single_block(game, pos)

    def create_single_block(self, game, pos):
        block = Block(game.block_size, game.design.get_block_colour(), pos)
        game.block_group.add(block)

    def remove_obstacles(self, game):
        for element in game.block_group:
            element.kill()

    def refill_blocks(self, game):
        self.remove_obstacles(game)
        self.setup_obstacles(game)

    def spawn_health_powerup(self, difficulty):
        if randint(0, 2 + difficulty) == 0:
            return True
        else:
            return False

    def set_random_gun_powerup(self, pos, game):
        rand = randint(0, 2)
        if rand == 0:
            game.powerup_group.add(BeamPowerup(pos))
        elif rand == 1:
            game.powerup_group.add(MultiPowerup(pos))
        else:
            game.powerup_group.add(DelayedPowerup(pos))

    def set_random_life_powerup(self, pos, game):
        rand = randint(0, 1)
        if rand == 0:
            game.powerup_group.add(ImmunityPowerup(pos))
        else:
            game.powerup_group.add(LifePowerup(pos))

    def setup_powerup(self, game, difficulty):
        if game.levels.items_random == True:
            random_position = [randint(10, 950), randint(50, 500)]
            self.set_random_gun_powerup(random_position, game)
            if randint(0, 2 + difficulty) == 0:
                random_position = [randint(10, 950), randint(50, 500)]
                self.set_random_life_powerup(random_position, game)


class Level_1(Level):
    def __init__(self):
        super().__init__()

        # Classic

    def setup_obstacles(self, game):
        game.block_size = game.config.get_option_dev("obstacle", "block_size")
        game.obstacle_amount = game.config.get_option_dev("obstacle", "amount")
        offset = [
            num * (game.screen_width / game.obstacle_amount)
            for num in range(game.obstacle_amount)
        ]

        start = [game.screen_width / 15, 600]
        for set in offset:
            self.create_obstacle(
                game, np.array(start) + [set, 0], self.obstacle.shape_1
            )

        # self.create_obstacle(game, [450, 450], self.obstacle.powerup_shell)

    def setup_powerup(self, game, difficulty):
        if game.levels.items_random == True:
            super().setup_powerup(game, difficulty)
        else:
            pos_gun = [500, 90]
            self.set_random_gun_powerup(pos_gun, game)
            if self.spawn_health_powerup(difficulty):
                if difficulty < 3:
                    self.set_random_life_powerup(self.get_free_position(), game)
                else:
                    self.set_random_life_powerup(self.get_hidden_position(), game)

    def get_hidden_position(self):
        return [random.choice([105, 260, 420, 600, 760, 940]), 500]

    def get_free_position(self):
        return [
            random.choice([130, 365, 650, 860]),
            random.choice(list(range(400, 500))),
        ]

    def get_random_position(self):
        return [
            random.choice(list(range(0, 950))),
            random.choice(list(range(400, 500))),
        ]


class Level_2(Level):
    def __init__(self):
        super().__init__()

        # Triangles on one level

    def setup_obstacles(self, game):
        game.block_size = game.config.get_option_dev("obstacle", "block_size")
        start_positions = [[210, 600], [470, 600], [730, 600]]
        for start in start_positions:
            self.create_obstacle(game, start, self.obstacle.shape_2)

        start_positions = [[80, 600], [340, 600], [600, 600], [860, 600]]
        for start in start_positions:
            self.create_obstacle(game, start, self.obstacle.shape_3)

    def setup_powerup(self, game, difficulty):
        if game.levels.items_random == True:
            super().setup_powerup(game, difficulty)
        elif difficulty <= 2:
            # Powerup gun hidden behind smaller tiles
            self.set_random_gun_powerup(self.get_hidden_position_smaller_tiles(), game)
            # Powerup live random
            if self.spawn_health_powerup(difficulty):
                self.set_random_life_powerup(self.get_random_position(), game)

        elif difficulty <= 4:
            # Powerup gun behind smaller tiles
            self.set_random_gun_powerup(self.get_hidden_position(), game)
            self.set_random_gun_powerup(self.get_hidden_position(), game)
            # Powerup life behind smaller tiles
            if self.spawn_health_powerup(difficulty):
                self.set_random_life_powerup(
                    self.get_hidden_position_smaller_tiles(), game
                )
        else:
            # Powerup gun hidden behind bigger tiles
            self.set_random_gun_powerup(self.get_hidden_position(), game)
            # Powerup life behind bigger tiles
            if self.spawn_health_powerup(difficulty):
                self.set_random_life_powerup(self.get_hidden_position(), game)

    def get_hidden_position(self):
        return [random.choice([105, 365, 625, 880]), int(random.uniform(400, 530))]

    def get_hidden_position_smaller_tiles(self):
        return [random.choice([240, 500, 760]), int(random.uniform(400, 600))]

    def get_random_position(self):
        return [randint(10, 950), randint(50, 500)]


class Level_3(Level):
    def __init__(self):
        super().__init__()

    # diamonds
    def setup_obstacles(self, game):
        game.block_size = game.config.get_option_dev("obstacle", "block_size")
        start_positions = [[500, 500], [200, 700], [700, 700]]
        for start in start_positions:
            self.create_obstacle(game, start, self.obstacle.shape_4)

        start_positions = [[200, 500], [300, 550], [200, 650], [780, 780]]
        for start in start_positions:
            self.create_obstacle(game, start, self.obstacle.shape_5)

    def setup_powerup(self, game, difficulty):
        if difficulty < 2 or game.levels.items_random == True:
            super().setup_powerup(game, difficulty)
        else:
            # Powerup Gun hidden in diamond formation
            self.set_random_gun_powerup(self.get_hidden_position(), game)
            if self.spawn_health_powerup(difficulty):
                if difficulty < 4:
                    # Powerup Life random + extra gun powerup
                    self.set_random_life_powerup(self.get_random_position(), game)
                    self.set_random_gun_powerup(self.get_hidden_position(), game)
                else:
                    # Powerup life hidden in diamond formation
                    self.set_random_life_powerup(self.get_hidden_position(), game)

    def get_free_position(self):
        pos = [0, int(random.uniform(300, 600))]
        pos[0] = random.choice(
            [
                int(random.uniform(20, 180)),
                int(random.uniform(360, 500)),
                int(random.uniform(830, 960)),
            ]
        )
        return pos

    def get_hidden_position(self):
        return random.choice(
            [[240, 580], [540, 500], [760, int(random.uniform(400, 600))]]
        )

    def get_random_position(self):
        return [randint(10, 950), randint(100, 500)]


class Level_4(Level):
    def __init__(self):
        super().__init__()

    # Heart
    def setup_obstacles(self, game):
        game.block_size = game.config.get_option_dev("obstacle", "block_size")
        start_positions = [[170, 600], [600, 600]]
        for start in start_positions:
            self.create_obstacle(game, start, self.obstacle.shape_6)

        start_positions = [[370, 600], [800, 600]]
        for start in start_positions:
            self.create_obstacle(game, start, self.obstacle.shape_7)

    def setup_powerup(self, game, difficulty):
        if game.levels.items_random == True:
            super().setup_powerup(game, difficulty)
        self.set_random_gun_powerup(self.get_free_position(), game)
        if self.spawn_health_powerup(difficulty):
            self.set_random_life_powerup(self.get_free_position(), game)
        elif difficulty < 4:
            # Powerups free
            self.set_random_gun_powerup(self.get_free_position(), game)
        else:
            # Powerups behind hearts
            self.set_random_gun_powerup(self.get_hidden_position(), game)
            if self.spawn_health_powerup(difficulty):
                self.set_random_life_powerup(self.get_hidden_position(), game)

    def get_free_position(self):
        return [random.choice([100, 290, 500, 720, 900]), int(random.uniform(300, 600))]

    def get_hidden_position(self):
        return [random.choice([225, 425, 645, 845]), int(random.uniform(300, 450))]


class Level_5(Level):
    def __init__(self):
        super().__init__()

    # Triangles on different levels
    def setup_obstacles(self, game):
        game.block_size = game.config.get_option_dev("obstacle", "block_size")
        start_positions = [[210, 630], [470, 630], [730, 630]]
        for start in start_positions:
            self.create_obstacle(game, start, self.obstacle.shape_2)

        start_positions = [[80, 570], [340, 570], [600, 570], [860, 570]]
        for start in start_positions:
            self.create_obstacle(game, start, self.obstacle.shape_3)

    def setup_powerup(self, game, difficulty):
        if game.levels.items_random == True:
            super().setup_powerup(game, difficulty)
        elif difficulty <= 2:
            # Powerup gun behind small tiles
            self.set_random_gun_powerup(self.get_hidden_position_smaller_tiles(), game)
            self.set_random_gun_powerup(self.get_hidden_position(), game)
            # Powerup life random
            if self.spawn_health_powerup(difficulty):
                self.set_random_life_powerup(self.get_random_position(), game)
        elif difficulty == 3:
            # Powerup gun behind small tiles
            self.set_random_gun_powerup(self.get_hidden_position_smaller_tiles(), game)
            # Powerup life random
            if self.spawn_health_powerup(difficulty):
                self.set_random_life_powerup(self.get_random_position(), game)
        else:
            # Powerup gun behind big tiles
            self.set_random_gun_powerup(self.get_hidden_position(), game)
            # Powerup life behind small tiles
            if self.spawn_health_powerup(difficulty):
                self.set_random_life_powerup(self.get_hidden_position(), game)

    def get_hidden_position(self):
        return [random.choice([105, 365, 625, 880]), int(random.uniform(400, 530))]

    def get_hidden_position_smaller_tiles(self):
        return [random.choice([240, 500, 760]), int(random.uniform(400, 600))]

    def get_random_position(self):
        return [randint(10, 950), randint(50, 500)]


class Level_6(Level):
    def __init__(self):
        super().__init__()

    # one line, middle free
    def setup_obstacles(self, game):
        game.block_size = game.config.get_option_dev("obstacle", "block_size")
        start_positions = [[0, 600], [615, 600]]
        for start in start_positions:
            self.create_obstacle(game, start, self.obstacle.shape_8)

    def setup_powerup(self, game, difficulty):
        if game.levels.items_random == True:
            super().setup_powerup(game, difficulty)
        elif difficulty < 3:
            # powerup gun accessable
            self.set_random_gun_powerup(self.get_free_position(), game)
            self.set_random_gun_powerup(self.get_hidden_position(), game)
        else:
            # powerups behind the borders
            self.set_random_gun_powerup(self.get_hidden_position(), game)
            self.set_random_life_powerup(self.get_hidden_position(), game)

    def get_free_position(self):
        return [int(random.uniform(490, 600)), int(random.uniform(400, 600))]

    def get_hidden_position(self):
        return [
            random.choice(list(range(0, 301)) + list(range(620, 941))),
            int(random.uniform(400, 600)),
        ]


class Level_7(Level):
    def __init__(self):
        super().__init__()

    # :)
    def setup_obstacles(self, game):
        game.block_size = game.config.get_option_dev("obstacle", "block_size")
        start_positions = [[110, 700], [850, 700]]
        for start in start_positions:
            self.create_obstacle(game, start, self.obstacle.shape_9)
        start_positions = [[290, 500], [670, 500]]
        for start in start_positions:
            self.create_obstacle(game, start, self.obstacle.shape_10)
        self.create_obstacle(game, [470, 600], self.obstacle.shape_11)

    def setup_powerup(self, game, difficulty):
        if game.levels.items_random == True:
            super().setup_powerup(game, difficulty)
        elif difficulty >= 4:
            self.set_random_gun_powerup(self.get_hidden_position(), game)
        else:
            self.set_random_gun_powerup(self.get_free_position(), game)
            self.set_random_gun_powerup(self.get_hidden_position(), game)

        if self.spawn_health_powerup(difficulty):
            self.set_random_life_powerup(self.get_free_position(), game)

    def get_hidden_position(self):
        return [random.choice([120, 300, 500, 680, 860]), int(random.uniform(400, 550))]

    def get_free_position(self):
        return [
            random.choice([50, 410, 620, 930]),
            int(random.uniform(400, 600)),
        ]
