from game_attributes import SingletonMeta


class GameGroups(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.alien_groups = {
            "alien_red": None,
            "alien_green": None,
            "alien_yellow": None,
            "alien_horde1": None,
            "extra_alien": None,
            "alien": None,
            "alien_laser": None,
        }
        self.block_groups = {
            "block": None,
        }
        self.powerup_groups = {
            "powerup": None,
        }
        self.player_groups = {
            "player": None,
            "player_laser": None,
        }
        self.g_groups = {
            **self.alien_groups,
            **self.block_groups,
            **self.powerup_groups,
            **self.player_groups,
        }

    def __getattr__(self, item):
        try:
            return self.g_groups[item]
        except KeyError:
            raise AttributeError(f"No Group called '{item}'")
