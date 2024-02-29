import pygame
from collision.collision_layers import CollisionLayers
from game_attributes import GameAttributes
from pygame import sprite
from strategy.move_strategy import Advance, NoMove, SimpleMove


class GameObject(sprite.Sprite):
    def __init__(
        self,
        collision_layers: CollisionLayers = CollisionLayers(),
    ):
        super().__init__()

        self.move_behaviour = {
            "no_move": NoMove,
            "simple_move": SimpleMove,
            "advance": Advance,
        }
        self.momentum = [0, 0]
        self.pos = [0, 0]
        self.rect = pygame.Rect(self.pos, [0, 0])
        self.game_attributes = GameAttributes()
        self.config = self.game_attributes.config
        self.design = self.game_attributes.design
        self.collision_layers = collision_layers

    def move(self, move_pattern):
        self.move_behaviour[move_pattern].handle_move(self, self.momentum)

    def action(self):
        pass
