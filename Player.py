from math import atan2, pi
import neat
import numpy as np
from pyglet.sprite import Sprite

class Player:
    def __init__(self, shipTexture, shieldTexture, alienBatch, shipGroup, shieldGroup, x=0, y=0):
        self.ship = Sprite(shipTexture, x=x, y=y, blend_src=770, blend_dest=771, batch=alienBatch, group=shipGroup, usage='dynamic', subpixel=False)
        self.shield = Sprite(shieldTexture, x=x, y=y, blend_src=770, blend_dest=771, batch=alienBatch, group=shieldGroup, usage='dynamic', subpixel=False)
        
        # Set the physical aspects of the Alien ship
        self.acceleration = np.array((0, 0), dtype=np.float32)
        self.velocity = np.array((0, 0), dtype=np.float32)
        self.position = np.array((x, y), dtype=np.float32)

    def setAcceleartion(self, acceleration):
        self.acceleration = np.array(acceleration, dtype=np.float32)


    def update(self, dt):
        """ Moves and rotates the alien space ship thingy

        Args:
            dt (float): The change in time since the last update in milliseconds
        """

        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt 


    def setCameraPosition(self, cameraOffset):
        self.ship.position = self.position - cameraOffset
        self.shield.position = self.position - cameraOffset