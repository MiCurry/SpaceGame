import os
from pathlib import Path

import arcade

from SpaceGame.menus.main_menu import MainMenu
from SpaceGame.settings import SCREEN_WIDTH, SCREEN_HEIGHT

def add_resource_handlers():
    resource_dir = os.path.join(Path(__file__).parent.resolve(), "resources")
    arcade.resources.add_resource_handle("sprites", resource_dir)

def do_main_menu():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Space Game", resizable=True, )
    main_menu = MainMenu()
    window.show_view(main_menu)
    arcade.run()


if __name__ == "__main__":
    add_resource_handlers()
    do_main_menu()
