import json
from os import path

DEV_FILE = "dev.json"


class Screen:
    def __init__(self, width, height):
        self.height = height
        self.width = width


class Volumes:
    def __init__(self, sounds, music, laser, explosion):
        self.music = music
        self.sounds = sounds
        self.laser = laser
        self.laser_max = laser
        self.explosion = explosion
        self.explosion_max = explosion
        self.music_on = True
        self.sound_on = True


class Speed:
    def __init__(self, player, alien, extra_alien):
        self.player = player
        self.alien = alien
        self.extra_alien = extra_alien


class Points:
    def __init__(self, red, green, yellow, extra):
        self.red = red
        self.green = green
        self.yellow = yellow
        self.extra = extra


class AlienPositions:
    def __init__(self, rows, cols, x_distance, y_distance, x_offset, y_offset):
        self.rows = rows
        self.cols = cols
        self.x_distance = x_distance
        self.y_distance = y_distance
        self.x_offset = x_offset
        self.y_offset = y_offset


class Config(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ConfigDev(metaclass=Config):
    current_directory = path.dirname(path.abspath(__file__))
    _CONFIG_PATH = path.join(current_directory, "..", "config", "dev_1.json")
    _DATA = None

    def __init__(self, config_path=None):
        if config_path is not None:
            self._CONFIG_PATH = config_path
        with open(self._CONFIG_PATH, "r") as f:
            self._DATA = json.load(f)

        self.screen = Screen(
            self._DATA["screen"]["width"], self._DATA["screen"]["height"]
        )
        self.volumes = Volumes(
            self._DATA["volumes"]["music"],
            self._DATA["volumes"]["sounds"],
            self._DATA["volumes"]["laser_max"],
            self._DATA["volumes"]["explosion_max"],
        )
        self.speeds = Speed(
            self._DATA["speeds"]["player"],
            self._DATA["speeds"]["aliens"],
            self._DATA["speeds"]["extra_alien"],
        )
        self.points = Points(
            self._DATA["points"]["red"],
            self._DATA["points"]["green"],
            self._DATA["points"]["yellow"],
            self._DATA["points"]["extra"],
        )
        self.alien_positions = AlienPositions(
            self._DATA["aliens"]["rows"],
            self._DATA["aliens"]["cols"],
            self._DATA["aliens"]["x_distance"],
            self._DATA["aliens"]["y_distance"],
            self._DATA["aliens"]["x_offset"],
            self._DATA["aliens"]["y_offset"],
        )

    def get_option_dev(self, *keys):
        config_value = self._DATA
        for key in keys:
            config_value = config_value[key]
            if config_value is None:
                return None
        return config_value


class ConfigUser(metaclass=Config):
    _CONFIG_PATH = "./config/user.json"
    _DATA = None

    def __init__(self, config_path=None):
        if config_path is not None:
            self._CONFIG_PATH = config_path
        with open(self._CONFIG_PATH, "r") as f:
            self._DATA = json.load(f)

    def get_option_user(self):
        return self._DATA["user1"]
