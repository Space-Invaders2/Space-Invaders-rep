from abc import ABC, abstractmethod

import numpy as np
from pygame import sprite


class MoveStrategy(ABC):
    @staticmethod
    @abstractmethod
    def handle_move(entity, momentum):
        pass

    @staticmethod
    def update_position(entity, momentum):
        if isinstance(entity, type(sprite.Group())):
            for element in entity.sprites():
                MoveStrategy.pixel_movement(element, momentum)
            return
        else:
            MoveStrategy.pixel_movement(entity, momentum)

    @staticmethod
    def pixel_movement(obj, momentum):
        pos = np.asarray(obj.pos) + momentum
        obj.rect.x = pos[0]
        obj.rect.y = pos[1]
        obj.pos = pos
        # obj.rect.move_ip(momentum)


class Advance(MoveStrategy):
    @staticmethod
    def handle_move(entity, momentum=[0, 0]):
        MoveStrategy.update_position(entity, [0, 10])


class SimpleMove(MoveStrategy):
    def handle_move(entity, momentum):
        MoveStrategy.update_position(entity, momentum)


class NoMove(MoveStrategy):
    def handle_move(entity, momentum):
        print("nomove")


class MoveHandler:
    def __init__(self, groups):
        self.groups = groups

    def handle_moves(self):
        for group in self.groups:
            for element in group:
                element.action()
