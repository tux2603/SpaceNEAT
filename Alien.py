from math import atan2, pi
import neat
import numpy as np
from pyglet.sprite import Sprite

class Alien:
    def __init__(self, shipTexture, shieldTexture, pointerTexture, alienBatch, shipGroup, shieldGroup, overlayGroup, x=0, y=0):
        self.ship = Sprite(shipTexture, x=x, y=y, blend_src=770, blend_dest=771, batch=alienBatch, group=shipGroup, usage='dynamic', subpixel=False)
        self.shield = Sprite(shieldTexture, x=x, y=y, blend_src=770, blend_dest=771, batch=alienBatch, group=shieldGroup, usage='dynamic', subpixel=False)
        
        self.pointer = Sprite(pointerTexture, x=x, y=y, blend_src=770, blend_dest=771, batch=alienBatch, group=overlayGroup, usage='dynamic', subpixel=False)
        self.pointer.visible = False

        # Set the physical aspects of the Alien ship
        self.acceleration = np.array((0, 0), dtype=np.float32)
        self.velocity = np.array((0, 0), dtype=np.float32)
        self.position = np.array((x, y), dtype=np.float32)

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

        self.ship.rotation = atan2(-self.velocity[1], self.velocity[0]) * 180 / pi #self.angularPosition

    def setCameraPosition(self, cameraOffset):
        self.ship.position = self.position - cameraOffset
        self.shield.position = self.getShieldCenter() - cameraOffset

    def setPointerPosition(self, playerLocation, screenWidth, screenHeight):
        shieldCenter = self.getShieldCenter()

        # Check to see if the alien ship is "on screen"
        if shieldCenter[0] >= playerLocation[0] - screenWidth / 2 and \
                shieldCenter[0] <= playerLocation[0] + screenWidth / 2 and \
                shieldCenter[1] >= playerLocation[1] - screenHeight / 2 and \
                shieldCenter[1] <= playerLocation[1] + screenHeight / 2:
            self.pointer.visible = False

        # If the ship isn't on screen, the position and direction of the pointer will have to be computed
        else:

            self.pointer.visible = True

            spacing = 10

            # Much math will now begin. Essentially, we will draw line segments between the four 
            #   corners of the display and another between the player and the alien ship, then find
            #   their intersection through primitive raytracing. If there is an intersection in the
            #   valid range, the pointer will be drawn there
            x1, y1 = (0, 0)
            dx1, dy1 = self.position - playerLocation

            tlx, tly = (-screenWidth / 2 + spacing,  screenHeight / 2 - spacing)
            brx, brY = ( screenWidth / 2 - spacing, -screenHeight / 2 + spacing)

            self._setPointerAtIntercept(x1, y1, dx1, dy1, tlx, tly, screenWidth - spacing * 2, 0, screenWidth / 2, screenHeight / 2) or \
                self._setPointerAtIntercept(x1, y1, dx1, dy1, brx, brY, -screenWidth + spacing * 2, 0, screenWidth / 2, screenHeight / 2) or \
                self._setPointerAtIntercept(x1, y1, dx1, dy1, tlx, tly, 0, -screenHeight + spacing * 2, screenWidth / 2, screenHeight / 2) or \
                self._setPointerAtIntercept(x1, y1, dx1, dy1, brx, brY, 0, screenHeight - spacing * 2, screenWidth / 2, screenHeight / 2)


    def _setPointerAtIntercept(self, x1, y1, dx1, dy1, x2, y2, dx2, dy2, offsetX, offsetY):
        denominator = dx1 * dy2 - dx2 * dy1

        if denominator != 0:
            intercept1 = (dy2 * (x2 - x1) - dx2 * (y2 - y1)) / denominator
            intercept2 = (dy1 * (x2 - x1) - dx1 * (y2 - y1)) / denominator

            if intercept1 >= 0 and intercept1 <= 1 and intercept2 >= 0 and intercept2 <= 1:
                self.pointer.position = (x1 + dx1 * intercept1 + offsetX, y1 + dy1 * intercept1 + offsetY)
                self.pointer.rotation = -atan2(dy1, dx1) * 180 / pi
                return True

        return False

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

class MotherShip:
    """ The mothership class will handle the neat algorithm, using it to
        (hopefully) generate better and better swarms. Swarms will be
        generated in waves, each wave corresponding to another generation of
        the neural nets. In order to prevent the user having to slog through
        20 some odd waves before there's evena  kinda useful opponent, there 
        will be some pregenerated genomes used as a starting point (hopefully)
    """

    def __init__(self, configPath):
        self._config 

    pass