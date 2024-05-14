import arcade
from SpaceGame.gametypes.PlayZoneTypes import Background

# Window settings
TITLE = "Space Game"
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000
SCREEN_SPLIT_WIDTH = SCREEN_WIDTH / 2.0

# Play Zone Settings
PLAY_ZONE = (4, 4)
BACKGROUND_COLOR = arcade.color.SPACE_CADET
BACKGROUND_IMAGE = "./resources/png/backgrounds/stars.png"
DEFAULT_BACKGROUND = Background(BACKGROUND_IMAGE,
                                1024,
                                1024,
                                1.0)

# Physics settings
GRAVITY = 0.0
DEFAULT_DAMPING = 1.0

# Ship Physics and properties
SHIP_STARTING_HITPOINTS = 5
SHIP_SCALING = 0.5
SHIP_MASS = 1.0
SHIP_FRICTION = 0.0
SHIP_ELASTICITY = 0.1
SHIP_DAMPING = 1.0

# Player settings
PLAYER_ONE = 0
PLAYER_TWO = 1
ALIVE = True
DEAD = False

# Ship controls settings
CONTROLLER = 'controller'
KEYBOARD = 'keyboard'
ROTATION_SPEED = 0.05
KEYBOARD_THRUSTER_FORCE = 200.0
KEYBOARD_ROTATION_FORCE = 0.05
MOVEMENT_SPEED = 500.0
DEAD_ZONE_LEFT_STICK = 0.05
DEAD_ZONE_RIGHT_STICK = 0.1
