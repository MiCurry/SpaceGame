from dataclasses import dataclass
import os

import logging
logger = logging.getLogger('space_game')

import json
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


def make_new_player(settings, player_name, sprite_file=':sprites:png/sprites/Ships/playerShip1_blue.png') -> PlayerData:
    shipData = ShipData(
        sprite=sprite_file,
        status=ALIVE,
        hitpoints=settings['SHIP_STARTING_HITPOINTS'],
        mass=settings['SHIP_MASS'],
        friction=settings['SHIP_FRICTION'],
        elasticity=settings['SHIP_ELASTICITY'],
        scaling=settings['SHIP_SCALING'],
        movement_speed=settings['MOVEMENT_SPEED'],
        rotation_speed=settings['ROTATION_SPEED']
    )

    playerScore = Score(
        kills=0,
        score=0,
        deaths=0,
        space_junk_blown_up=0,
        ufo_deaths=0,
        ufo_kills=0,
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
        ufo_kills=0,
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
                 start_position: Vec2d,
                 player_number=0,
                 input_source=CONTROLLER,
                 status=ALIVE,
                 lives=-1,
                 damping_index=3
                 ):

        self._damping_idx = damping_index

        self._playerData : PlayerData = playerData
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

        logger.info(f"Player Initialized: {self._playerData.shipData}")

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
        logger.debug(f"Setting up Player: ({self.player_name}, {self.player_name})")
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
        self.body.angular_velocity /= 1.25

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

        self.calculate_distance_flown()
        self.last_position = self.position

        self.body.angular_velocity += self.applied_rotational_vel
        #self.body.apply_force_at_world_point((dx, -dy), (self.center_x, self.center_y))
        self.body.apply_force_at_local_point((dx, dy), (0, 0))

    def calculate_distance_flown(self):
        distance = (self.position - self.last_position).length
        self.add_distance_flown(distance)

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

    def die(self):
        logger.debug(f"Player {self.player_number} - {self.player_name} died - killed by: {self.last_hit_by}!")
        super().die()   
        self.explode()

    def explode(self):
        logger.debug(f"Player {self.player_number} - {self.player_name} exploded! Killed by: {self.last_hit_by}")
        super().explode()

        if self.last_hit_by == "UFO":
            self.main.scoreboard.add_ufo_death(self.player_number)
        else:
            self.main.scoreboard.add_kill(self.last_hit_by, self)
            self.main.scoreboard.add_death(self.player_number)

        self.lives -= 1
        self.timers.add(RESPAWN_TIMER, 5)

    def shoot(self):
        if self.status is ALIVE:
            super().shoot()
            self.add_shot_fired()

    def add_death(self):
        self._playerData.playerScore.deaths += 1
        self._playerData.playerStats.deaths += 1

    def add_kill(self):
        self._playerData.playerScore.kills += 1
        self._playerData.playerStats.kills += 1

    def add_score(self, amount):
        self._playerData.playerScore.score += amount
        self._playerData.playerStats.total_score += amount

    def add_shot_fired(self):
        self._playerData.playerScore.shots_fired += 1
        self._playerData.playerStats.shots_fired += 1

    def add_shot_hit(self):
        self._playerData.playerScore.shots_hit += 1
        self._playerData.playerStats.shots_hit += 1

    def add_space_junk_blown_up(self):
        self._playerData.playerScore.space_junk_blown_up += 1
        self._playerData.playerStats.total_space_junk_blown_up += 1

    def add_ufo_death(self):
        self._playerData.playerScore.ufo_deaths += 1
        self._playerData.playerStats.ufo_deaths += 1

    def add_ufo_kill(self):
        self._playerData.playerScore.ufo_kills += 1
        self._playerData.playerStats.ufo_kills += 1

    def add_distance_flown(self, distance):
        self._playerData.playerScore.distance_flown += distance
        self._playerData.playerStats.distance_traveled += distance
    
    def calculate_accuracy(self):   
        shots_fired = self._playerData.playerScore.shots_fired
        shots_hit = self._playerData.playerScore.shots_hit

        if shots_fired == 0:
            self._playerData.playerScore.accuracy = 0.0
        else:
            self._playerData.playerScore.accuracy = (shots_hit / shots_fired) * 100.0

    def save(self):
        if not os.path.exists(PLAYER_DIRECTORY):
            os.makedirs(PLAYER_DIRECTORY)

        player_fname = os.path.join(PLAYER_DIRECTORY, self.player_name)

        logger.info(f"Saving player profile for: {self.player_name}")

        self.calculate_accuracy()
        self._playerData.shipData.hitpoints = self.max_hitpoints

        with open(player_fname, 'w') as file:
            json.dump({
                'name' : self._playerData.name,
                'damping' : self._damping_idx,
                'shipData' : {
                    'sprite' : self._playerData.shipData.sprite,
                    'status' : ALIVE,
                    'hitpoints' : self._playerData.shipData.hitpoints,
                    'mass' : self.mass,
                    'friction' : self.friction,
                    'elasticity' : self.elasticity,
                    'scaling' : 0.5,
                    'movement_speed' : self.movement_speed,
                    'rotation_speed' : self.rotation_speed
                },
                'playerScore' : {
                    'kills' : self._playerData.playerScore.kills,
                    'score' : self._playerData.playerScore.score,
                    'deaths' : self._playerData.playerScore.deaths,
                    'space_junk_blown_up' : self._playerData.playerScore.space_junk_blown_up,
                    'ufo_deaths' : self._playerData.playerScore.ufo_deaths,
                    'ufo_kills' : self._playerData.playerScore.ufo_kills,
                    'shots_fired' : self._playerData.playerScore.shots_fired,
                    'shots_hit' : self._playerData.playerScore.shots_hit
                },
                'TotalPlayerStats' : {
                    'total_score' : self._playerData.playerStats.total_score,
                    'highest_score' : self._playerData.playerStats.highest_score,
                    'total_space_junk_blown_up' : self._playerData.playerStats.total_space_junk_blown_up,
                    'highest_space_junk_blown_up' : self._playerData.playerStats.highest_space_junk_blown_up,
                    'highest_kills' : self._playerData.playerStats.highest_kills,
                    'highest_deaths' : self._playerData.playerStats.highest_deaths,
                    'kills' : self._playerData.playerStats.kills,
                    'deaths' : self._playerData.playerStats.deaths,
                    'kd_ratio' : self._playerData.playerStats.kd_ratio,
                    'ufo_deaths' : self._playerData.playerStats.ufo_deaths,
                    'ufo_kills' : self._playerData.playerStats.ufo_kills,
                    'shots_fired' : self._playerData.playerStats.shots_fired,
                    'shots_hit' : self._playerData.playerStats.shots_hit,
                    'accuracy' : self._playerData.playerStats.accuracy,
                    'distance_traveled' : self._playerData.playerStats.distance_traveled
                }
            }
            , file,
            indent=1) 

