from SpaceGame.gametypes.Bullet import Bullet
from SpaceGame.gametypes.Explosion import ExplosionSize
from SpaceGame.gametypes.PlayZoneTypes import SpaceObject
from SpaceGame.gametypes.Ship import Ship
from SpaceGame.gametypes.UFOs import UFO


def ship_bullet_hit_handler(bullet: Bullet, ship: Ship, arbiter, space, data):
    if bullet.creator != ship.player_number:
        bullet.remove_from_sprite_lists()
        ship.damage(bullet)
        data['window'].add_explosion(bullet.body.position, ExplosionSize.SMALL)


def spaceObject_bullet_hit_handler(bullet: Bullet, junk: SpaceObject, arbiter, space, data):
    bullet.remove_from_sprite_lists()
    data['window'].add_explosion(bullet.body.position, ExplosionSize.SMALL)
    junk.damage(bullet.damage)


def bullet_ufo_hit_handler(bullet: Bullet, ufo: UFO, arbiter, space, data):
    bullet.remove_from_sprite_lists()
    data['window'].add_explosion(bullet.body.position, ExplosionSize.SMALL)
    ufo.damage(bullet.damage)
