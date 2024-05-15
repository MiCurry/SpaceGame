import arcade

from SpaceGame.gamemodes.pvp import PvPGame
from SpaceGame.settings import SCREEN_WIDTH, SCREEN_HEIGHT

if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Space Game", resizable=True, )
    game = PvPGame()
    game.setup()
    window.show_view(game)
    arcade.run()
