from math import sin, cos, pi
import numpy as np
import pyglet
from pyglet.sprite import Sprite
from pyglet.window import key
from random import randint
from time import time

from Alien import Alien, Swarm
from Player import Player
from Utilities import Utils

gameWindow = pyglet.window.Window(800, 600, fullscreen=False)


def loadResources():
    global alienShipTexture, alienShieldTexture, playerShipTexture, pointerTexture

    # Set the locations to find resources
    pyglet.resource.path = ['resources']
    pyglet.resource.reindex()

    # Load the alien ship textures
    alienShipTexture = pyglet.resource.image('images/alienShip.png')
    alienShieldTexture = pyglet.resource.image('images/alienShield.png')

    playerShipTexture = pyglet.resource.image('images/playerShip.png')

    pointerTexture = pyglet.resource.image('images/pointer.png')

    # Set the anchors for rotation
    alienShipTexture.anchor_x = alienShipTexture.width / 2
    alienShipTexture.anchor_y = alienShipTexture.height / 2
    alienShieldTexture.anchor_x = alienShieldTexture.width / 2
    alienShieldTexture.anchor_y = alienShieldTexture.height / 2
    
    playerShipTexture.anchor_x = playerShipTexture.width / 2
    playerShipTexture.anchor_y = playerShipTexture.height / 2
    
    pointerTexture.anchor_x = pointerTexture.width / 2
    pointerTexture.anchor_y = pointerTexture.height / 2

def update(dt):
    global cameraOffset, rotationalSens, forwardAccel, reverseAccel, orthAccel



    ###### Handle Player Input ######

    if keyboard[key.A]:
        player.ship.rotation -= rotationalSens * dt

    if keyboard[key.D]:
        player.ship.rotation += rotationalSens * dt

    if keyboard[key.W]:
        player.setAcceleartion((forwardAccel * cos(player.ship.rotation * pi / 180), -forwardAccel * sin(player.ship.rotation * pi / 180)))
    elif keyboard[key.S]:
        player.setAcceleartion((reverseAccel * cos(player.ship.rotation * pi / 180), -reverseAccel * sin(player.ship.rotation * pi / 180)))
    elif keyboard[key.Q]:
        player.setAcceleartion((orthAccel * sin(player.ship.rotation * pi / 180), orthAccel * cos(player.ship.rotation * pi / 180)))
    elif keyboard[key.E]:
        player.setAcceleartion((-orthAccel * sin(player.ship.rotation * pi / 180), -orthAccel * cos(player.ship.rotation * pi / 180)))  
    else:
        player.setAcceleartion((0,0))



    ###### Update all sprites ######

    player.update(dt)
    for i in swarm1:
        i.update(dt)

    centerCamera(player.position)

    player.setCameraPosition(cameraOffset)
    
    for i in swarm1:
        i.setCameraPosition(cameraOffset)
        i.setPointerPosition(player.position, screenWidth, screenHeight)

def centerCamera(location):
    """ This function centers the visible portion of the screen around
        A certain location


    Args:
        location (tuple): The location to be centered
    """
    global cameraOffset
    cameraOffset[0] = location[0] - screenWidth / 2
    cameraOffset[1] = location[1] - screenHeight / 2

@gameWindow.event
def on_mouse_press(x, y, button, modifiers):
    global mouseState
    mouseState[button] = True

@gameWindow.event
def on_mouse_release(x, y, button, modifiers):
    global mouseState
    mouseState[button] = False

@gameWindow.event
def on_mouse_motion(x, y, dx, dy):
    global mouseLocation
    mouseLocation = (x, y)

@gameWindow.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global mouseLocation
    mouseLocation = (x, y)

@gameWindow.event
def on_draw():
    gameWindow.clear()
    alienBatch.draw()
    fpsDisplay.draw()


if __name__ == '__main__':
    alienShipTexture = None
    alienShieldTexture = None
    playerShipTexture = None
    pointerTexture = None
    cachedTextures = {}

    # Make the windows fullscreen on the first screen found
    display = pyglet.canvas.get_display()
    screens = display.get_screens()
    screenWidth = screens[0].width
    screenHeight = screens[0].height
    screenCenter = np.array((screenWidth / 2, screenHeight / 2), dtype=np.float32)
    gameWindow.set_size(screenWidth, screenHeight)
    gameWindow.set_fullscreen(fullscreen=True, screen=screens[0])

    # Create a "camera" offset, allowing for easy panning around the world
    cameraOffset = np.array((0, 0), dtype=np.float32)

    # Keep track of mouse and keyboard states
    mouseLocation = (0, 0)
    mouseState = {pyglet.window.mouse.LEFT: False,
                    pyglet.window.mouse.MIDDLE: False,
                    pyglet.window.mouse.RIGHT: False}

    keyboard = key.KeyStateHandler()
    oldKeyboard = key.KeyStateHandler()
    gameWindow.push_handlers(keyboard)

    # Load in the resources
    loadResources()

    alienBatch = pyglet.graphics.Batch()

    shipGroup = pyglet.graphics.OrderedGroup(10)
    shieldGroup = pyglet.graphics.OrderedGroup(20)
    overlayGroup = pyglet.graphics.OrderedGroup(30)


    playerShipColored = Utils.colorTexture(playerShipTexture, (120, 120, 120), (40, 40, 200), (255, 128, 0))
    player = Player(playerShipColored, alienShieldTexture, alienBatch, shipGroup, shieldGroup, x=screenWidth / 2, y=screenHeight/2)
    player.velocity = np.array((100,0), dtype=np.float32)
    rotationalSens = 200
    forwardAccel = 300
    reverseAccel = -200
    orthAccel = 150
    
    
    swarm1 = []

    for i in range(32):
        c0 = (randint(0, 255), randint(0, 255), randint(0, 255))
        c1 = (randint(0, 255), randint(0, 255), randint(0, 255))
        c2 = (randint(0, 255), randint(0, 255), randint(0, 255))
        c4 = (128 + c0[0] / 2, 128 + c0[1] / 2, 128 + c0[2] / 2,)

        shipTex = Utils.colorTexture(alienShipTexture, c0, c1, c2)
        shieldTex = Utils.colorTexture(alienShieldTexture, c0, c1, c2)
        pointerTex = Utils.colorTexture(pointerTexture, c4, c1, c2)
        swarm1.append(Alien(shipTex, shieldTex, pointerTex, alienBatch, shipGroup, shieldGroup, overlayGroup, x=screenWidth / 2, y=screenHeight/2))
        swarm1[-1].pointer.position = (12, i * 16 + 12)
        swarm1[-1].pointer.visible = True

    # Create the FPS monitor
    fpsDisplay = pyglet.window.FPSDisplay(window=gameWindow)
    

    for i, ship in enumerate(swarm1):
        theta = (i + 0.5) * 2 * pi / len(swarm1)
        ship.setAcceleartion((sin(theta), cos(theta)))

    pyglet.clock.schedule_interval(update, 1/60.0)

    # TODO Rest window width and height
    pyglet.app.run()
