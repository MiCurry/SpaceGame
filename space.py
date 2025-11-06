import sys
import os
from pathlib import Path

import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(module)s:%(lineno)d: %(message)s',
                    level=logging.WARNING)

from SpaceGame.shared.player_helper import add_players_to_settings, load_player_names
import arcade

from SpaceGame.menus.main_menu import MainMenu
from SpaceGame.settings import SettingsManager 

VERSION = 'develop'

settings = SettingsManager()

def add_resource_handlers():
    resource_dir = os.path.join(Path(__file__).parent.resolve(), "resources")
    arcade.resources.add_resource_handle("sprites", resource_dir)

def do_main_menu():
    window = arcade.Window(settings['SCREEN_WIDTH'], settings["SCREEN_HEIGHT"], "Space Game", resizable=True, )
    main_menu = MainMenu(settings=settings)
    window.show_view(main_menu)
    arcade.run()


if __name__ == "__main__":
    logger = logging.getLogger('space_game')
    logger.setLevel(logging.DEBUG)
    logger.info(f"Starting Space Game Version: {VERSION}")

    add_players_to_settings(load_player_names(settings), settings)

    add_resource_handlers()
    do_main_menu()
