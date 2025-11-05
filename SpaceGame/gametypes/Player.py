from dataclasses import dataclass
import json
import os
from typing import Optional, Tuple

from SpaceGame.scoreboard.scoreboard import Score, TotalPlayerStats
import arcade

from arcade.types import Color
from pymunk.vec2d import Vec2d
import pyglet.input
from arcade.future.input.manager import ActionState
from pyglet import clock

from SpaceGame.controls import Controller
from SpaceGame.gametypes.InputManager import InputManager
from SpaceGame.gametypes.Ship import Ship, ShipData
from SpaceGame.settings import CONTROLLER, KEYBOARD, ALIVE, PLAYER_DIRECTORY, Setting
from SpaceGame.shared.timer import TimerManager

RESPAWN_TIMER = "respawn"

NO_DAMPING = {'name' : 'Damping: Off',
                 'value' : 1}

LOW_DAMPING = {'name' : 'Damping: Low',
                 'value' : 1.005}
            
MEDIUM_DAMPING = {'name' : 'Damping: Med',
                 'value' : 1.025}

HIGH_DAMPING = {'name' : 'Damping: High',
                 'value' : 1.040}

PLAYER_DAMPING_LEVELS = [NO_DAMPING, LOW_DAMPING, MEDIUM_DAMPING, HIGH_DAMPING]

TEXT_FADE_INT = 3

PLAYER_DIRECTORY = os.path.join('./data', 'players')

@dataclass
class PlayerData:
    name : str
    shipSprite : str
    shipData : ShipData
    playerScore : Score
    playerStats : TotalPlayerStats

def player_file_exists(player_name) -> bool:
    return os.path.isfile(os.path.join(PLAYER_DIRECTORY, player_name))

def load_player(player_name) -> PlayerData:
    pass

def make_new_player(player_name, sprite_file=':sprites:png/sprites/Ships/playerShip1_blue.png') -> PlayerData:
    shipData = ShipData(
        sprite=sprite_file,
        status=ALIVE,
        hitpoints=0,
        mass=0,
        friction=0,
        elasticity=0,
        scaling=0,
        movement_speed=0,
        rotation_speed=0
    )

    playerScore = Score(
        kills=0,
        score=0,
        deaths=0,
        space_junk_blown_up=0,
        ufo_deaths=0,
        shots_fired=0,
        shots_hit=0,
        accuracy=0.0,
        kd=0.0,
        distance_flown=0,
        highest_speed=0
    )
    
    playerStats = TotalPlayerStats(
        total_score=0,
        highest_score=0,
        total_space_junk_blown_up=0,
        highest_space_junk_blown_up=0,
        highest_kills=0,
        highest_deaths=0,
        kills=0,
        deaths=0,
        kd_ratio=0.0,
        ufo_deaths=0,
        shots_fired=0,
        shots_hit=0,
        accuracy=0.0,
        distance_traveled=0
        )

    playerData = PlayerData(
        name=player_name,
        shipSprite=sprite_file,
        shipData=shipData,
        playerScore=playerScore,
        playerStats=playerStats
    )

    return Player(
        main=None,
        player_name=player_name,
        playerData=playerData,
        start_position=Vec2d(0,0),
        player_number=0,
        input_source=None,
        status=ALIVE,
        lives=-1
    )




