import sys

sys.path.append("../")  # noqa
from design.graphics import CRT
from game import Game, GameSetup
from screens.menu import MenuGroup

if __name__ == "__main__":
    setup = GameSetup()
    menu = MenuGroup()
    game = Game()

    crt = CRT(setup)

    while True:
        menu.check_menus(game, setup)
