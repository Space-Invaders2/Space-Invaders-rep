from game_objects.game_object import GameObject


class Entity(GameObject):
    def __init__(self, gun=None, **kwargs):
        super().__init__(**kwargs)
        import strategy.gun as strat_gun

        self.gun = gun if gun else strat_gun.EmptyGun()
        self.direction = [0, 1]

    def shoot(self):
        self.gun.shoot(self.direction)

    def set_gun(self, gun):
        self.gun = gun
