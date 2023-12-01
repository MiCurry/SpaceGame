import arcade

DEFAULT_DEAD_ZONE = 0.05

CONTROLLER_RIGHT_BUMPER = 7 # The Right Bumper for A XB1 Controller

def do_we_haz_controller():
    return arcade.get_game_controllers()


def get_and_open_controller(controller_number=0):
    controller = arcade.get_game_controllers()[controller_number]
    controller.open()
    return controller


def register_controller_to_player(player):
    player.controller.push_handlers(player)


def add_controller_to_player(player):
    player.controller = get_and_open_controller(player.player_number)
    register_controller_to_player(player)

def remove_controller_from_player(player):
    player.controller.remove_handlers()

def apply_deadzone(v, dead_zone=DEFAULT_DEAD_ZONE):
    if abs(v) < dead_zone:
        return 0
    return v