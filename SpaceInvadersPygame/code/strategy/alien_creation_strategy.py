from abc import ABC

from entities.alien import *
from game_attributes import GameAttributes


class AlienFormations:
    def __init__(self):
        self.patterns = [
            AlienFormation1(),
            AlienFormation2(),
            AlienFormation5(),
            AlienFormation3(),
            AlienFormation4(),
        ]

    def create_aliens(self, game, difficulty):
        self.patterns[game.levels.alien_pattern].create(game, difficulty)
        game.levels.alien_pattern = (game.levels.alien_pattern + 1) % len(self.patterns)


class AlienFormationStrategy(ABC):
    def __init__(self):
        self.config = GameAttributes().config

    def create(
        game, difficulty, x_distance=60, y_distance=48, x_offset=70, y_offset=100
    ):
        pass


class AlienFormation1(AlienFormationStrategy):
    # 1, 2, 3
    def create(self, game, difficulty):
        rows = self.config.alien_positions.rows + int(difficulty // 2)
        cols = self.config.alien_positions.cols + difficulty - 3
        for row_index, _ in enumerate(range(rows)):
            for col_index, _ in enumerate(range(cols)):
                x = (
                    col_index * self.config.alien_positions.x_distance
                    + self.config.alien_positions.x_offset
                )
                y = (
                    row_index * self.config.alien_positions.y_distance
                    + self.config.alien_positions.y_offset
                )

                if row_index == 0:
                    alien_sprite = AlienYellow(x, y)
                    game.alien_yellow_group.add(alien_sprite)
                elif 1 <= row_index <= 2:
                    alien_sprite = AlienGreen(x, y)
                    game.alien_green_group.add(alien_sprite)
                else:
                    alien_sprite = AlienRed(x, y)
                    game.alien_red_group.add(alien_sprite)

                game.alien_horde1_group.add(alien_sprite)
                game.alien_group.add(alien_sprite)


class AlienFormation2(AlienFormationStrategy):
    # 1, 3, 3
    def create(self, game, difficulty):
        rows = self.config.alien_positions.rows + int(difficulty // 2) + 1
        cols = self.config.alien_positions.cols + difficulty - 3
        for row_index, _ in enumerate(range(rows)):
            for col_index, _ in enumerate(range(cols)):
                x = (
                    col_index * self.config.alien_positions.x_distance
                    + self.config.alien_positions.x_offset
                )
                y = (
                    row_index * self.config.alien_positions.y_distance
                    + self.config.alien_positions.y_offset
                )

                if row_index == 0:
                    alien_sprite = AlienYellow(x, y)
                    game.alien_yellow_group.add(alien_sprite)
                elif 1 <= row_index <= 3:
                    alien_sprite = AlienGreen(x, y)
                    game.alien_green_group.add(alien_sprite)
                else:
                    alien_sprite = AlienRed(x, y)
                    game.alien_red_group.add(alien_sprite)

                game.alien_horde1_group.add(alien_sprite)
                game.alien_group.add(alien_sprite)


class AlienFormation3(AlienFormationStrategy):
    # 2, 2, 2
    def create(self, game, difficulty):
        rows = self.config.alien_positions.rows + int(difficulty // 2)
        cols = self.config.alien_positions.cols + difficulty - 4
        for row_index, _ in enumerate(range(rows)):
            for col_index, _ in enumerate(range(cols)):
                x = (
                    col_index * self.config.alien_positions.x_distance
                    + self.config.alien_positions.x_offset
                )
                y = (
                    row_index * self.config.alien_positions.y_distance
                    + self.config.alien_positions.y_offset
                )

                if row_index <= 1:
                    alien_sprite = AlienYellow(x, y)
                    game.alien_yellow_group.add(alien_sprite)
                elif row_index <= 3:
                    alien_sprite = AlienGreen(x, y)
                    game.alien_green_group.add(alien_sprite)
                else:
                    alien_sprite = AlienRed(x, y)
                    game.alien_red_group.add(alien_sprite)

                game.alien_horde1_group.add(alien_sprite)
                game.alien_group.add(alien_sprite)


class AlienFormation4(AlienFormationStrategy):
    # 3, 3, 3
    def create(self, game, difficulty):
        rows = self.config.alien_positions.rows + int(difficulty // 2) + 3
        cols = self.config.alien_positions.cols + difficulty - 7
        for row_index, _ in enumerate(range(rows)):
            for col_index, _ in enumerate(range(cols)):
                x = (
                    col_index * self.config.alien_positions.x_distance
                    + self.config.alien_positions.x_offset
                )
                y = (
                    row_index * self.config.alien_positions.y_distance
                    + self.config.alien_positions.y_offset
                )

                if row_index == 0:
                    alien_sprite = AlienYellow(x, y)
                    game.alien_yellow_group.add(alien_sprite)
                elif 1 <= row_index <= 2:
                    alien_sprite = AlienGreen(x, y)
                    game.alien_green_group.add(alien_sprite)
                else:
                    alien_sprite = AlienRed(x, y)
                    game.alien_red_group.add(alien_sprite)

                game.alien_horde1_group.add(alien_sprite)
                game.alien_group.add(alien_sprite)


class AlienFormation5(AlienFormationStrategy):
    # 1, 1, 1
    def create(self, game, difficulty):
        rows = self.config.alien_positions.rows + int(difficulty // 2) - 3
        cols = self.config.alien_positions.cols + difficulty - 2
        for row_index, _ in enumerate(range(rows)):
            for col_index, _ in enumerate(range(cols)):
                x = (
                    col_index * self.config.alien_positions.x_distance
                    + self.config.alien_positions.x_offset
                    - 20
                )
                y = (
                    row_index * self.config.alien_positions.y_distance
                    + self.config.alien_positions.y_offset
                )

                if row_index == 0:
                    alien_sprite = AlienYellow(x, y)
                    game.alien_yellow_group.add(alien_sprite)
                elif row_index <= 1:
                    alien_sprite = AlienGreen(x, y)
                    game.alien_green_group.add(alien_sprite)
                else:
                    alien_sprite = AlienRed(x, y)
                    game.alien_red_group.add(alien_sprite)

                game.alien_horde1_group.add(alien_sprite)
                game.alien_group.add(alien_sprite)
