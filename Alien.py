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

        self.ship.scale = 0.8


    def getShieldCenter(self): 
        accelLen = np.linalg.norm(self.acceleration)
        return self.position - (self.acceleration if accelLen < 50 else self.acceleration * 50 / accelLen) / 5
    
    def setAcceleartion(self, acceleration):
        self.acceleration = np.array(acceleration, dtype=np.float32)


    def update(self, dt):
        """ Moves and rotates the alien space ship thingy

        Args:
            dt (float): The change in time since the last update in milliseconds
        """

        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt 

        self.angularVelocity += self.angularAcceleration * dt
        self.angularPosition += self.angularVelocity * dt

        self.ship.rotation = self.angularPosition

    def setCameraPosition(self, cameraOffset):
        self.ship.position = self.position - cameraOffset
        self.shield.position = self.getShieldCenter() - cameraOffset
        
        

class Swarm:
    def __init__(self, size, shipTexture, shieldTexture, alienBatch, shipGroup, shieldGroup, x=0, y=0):
        self.members = []

        for i in range(size):
            self.members.append(Alien(shipTexture, shieldTexture, alienBatch, shipGroup, shieldGroup, x=x, y=y))

    def __iter__(self):
        return SwarmIterator(self)

    def __len__(self):
        return len(self.members)

    def update(self, dt):
        for i in self:
            i.update(dt)

    def setCameraPosition(self, cameraOffset):
        for i in self:
            i.setCameraPosition(cameraOffset)

class SwarmIterator:
    """ A utility class for the sole and express purpose of iterating over 
        alien ships within a swarm. It's just a standard copy-pasta style
        iterator. Nothing fancy
    """

    def __init__(self, swarm):
        self._swarm = swarm
        self._index = 0

    def __next__(self):
        if self._index < len(self._swarm.members):
            alien = self._swarm.members[self._index]
            self._index += 1
            return alien
        raise StopIteration
