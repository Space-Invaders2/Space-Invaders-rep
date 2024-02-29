import pygame
from config import ConfigDev
from design.graphics import ClassicDesignFactory


class Scoreboard:
    def __init__(self, score=0, design=ClassicDesignFactory):
        self.score = score
        self.design = design

        self.config = ConfigDev()
        self.lives = self.config.get_option_dev("player", "lives")

        self.life_surface = self.design.get_player_image()
        self.font = self.design.get_font()
        self.off_set = self.config.get_option_dev("offset", "display_score")

    def update_score(self, points: int) -> None:
        self.score += points

    def display_lives(self, screen: pygame.Surface, player_lives: int) -> None:
        life_width = self.life_surface.get_size()[0]
        life_spacing = 10

        self.lives_x_start_pos = self.config.screen.width - (
            (life_width + life_spacing) * player_lives
        )
        for life in reversed(range(player_lives)):
            x = self.lives_x_start_pos + (life * (life_width + life_spacing))
            screen.blit(self.life_surface, (x, 8))

    def display_score(self, screen: pygame.display) -> None:
        score_surf = self.font.render(f"score: {self.score}", False, "white")
        score_rect = score_surf.get_rect(topleft=self.off_set)
        screen.blit(score_surf, score_rect)
