import pygame
from config import ConfigDev
from design.graphics import ClassicDesignFactory


class Scoreboard:
    def __init__(self, score=0, design=ClassicDesignFactory()):
        self.score = score
        self.design = design

        self.config = ConfigDev()
        self.font = self.design.get_font()
        self.off_set = self.config.get_option_dev("offset", "display_score")

    def update_score(self, points: int) -> None:
        self.score += points

    def display_score(self, screen: pygame.display) -> None:
        score_surf = self.font.render(f"score: {self.score}", False, "white")
        score_rect = score_surf.get_rect(topleft=self.off_set)
        screen.blit(score_surf, score_rect)
