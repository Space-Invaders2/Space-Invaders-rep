from collision.collision_layers import CollisionLayers, ObjectLayer
from design.change_design import ComponentToBeUpdated, Visitor
from game_objects.game_object import GameObject
from game_types import Color, Position
from pygame import Surface


class Block(GameObject, ComponentToBeUpdated):
    def __init__(self, size: int, color: Color, pos: Position):
        super().__init__(
            collision_layers=CollisionLayers(
                object_name="Block",
                object_layer=ObjectLayer.BLOCK,
                collidable_layers=[
                    ObjectLayer.ALIEN,
                    ObjectLayer.PLAYER_LASER,
                    ObjectLayer.ALIEN_LASER,
                ],
            )
        )

        self.image = Surface((size, size))
        self.image.fill(color)
        self.pos = pos
        self.rect = self.image.get_rect(topleft=pos)

    def accept(self, visitor: Visitor):
        return visitor.change_block_colour(self)


class ObstacleShape:
    def __init__(self):
        self.shape_1 = [
            "  XXXXXXX  ",
            " XXXXXXXXX ",
            "XXXXXXXXXXX",
        ]

        self.shape_2 = [
            "    X    ",
            "   XXX   ",
            "  XXXXX  ",
            " XXXXXXX ",
        ]

        self.shape_3 = [
            "XXXXXXXXX",
            " XXXXXXX ",
            "  XXXXX  ",
            "   XXX   ",
            "    X    ",
        ]

        self.shape_4 = [
            "      X     ",
            "            ",
            "    X X X    ",
            "            ",
            "  X X X X X  ",
            "            ",
            "X X X X X X X",
            "            ",
            "  X X X X X  ",
            "            ",
            "    X X X    ",
            "            ",
            "      X      ",
        ]

        self.shape_5 = [
            "     X    ",
            "    XXX   ",
            "   XXXXX  ",
            "    XXX   ",
            "     X    ",
        ]

        self.shape_6 = [
            "  XXX   XXX  ",
            " XXXXX XXXXX ",
            "XXXXXXXXXXXXX",
            " XXXXXXXXXXX ",
            "  XXXXXXXXXX ",
            "   XXXXXXXX  ",
            "    XXXXXX   ",
            "     XXXX    ",
            "      XX     ",
        ]

        self.shape_7 = [
            "      XX     ",
            "     XXXX    ",
            "    XXXXXX   ",
            "   XXXXXXXX  ",
            "  XXXXXXXXXX ",
            "XXXXXXXXXXXXX",
            " XXXXX XXXXX ",
            "  XXX   XXX  ",
        ]

        self.shape_8 = [
            "XX     XXXXX     XXXXX     XXXXX     XXXXX     XXXXX     XXXXX  ",
            "  XXXXX     XXXXX     XXXXX     XXXXX     XXXXX     XXXXX     XX",
        ]

        self.powerup_shell = [
            "XXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXX",
            "XX             XX",
            "XX             XX",
            "XX             XX",
            "XX             XX",
            "XX             XX",
            "XX             XX",
            "XX             XX",
            "XX             XX",
            "XX             XX",
            "XX             XX",
            "XX             XX",
            "XXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXX",
        ]

        self.shape_9 = [
            " XX      XX ",
            " XX      XX ",
            "            ",
            "            ",
            "            ",
            "            ",
            "XX        XX",
            " XX      XX ",
            "  XXX  XXX  ",
            "   XXXXXX   ",
        ]

        self.shape_10 = [
            " XX      XX ",
            " XX      XX ",
            "            ",
            "            ",
            "            ",
            "            ",
            "   XXXXXX   ",
            "  XXX  XXX  ",
            " XX      XX ",
            "XX        XX",
        ]

        self.shape_11 = [
            " XX      XX ",
            " XX      XX ",
            "            ",
            "            ",
            "            ",
            "            ",
            "            ",
            "XXXXXXXXXXXX",
            "XXXXXXXXXXXX",
        ]

        self.shape_12 = [
            "  XX      XX  ",
            "   XX    XX   ",
            "   XX    XX   ",
            "    XX  XX    ",
            "     XXXX     ",
            "    XX  XX    ",
            "   XX    XX   ",
            "   XX    XX   ",
            "  XX      XX  ",
        ]

        self.shape_13 = [
            "  X     X  ",
            "  XX    XX ",
            " XXXX  XXXX ",
            "  XXX  XXX  ",
            "   X    X   ",
            "  XXX  XXX  ",
            " XXXX  XXXX ",
            "  XX    XX ",
            "  X     X  ",
        ]

        self.shape_14 = [
            "XXXXXXXXX",
            "X       X",
            "X  XXX  X",
            "X   X   X",
            "X  XXX  X",
            "X X X X X",
            "X X X X X",
            "X       X",
            "XXXXXXXXX",
        ]
