import numpy as np
from pyglet.sprite import Sprite

class Alien:
    def __init__(self, shipTexture, shieldTexture, alienBatch, shipGroup, shieldGroup, x=0, y=0):
        self.ship = Sprite(shipTexture, x=x, y=y, blend_src=770, blend_dest=771, batch=alienBatch, group=shipGroup, usage='dynamic', subpixel=False)
        self.shield = Sprite(shieldTexture, x=x, y=y, blend_src=770, blend_dest=771, batch=alienBatch, group=shieldGroup, usage='dynamic', subpixel=False)

        # Set the physical aspects of the Alien ship
        self.acceleration = np.array((0, 0), dtype=np.float32)
        self.velocity = np.array((0, 0), dtype=np.float32)
        self.position = np.array((x, y), dtype=np.float32)

        self.angularAcceleration = 0
        self.angularVelocity = 0
        self.angularPosition = 0


    def getShieldCenter(self): 
        accelLen = np.linalg.norm(self.acceleration)
        return self.position - (self.acceleration if accelLen < 50 else self.acceleration * 50 / accelLen) / 5
    
    def setAcceleartion(self, acceleration):
        self.acceleration = np.array(acceleration, dtype=np.float32)


    def update(self, dt, cameraOffset):
        """ Moves and rotates the alien space ship thingy

        Args:
            dt (float): The change in time since the last update in milliseconds
        """

        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt 

        self.angularVelocity += self.angularAcceleration * dt
        self.angularPosition += self.angularVelocity * dt

        self.ship.position = self.position - cameraOffset
        self.ship.rotation = self.angularPosition
        accelLen = np.linalg.norm(self.acceleration)
        self.shield.position = self.getShieldCenter() - cameraOffset
        



