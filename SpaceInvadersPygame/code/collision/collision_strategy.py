import itertools
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Union

from collision.collision_layers import ObjectLayer
from game_attributes import GameAttributes
from game_groups import GameGroups
from game_objects.game_object import GameObject
from game_types import Group, Groups, GroupSingle, GroupUnion
from pygame import sprite


class CollisionStrategy(ABC):
    @abstractmethod
    def handle_collision(self, first: GroupUnion, second: GroupUnion):
        pass

    @staticmethod
    def sprite_layer_collided(sprite1: GameObject, sprite2: GameObject) -> bool:
        sprite1_layers = sprite1.collision_layers
        sprite2_layers = sprite2.collision_layers
        return sprite1_layers.can_collide(sprite2_layers) and sprite.collide_rect(
            sprite1, sprite2
        )


class PlayerAlienCollision(CollisionStrategy):
    """Player collides with an alien."""

    def handle_collision(self, player: GroupSingle, aliens: Group) -> bool:
        collided_aliens = sprite.spritecollide(
            player.sprite, aliens, dokill=True, collided=self.sprite_layer_collided
        )

        if collided_aliens:
            player.sprite.lives -= 1


class PlayerLaserCollision(CollisionStrategy):
    """Player collides with a laser."""

    def handle_collision(self, player: GroupSingle, lasers: Group) -> bool:
        kill_lasers_on_collision = (
            ObjectLayer.ALIEN_LASER in player.sprite.collision_layers
        )

        collided_lasers = sprite.spritecollide(
            player.sprite,
            lasers,
            dokill=kill_lasers_on_collision,
            collided=self.sprite_layer_collided,
        )
        if collided_lasers and player.sprite.immunity < 0:
            player.sprite.lives -= 1


class AlienLaserCollision(CollisionStrategy):
    """Alien collides with a laser."""

    def handle_collision(self, aliens: Group, lasers: Group) -> int:
        collided_aliens = sprite.groupcollide(
            aliens,
            lasers,
            dokilla=True,
            dokillb=True,
            collided=self.sprite_layer_collided,
        )

        points = self.get_alien_points(collided_aliens)
        GameAttributes().scoreboard.update_score(points)

    @staticmethod
    def get_alien_points(collided_aliens: Dict):
        return sum(alien.score_points for alien in collided_aliens)


class BlockLaserCollision(CollisionStrategy):
    """Alien collides with a laser."""

    def handle_collision(self, blocks: Group, lasers: Group) -> None:
        sprite.groupcollide(
            blocks,
            lasers,
            dokilla=True,
            dokillb=True,
            collided=self.sprite_layer_collided,
        )


class BlockAlienCollision(CollisionStrategy):
    """Block collides with an alien."""

    def handle_collision(self, blocks: Group, aliens: Group) -> None:
        sprite.groupcollide(
            aliens,
            blocks,
            dokilla=True,
            dokillb=True,
            collided=self.sprite_layer_collided,
        )


class PowerupLaserCollision(CollisionStrategy):
    """Powerup collides with a Laser."""

    def handle_collision(self, powerups: Group, lasers: Group) -> None:
        powerups_collided = sprite.groupcollide(
            powerups,
            lasers,
            dokilla=True,
            dokillb=True,
            collided=self.sprite_layer_collided,
        )

        player = GameGroups().player.sprite
        for powerups in powerups_collided:
            powerups.upgrade(player)


class BoundaryCollision:
    def handle_collision(
        self, group: Union[GroupUnion, GameObject]
    ) -> Optional[List[int]]:
        if isinstance(group, GameObject):
            return self.check_collision(group)

        for element in group.sprites():
            collision_result = self.check_collision(element)
            if collision_result:
                return collision_result

        return None

    def check_collision(self, obj) -> Optional[List[int]]:
        if obj.rect.right >= GameAttributes().screen_width or obj.rect.left <= 0:
            return [-1, 1]
        elif obj.rect.bottom >= GameAttributes().screen_height or obj.rect.top <= 0:
            return [1, -1]
        return None


class CollisionHandler:
    def __init__(self, groups: Groups) -> None:
        self.class_collision_dict = {
            ("Block", "Alien"): BlockAlienCollision(),
            ("Block", "Laser"): BlockLaserCollision(),
            ("Alien", "Laser"): AlienLaserCollision(),
            ("Player", "Laser"): PlayerLaserCollision(),
            ("Player", "Alien"): PlayerAlienCollision(),
            ("Powerup", "Laser"): PowerupLaserCollision(),
        }
        self.groups = groups

    def get_sprite_class(self, group: GroupUnion) -> Union[str, None]:
        if isinstance(group, GroupSingle):
            game_object = group.sprite if group.sprite else None
        elif isinstance(group, Group):
            game_object = group.sprites()[0] if group.sprites() else None
        if game_object:
            return game_object.collision_layers.object_name

    def handle_collisions(self) -> None:
        non_empty_groups = [group for group in self.groups if len(group) > 0]
        for group1, group2 in itertools.combinations(non_empty_groups, 2):
            class1 = self.get_sprite_class(group1)
            class2 = self.get_sprite_class(group2)
            self.process_collision((class1, class2), (group1, group2), symmetric=True)

    def process_collision(
        self,
        class_pair: Tuple[GroupUnion],
        group_pair: Tuple[GroupUnion],
        symmetric: bool,
    ) -> None:
        strategy: CollisionStrategy = self.class_collision_dict.get(class_pair)
        if strategy:
            strategy.handle_collision(*group_pair)
        elif symmetric:
            self.process_collision(class_pair[::-1], group_pair[::-1], symmetric=False)
