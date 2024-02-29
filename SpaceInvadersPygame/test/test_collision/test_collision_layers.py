import pytest
from collision.collision_layers import CollisionLayers, ObjectLayer

obj_layer_values = [
    (0, 1),
    (1, 0),
    (1, 2),
    (2, 1),
    (2, 3),
    (3, 2),
    (15, 30),
    (30, 15),
]

obj_layers_bitmasks = [
    (ObjectLayer.bitmask(val[0]), ObjectLayer.bitmask(val[1]))
    for val in obj_layer_values
]


@pytest.mark.parametrize("obj1_layer, obj2_layer", obj_layers_bitmasks)
class TestCollisionLayers:
    def test_empty_collision(self, obj1_layer, obj2_layer):
        coll_layer1 = CollisionLayers(object_layer=obj1_layer, collidable_layers=[])
        coll_layer2 = CollisionLayers(object_layer=obj2_layer, collidable_layers=[])
        assert (
            coll_layer1.can_collide(coll_layer2)
            and coll_layer2.can_collide(coll_layer1)
        ) == False

    def test_one_side_collision(self, obj1_layer, obj2_layer):
        coll_layer1 = CollisionLayers(
            object_layer=obj1_layer, collidable_layers=[obj2_layer]
        )
        coll_layer2 = CollisionLayers(object_layer=obj2_layer, collidable_layers=[])
        assert (
            coll_layer1.can_collide(coll_layer2)
            and coll_layer2.can_collide(coll_layer1)
        ) == True

    def test_both_sides_collision(self, obj1_layer, obj2_layer):
        coll_layer1 = CollisionLayers(
            object_layer=obj1_layer, collidable_layers=[obj2_layer]
        )
        coll_layer2 = CollisionLayers(
            object_layer=obj2_layer, collidable_layers=[obj1_layer]
        )
        assert (
            coll_layer1.can_collide(coll_layer2)
            and coll_layer2.can_collide(coll_layer1)
        ) == True

    @pytest.mark.parametrize(
        "left_collidable_range, right_collidable_range",
        [
            (
                [ObjectLayer.bitmask(i) for i in range(0, 5)],
                [ObjectLayer.bitmask(i) for i in range(5, 10)],
            ),  # Disjoint ranges
            (
                [ObjectLayer.bitmask(i) for i in range(0, 6)],
                [ObjectLayer.bitmask(i) for i in range(4, 10)],
            ),  # Somewhat disjoint ranges
            (
                [ObjectLayer.bitmask(i) for i in range(1, 10)],
                [ObjectLayer.bitmask(i) for i in range(1, 10)],
            ),  # Completely intersecting ranges
        ],
    )
    def test_multilayer_empty_collision(
        self, obj1_layer, obj2_layer, left_collidable_range, right_collidable_range
    ):
        left_collidable_layers = [x for x in left_collidable_range if x != obj2_layer]
        right_collidable_layers = [x for x in right_collidable_range if x != obj1_layer]
        coll_layer1 = CollisionLayers(
            object_layer=obj1_layer, collidable_layers=left_collidable_layers
        )
        coll_layer2 = CollisionLayers(
            object_layer=obj2_layer, collidable_layers=right_collidable_layers
        )
        assert (
            coll_layer1.can_collide(coll_layer2)
            and coll_layer2.can_collide(coll_layer1)
        ) == False

    @pytest.mark.parametrize(
        "collidable_range",
        [
            ([ObjectLayer.bitmask(i) for i in range(0, 10, 1)]),  # Simple range
            ([ObjectLayer.bitmask(i) for i in range(0, 10, 3)]),  # Step range
            ([ObjectLayer.bitmask(i) for i in range(2, 10, -1)]),  # Inverse range
        ],
    )
    def test_multilayer_one_side_collision(
        self, obj1_layer, obj2_layer, collidable_range
    ):
        one_side_collidable_layers = [
            x for x in collidable_range if x != obj2_layer
        ] + [obj2_layer]

        coll_layer1 = CollisionLayers(
            object_layer=obj1_layer, collidable_layers=one_side_collidable_layers
        )
        coll_layer2 = CollisionLayers(object_layer=obj2_layer, collidable_layers=[])
        assert (
            coll_layer1.can_collide(coll_layer2)
            and coll_layer2.can_collide(coll_layer1)
        ) == True

    @pytest.mark.parametrize(
        "left_collidable_range, right_collidable_range",
        [
            (
                [ObjectLayer.bitmask(i) for i in range(0, 5)],
                [ObjectLayer.bitmask(i) for i in range(5, 10)],
            ),  # Disjoint ranges
            (
                [ObjectLayer.bitmask(i) for i in range(0, 6)],
                [ObjectLayer.bitmask(i) for i in range(4, 10)],
            ),  # Somewhat disjoint ranges
            (
                [ObjectLayer.bitmask(i) for i in range(1, 10)],
                [ObjectLayer.bitmask(i) for i in range(1, 10)],
            ),  # Completely intersecting ranges
        ],
    )
    def test_multilayer_both_sides_collision(
        self, obj1_layer, obj2_layer, left_collidable_range, right_collidable_range
    ):
        right_collidable_layers = [
            x for x in right_collidable_range if x != obj1_layer
        ] + [obj1_layer]
        left_collidable_layers = [
            x for x in left_collidable_range if x != obj2_layer
        ] + [obj2_layer]

        coll_layer1 = CollisionLayers(
            object_layer=obj1_layer, collidable_layers=left_collidable_layers
        )
        coll_layer2 = CollisionLayers(
            object_layer=obj2_layer, collidable_layers=right_collidable_layers
        )
        assert (
            coll_layer1.can_collide(coll_layer2)
            and coll_layer2.can_collide(coll_layer1)
        ) == True