def get_player_or_make_new_one(settings, player_name) -> PlayerData:
    if player_file_exists(player_name):
        logger.info(f"Loading existing player profile for: {player_name}")
        return load_player(player_name) 
    else:
        logger.info(f"Creating new player profile for: {player_name}")
        return make_new_player(settings, player_name)

def load_player(player_name) -> PlayerData:
    player_fname = os.path.join(PLAYER_DIRECTORY, player_name)
    logger.debug("In load_player")

    if not os.path.exists(player_fname):
        logger.warning("Player file not found: %s. Creating new player.", player_fname)
        return None

    logger.debug(f"Loading Player '{player_name}' from '{player_fname}'")

    with open(player_fname, 'r') as fh:
        data = json.load(fh)

    # Player Data
    damping = data.get('damping', 0)

    # Reconstruct ShipData
    sd = data.get('shipData', {})
    ship_data = ShipData(
        sprite=sd.get('sprite', ':sprites:png/sprites/Ships/playerShip1_blue.png'),
        status=sd.get('status', ALIVE),
        hitpoints=sd.get('hitpoints', 10),
        mass=sd.get('mass', 20),
        friction=sd.get('friction', 0.0),
        elasticity=sd.get('elasticity', 0.0),
        scaling=sd.get('scaling', 0.0),
        movement_speed=sd.get('movement_speed', 0.0),
        rotation_speed=sd.get('rotation_speed', 0.0),
        max_speed=sd.get('max_speed', 0.0)
    )

    # Reconstruct Score (fill missing fields with sensible defaults)
    ps = data.get('playerScore', {})
    score = Score(
        kills=ps.get('kills', 0),
        score=ps.get('score', 0),
        deaths=ps.get('deaths', 0),
        space_junk_blown_up=ps.get('space_junk_blown_up', 0),
        ufo_deaths=ps.get('ufo_deaths', 0),
        ufo_kills=ps.get('ufo_kills', 0),
        shots_fired=ps.get('shots_fired', 0),
        shots_hit=ps.get('shots_hit', 0),
        accuracy=ps.get('accuracy', 0.0),
        kd=ps.get('kd', 0.0),
        distance_flown=ps.get('distance_flown', 0),
        highest_speed=ps.get('highest_speed', 0),
    )

    # Reconstruct TotalPlayerStats
    tps = data.get('TotalPlayerStats', {})
    total_stats = TotalPlayerStats(
        total_score=tps.get('total_score', 0),
        highest_score=tps.get('highest_score', 0),
        total_space_junk_blown_up=tps.get('total_space_junk_blown_up', 0),
        highest_space_junk_blown_up=tps.get('highest_space_junk_blown_up', 0),
        highest_kills=tps.get('highest_kills', 0),
        highest_deaths=tps.get('highest_deaths', 0),
        kills=tps.get('kills', 0),
        deaths=tps.get('deaths', 0),
        kd_ratio=tps.get('kd_ratio', 0.0),
        ufo_deaths=tps.get('ufo_deaths', 0),
        ufo_kills=tps.get('ufo_kills', 0),
        shots_fired=tps.get('shots_fired', 0),
        shots_hit=tps.get('shots_hit', 0),
        accuracy=tps.get('accuracy', 0.0),
        distance_traveled=tps.get('distance_traveled', 0),
    )

    player_data = PlayerData(
        name=data.get('name', player_name),
        shipSprite=data.get('shipSprite', ship_data.sprite),
        shipData=ship_data,
        playerScore=score,
        playerStats=total_stats,
    )

    # Instantiate Player object (main set to None for now)
    player = Player(
        main=None,
        player_name=player_data.name,
        playerData=player_data,
        start_position=Vec2d(0, 0),
        player_number=0,
        input_source=None,
        status=ALIVE,
        lives=-1,
    )

    player._damping_idx = damping
    player.data = ship_data

    logger.debug(f"DAMPING INDEX: {player._damping_idx} {damping}")

    return player
