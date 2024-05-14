import arcade

from SpaceGame.gamemodes.pvp import PvPGame

if __name__ == "__main__":
    window = PvPGame()
    window.setup()
    arcade.run()
