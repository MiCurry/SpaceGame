import logging
logger = logging.getLogger('space_game')

from SpaceGame.gametypes.Bullet import Bullet
from SpaceGame.gametypes.Explosion import ExplosionSize
from SpaceGame.gametypes.PlayZoneTypes import SpaceObject
from SpaceGame.gametypes.Ship import Ship
from SpaceGame.gametypes.UFOs import UFO
from SpaceGame.gametypes.enemies.Bug import Bug

import arcade

def ship_bullet_hit_handler(bullet: Bullet, ship: Ship, arbiter, space, data):
    creator = bullet.creator

    if creator == ship:
        logger.debug("Bullet hit its creator ship, ignoring hit.")
        return

    bullet.remove_from_sprite_lists()
    bullet.main.add_explosion(bullet.body.position, ExplosionSize.SMALL)

    creator.add_shot_hit()
    ship.damage(bullet)


def spaceObject_bullet_hit_handler(bullet: Bullet, junk: SpaceObject, arbiter, space, data):
    creator = bullet.creator

    bullet.remove_from_sprite_lists()
    bullet.main.add_explosion(bullet.body.position, ExplosionSize.SMALL)
    junk.damage(bullet)

    creator.add_shot_hit()

def bullet_ufo_hit_handler(bullet: Bullet, ufo: UFO, arbiter, space, data):
    creator = bullet.creator
    bullet.remove_from_sprite_lists()
    bullet.main.add_explosion(bullet.body.position, ExplosionSize.SMALL)
    ufo.damage(bullet)

    creator.add_shot_hit()


def bullet_bug_hit_handler(bullet: Bullet, bug: Bug, arbiter, space, data):
    creator = bullet.creator

    bullet.remove_from_sprite_lists()
    bullet.main.add_explosion(bullet.body.position, ExplosionSize.SMALL)
    bug.damage(bullet)

    creator.add_shot_hit()

def bullet_bullet_hit_handler(bullet1: Bullet, bullet2: Bullet, arbiter, space, data):
    bullet1.remove_from_sprite_lists()
    bullet2.remove_from_sprite_lists()
    bullet1.main.add_explosion(bullet1.body.position, ExplosionSize.BIG)