class Player(Ship):
    def __str__(self):
        return f"Player: {self.player_number} - {self.player_name}"

    def __init__(self, main, player_name,
                 playerData : PlayerData,
                 start_position: Tuple,
                 player_number=0,
                 input_source=CONTROLLER,
                 status=ALIVE,
                 lives=-1,
                 ):

        self._damping_idx = 0

        self._playerData : PlayerData = playerData
        print(self._playerData.shipData.sprite)
        self.player_name = player_name
        self.input_source = input_source
        self.controller = None
        self.player_number = player_number
        self.do_draw_text = False

        self.w_pressed = 0.0
        self.s_pressed = 0.0
        self.a_pressed = 0.0
        self.d_pressed = 0.0
        self.left_pressed = 0.0
        self.right_pressed = 0.0
        self.last_hit_buy = None

        print("Player Ship Data: ", self._playerData.shipData)

        self.lives = lives

        super().__init__(main,
                         start_position,
                         self._playerData.shipData
                         )

        self.timers = TimerManager()

    def register_with_settings(self):
        super().register_with_settings()
        self._register_handle('ROTATION_SPEED')
        self._register_handle('MOVEMENT_SPEED')

    def _register_handle(self, setting_name : str):
        setting : Setting = self.main.settings.get(setting_name)
        setting.register_handle(self.signal_handler)

    def signal_handler(self, setting : Setting):
        super().signal_handler(setting)

        if setting.name == 'ROTATION_SPEED':
            self.rotation_speed = setting.value
        elif setting.name == 'MOVEMENT_SPEED':
            self.movement_speed = setting.value

    def setup(self):
        super().setup()
        self.damping_text = arcade.Text(
            text=f"Damping Text",
            x=self.position[0],
            y=self.position[1],
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x='center'
        )
        self.register_with_settings()
        self.input_manager = InputManager(self.input_source, action_handler=self.on_action)

    def apply_angle_damping(self):
        self.body.angular_velocity /= 1.05

    def apply_x_vel_damping(self):
        self.body.velocity = Vec2d(self.body.velocity.x / PLAYER_DAMPING_LEVELS[self._damping_idx]['value'],
                    self.body.velocity.y)

    def apply_y_vel_damping(self):
        self.body.velocity = Vec2d(self.body.velocity.x,
                    self.body.velocity.y / PLAYER_DAMPING_LEVELS[self._damping_idx]['value'])

    def update(self, delta_t: float):
        self.input_manager.on_update()
        super().update(delta_t=delta_t)

        if RESPAWN_TIMER in self.timers.get_elapsed():
            self.timers.clear_elapsed(RESPAWN_TIMER)
            self.respawn()

        if self.applied_rotational_vel == 0.0:
            self.apply_angle_damping()

        dx = self.input_manager.input_manager.axis('left_right') * self.movement_speed
        dy = self.input_manager.input_manager.axis('up_down') * self.movement_speed


        if dx == 0.0:
            self.apply_x_vel_damping()

        if dy == 0.0:
            self.apply_y_vel_damping()

        self.damping_text.position = (self.position[0], self.position[1] - 50)

        self.applied_rotational_vel = self.input_manager.input_manager.axis('rotate') * self.rotation_speed

        self.body.angular_velocity += self.applied_rotational_vel
        self.body.apply_force_at_world_point((dx, -dy), (self.center_x, self.center_y))

    def draw_damping_level(self):
        color = self.damping_text.color
        r = color[0]; g = color[1]; b = color[2]
        a = color[3] - TEXT_FADE_INT

        if a < 0:
            a = 0
            self.do_draw_text = False

        self.damping_text.color = Color(r, g, b, a)

        if self.do_draw_text:
            self.damping_text.draw()

    def draw(self):
        self.draw_damping_level()

    def update_damping_text(self):
        self.damping_text.text = f"{PLAYER_DAMPING_LEVELS[self._damping_idx]['name']}"
        
    def dampining_up(self):
        if self._damping_idx == len(PLAYER_DAMPING_LEVELS) - 1:
            self._damping_idx = 0
        else:
            self._damping_idx += 1

        self.damping_text.color = arcade.color.WHITE
        self.update_damping_text()
        self.do_draw_text = True

    def damping_down(self):
        if self._damping_idx == 0:
            self._damping_idx = len(PLAYER_DAMPING_LEVELS) - 1 
        else:
            self._damping_idx -= 1

        self.damping_text.color = arcade.color.WHITE
        self.update_damping_text()
        self.do_draw_text = True

    def on_action(self, action: str, state: ActionState):
        if action == 'shoot' and state == ActionState.PRESSED:
            self.shoot()
        elif action == 'damping_up' and state == ActionState.PRESSED:
            self.dampining_up()
        elif action == 'damping_down' and state == ActionState.PRESSED:
            self.damping_down()

    def explode(self):
        super().explode()

        if self.last_hit_buy == "UFO":
            self.main.scoreboard.add_ufo_death(self.player_number)
        else:
            self.main.scoreboard.add_kill(self.last_hit_buy, self)
            self.main.scoreboard.add_death(self.player_number)

        self.lives -= 1
        self.timers.add(RESPAWN_TIMER, 5)

def get_player_or_make_new_one(player_name) -> PlayerData:
    if player_file_exists(player_name):
        return load_player(player_name) 
    else:
        return make_new_player(player_name)