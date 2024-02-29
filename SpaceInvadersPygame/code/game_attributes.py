from config import ConfigDev
from design.graphics import AbstractDesignFactory, ClassicDesignFactory
from screens.highscore import Highscores
from screens.scoreboard import Scoreboard


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class GameAttributes(metaclass=SingletonMeta):
    def __init__(self, design: AbstractDesignFactory = ClassicDesignFactory()) -> None:
        self.config = ConfigDev()
        self.highscores = Highscores()
        self.scoreboard = Scoreboard()
        self.screen_width = self.config.get_option_dev("screen", "width")
        self.screen_height = self.config.get_option_dev("screen", "height")
        self.design = design
        self.level = 0
        self.difficulty = 2
