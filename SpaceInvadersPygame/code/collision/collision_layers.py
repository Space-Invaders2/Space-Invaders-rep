from enum import IntEnum
from typing import List


class ObjectLayer(IntEnum):
    # @staticmethod
    def bitmask(shift):
        return 1 << shift

    UNDEFINED = -1
    PLAYER = bitmask(0)
    ALIEN = bitmask(1)
    PLAYER_LASER = bitmask(2)
    ALIEN_LASER = bitmask(3)
    BLOCK = bitmask(4)
    POWERUP = bitmask(5)


class CollisionLayers:
    def __init__(
        self,
        object_name: str = None,
        object_layer: ObjectLayer = ObjectLayer.UNDEFINED,
        collidable_layers: List[ObjectLayer] = [],
    ):
        self.object_name = object_name
        self._object_layer = object_layer
        self._collidable_layers = sum(collidable_layers)

    def can_collide(self, other: "CollisionLayers") -> bool:
        """Check if two objects can collide based on their bitmask layers."""
        return ((self._object_layer & other._collidable_layers) != 0) or (
            (other._object_layer & self._collidable_layers)
        ) != 0

    @property
    def object_layer(self) -> ObjectLayer:
        return self._object_layer

    def __contains__(self, item):
        return item & self._collidable_layers
