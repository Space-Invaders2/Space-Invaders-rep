from abc import ABC, abstractmethod
from os import path
from random import randint

import pygame
from config import ConfigDev


class AbstractDesignFactory(ABC):
    def __init__(self):
        pygame.init()
        self.design_name = None
        self.config = ConfigDev()

    pygame.mixer.init()
    laser_sound = pygame.mixer.Sound(
        path.join(
            path.dirname(path.abspath(__file__)), "..", "..", "audio", "laser.mp3"
        )
    )
    explosion_sound = pygame.mixer.Sound(
        path.join(
            path.dirname(path.abspath(__file__)),
            "..",
            "..",
            "audio",
            "explosion.mp3",
        )
    )

    def get_player_image(self) -> pygame.image:
        pass

    @abstractmethod
    def get_alien_image(colour) -> pygame.image:
        pass

    @abstractmethod
    def get_powerup_image(type) -> pygame.image:
        pass

    @abstractmethod
    def get_font() -> pygame.font.Font:
        pass

    @abstractmethod
    def get_music() -> pygame.mixer.Sound:
        pass

    @abstractmethod
    def get_block_colour():
        pass

    @abstractmethod
    def get_boss_image() -> pygame.image:
        pass


class ClassicDesignFactory(AbstractDesignFactory):
    def __init__(self):
        super().__init__()
        self.design_name = "classic"

        self.current_directory = path.dirname(path.abspath(__file__))
        self._IMG_PATH = path.join(
            self.current_directory, "..", "..", "graphics", self.design_name
        )

    def get_player_image(self):
        return pygame.image.load(
            path.join(
                path.join(
                    self.current_directory, "..", "..", "graphics", self.design_name
                ),
                "player.png",
            )
        )

    def get_powerup_image(self, type) -> pygame.image:
        if type == "life":
            return pygame.image.load(path.join(self._IMG_PATH, "powerup_life.png"))
        elif type == "immunity":
            return pygame.image.load(path.join(self._IMG_PATH, "powerup_immunity.png"))
        elif type == "beam":
            return pygame.image.load(path.join(self._IMG_PATH, "powerup_beam.png"))
        elif type == "multi":
            return pygame.image.load(path.join(self._IMG_PATH, "powerup_multi.png"))
        elif type == "delayed":
            return pygame.image.load(path.join(self._IMG_PATH, "powerup_delayed.png"))

    def get_alien_image(self, colour):
        if colour == "green":
            return pygame.image.load(path.join(self._IMG_PATH, "green.png"))
        elif colour == "red":
            return pygame.image.load(path.join(self._IMG_PATH, "red.png"))
        elif colour == "yellow":
            return pygame.image.load(path.join(self._IMG_PATH, "yellow.png"))
        elif colour == "extra":
            return pygame.image.load(path.join(self._IMG_PATH, "extra.png"))
        else:
            pass

    def get_boss_image(self) -> pygame.Surface:
        graphics_path = path.join(
            self.current_directory, "..", "..", "graphics", self.design_name
        )
        return pygame.image.load(path.join(graphics_path, "boss.png"))

    def get_font(self) -> pygame.font.Font:
        return pygame.font.Font(
            path.join(self.current_directory, "..", "..", "font", "Pixeled.ttf"), 20
        )

    def get_music(self):
        pygame.mixer.music.load(
            path.join(self.current_directory, "..", "..", "audio", "music.wav")
        )
        pygame.mixer.music.play(-1)

    def get_block_colour(self):
        return self.config.get_option_dev("colour", "red")


class ModernDesignFactory(AbstractDesignFactory):
    def __init__(self):
        super().__init__()
        self.design_name = "modern"

        self.current_directory = path.dirname(path.abspath(__file__))
        self._IMG_PATH = path.join(
            self.current_directory, "..", "..", "graphics", self.design_name
        )

    def get_player_image(self):
        return pygame.image.load(
            path.join(
                path.join(
                    self.current_directory, "..", "..", "graphics", self.design_name
                ),
                "player.png",
            )
        )

    def get_powerup_image(self, type) -> pygame.image:
        if type == "life":
            return pygame.image.load(path.join(self._IMG_PATH, "powerup_life.png"))
        elif type == "immunity":
            return pygame.image.load(path.join(self._IMG_PATH, "powerup_immunity.png"))
        elif type == "beam":
            return pygame.image.load(path.join(self._IMG_PATH, "powerup_beam.png"))
        elif type == "multi":
            return pygame.image.load(path.join(self._IMG_PATH, "powerup_multi.png"))
        elif type == "delayed":
            return pygame.image.load(path.join(self._IMG_PATH, "powerup_delayed.png"))

    def get_alien_image(self, colour):
        if colour == "green":
            return pygame.image.load(path.join(self._IMG_PATH, "green.png"))
        elif colour == "red":
            return pygame.image.load(path.join(self._IMG_PATH, "red.png"))
        elif colour == "yellow":
            return pygame.image.load(path.join(self._IMG_PATH, "yellow.png"))
        elif colour == "extra":
            return pygame.image.load(path.join(self._IMG_PATH, "extra.png"))
        else:
            pass

    def get_boss_image(self) -> pygame.Surface:
        graphics_path = path.join(
            self.current_directory, "..", "..", "graphics", self.design_name
        )
        return pygame.image.load(path.join(graphics_path, "boss.png"))

    def get_font(self) -> pygame.font.Font:
        return pygame.font.Font(
            path.join(self.current_directory, "..", "..", "font", "Pixeled.ttf"), 20
        )

    def get_music(self):
        pygame.mixer.music.load(
            path.join(self.current_directory, "..", "..", "audio", "modern.mp3")
        )
        pygame.mixer.music.play(-1)

    def get_block_colour(self):
        return self.config.get_option_dev("colour", "green")


