import arcade

from SpaceGame.gamemodes.pvp import PvpGame
from SpaceGame.menus.main_menu import MainMenu
from SpaceGame.settings import SCREEN_WIDTH, SCREEN_HEIGHT

import argparse


def do_main_menu():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Space Game", resizable=True, )
    main_menu = MainMenu()
    main_menu.setup()
    window.show_view(main_menu)
    arcade.run()

def do_pvp():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Space Game", resizable=True, )
    game = PvpGame()
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    argparse = argparse.ArgumentParser(description="Space game CLI Runner")
    argparse.add_argument('view',
                          help="Options are: main, pvp",
                          type=str)

    args = argparse.parse_args()

    if args.view == "main":
        do_main_menu()
    elif args.view == "pvp":
        do_pvp()
    else:
        print(f"Did not understand: {args.view}. Choices are: 'main', 'pvp'")