class BlackWhiteDesignFactory(AbstractDesignFactory):
    def __init__(self):
        super().__init__()
        self.design_name = "black_white"
        self.current_directory = path.dirname(path.abspath(__file__))
        self._IMG_PATH = path.join(
            self.current_directory, "..", "..", "graphics", self.design_name
        )

    def get_player_image(self):
        return pygame.image.load(
            path.join(
                path.join(
                    self.current_directory, "..", "..", "graphics", self.design_name
                ),
                "player.png",
            )
        )

    def get_powerup_image(self, type) -> pygame.image:
        if type == "life":
            return pygame.image.load(path.join(self._IMG_PATH, "powerup_life.png"))
        elif type == "immunity":
            return pygame.image.load(path.join(self._IMG_PATH, "powerup_immunity.png"))
        elif type == "beam":
            return pygame.image.load(path.join(self._IMG_PATH, "powerup_beam.png"))
        elif type == "multi":
            return pygame.image.load(path.join(self._IMG_PATH, "powerup_multi.png"))
        elif type == "delayed":
            print("get_powerup_image called. elif type ==  delayed")
            return pygame.image.load(path.join(self._IMG_PATH, "powerup_delayed.png"))

    def get_alien_image(self, colour):
        if colour == "green":
            return pygame.image.load(path.join(self._IMG_PATH, "green.png"))
        elif colour == "red":
            return pygame.image.load(path.join(self._IMG_PATH, "red.png"))
        elif colour == "yellow":
            return pygame.image.load(path.join(self._IMG_PATH, "yellow.png"))
        elif colour == "extra":
            return pygame.image.load(path.join(self._IMG_PATH, "extra.png"))
        else:
            pass

    def get_boss_image(self) -> pygame.Surface:
        graphics_path = path.join(
            self.current_directory, "..", "..", "graphics", self.design_name
        )
        return pygame.image.load(path.join(graphics_path, "boss.png"))

    def get_font(self) -> pygame.font.Font:
        return pygame.font.Font(
            path.join(self.current_directory, "..", "..", "font", "Pixeled.ttf"), 20
        )

    def get_music(self):
        pygame.mixer.music.load(
            path.join(self.current_directory, "..", "..", "audio", "black_white.mp3")
        )
        pygame.mixer.music.play(-1)

    def get_block_colour(self):
        return self.config.get_option_dev("colour", "white")


class ChristmasDesignFactory(AbstractDesignFactory):
    def __init__(self):
        super().__init__()
        self.design_name = "christmas"
        self.current_directory = path.dirname(path.abspath(__file__))
        self._IMG_PATH = path.join(
            self.current_directory, "..", "..", "graphics", self.design_name
        )

    def get_player_image(self):
        return pygame.image.load(
            path.join(
                path.join(
                    self.current_directory, "..", "..", "graphics", self.design_name
                ),
                "player.png",
            )
        )

    def get_powerup_image(self, type) -> pygame.image:
        return pygame.image.load(path.join(self._IMG_PATH, f"powerup_{type}.png"))

    def get_alien_image(self, colour):
        return pygame.image.load(path.join(self._IMG_PATH, f"{colour}.png"))

    def get_boss_image(self) -> pygame.Surface:
        graphics_path = path.join(
            self.current_directory, "..", "..", "graphics", self.design_name
        )
        return pygame.image.load(path.join(graphics_path, "boss.png"))

    def get_font(self) -> pygame.font.Font:
        return pygame.font.Font(
            path.join(self.current_directory, "..", "..", "font", "Pixeled.ttf"), 20
        )

    def get_music(self):
        pygame.mixer.music.load(
            path.join(self.current_directory, "..", "..", "audio", "black_white.mp3")
        )
        pygame.mixer.music.play(-1)

    def get_block_colour(self):
        return self.config.get_option_dev("colour", "white")


class CRT:
    """Cathode-ray Tube"""

    def __init__(self, setup) -> None:
        self.setup = setup
        self.tv = pygame.image.load(
            path.join(
                path.dirname(path.abspath(__file__)),
                "..",
                "..",
                "graphics",
                "tv.png",
            )
        ).convert_alpha()
        self.tv = pygame.transform.scale(
            self.tv, (setup.screen_width, setup.screen_height)
        )

    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()
        self.setup.screen.blit(self.tv, (0, 0))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(self.setup.screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(
                self.tv, "black", (0, y_pos), (self.setup.screen_width, y_pos), 1
            )

    def fps_display(self, clock):
        font = pygame.font.Font(
            path.join(
                path.dirname(path.abspath(__file__)),
                "..",
                "..",
                "font",
                "Pixeled.ttf",
            ),
            16,
        )
        fps_text = font.render(f"FPS: {int(clock.get_fps())}", False, "grey")
        self.setup.screen.blit(fps_text, (self.setup.screen_width / 3, -8))

    def mouse_pos_display(self):
        font = pygame.font.Font(
            path.join(
                path.dirname(path.abspath(__file__)),
                "..",
                "..",
                "font",
                "Pixeled.ttf",
            ),
            16,
        )
        mouse_pos = pygame.mouse.get_pos()
        mouse_text = font.render(f"mouse pos: {mouse_pos}", False, "grey")
        self.setup.screen.blit(mouse_text, (self.setup.screen_width / 3, 20))

    def countdown_display(self, countdown):
        font = pygame.font.Font(
            path.join(
                path.dirname(path.abspath(__file__)),
                "..",
                "..",
                "font",
                "Pixeled.ttf",
            ),
            16,
        )
        countdown_text = font.render(f"Time: {countdown}", False, "grey")
        self.setup.screen.blit(countdown_text, (20, self.setup.screen_height - 36))
