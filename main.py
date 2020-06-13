from math import sin, cos
import numpy as np
import pyglet
from pyglet.sprite import Sprite
from pyglet.window import key
from time import time

from Alien import Alien, Swarm

gameWindow = pyglet.window.Window(800, 600, fullscreen=False)


def loadResources():
    global alienShipTexture, alienShieldTexture
    global fpsDisplay

    # Set the locations to find resources
    pyglet.resource.path = ['resources']
    pyglet.resource.reindex()

    # Load the alien ship textures
    alienShipTexture = pyglet.resource.image(
        'images/alienThingSingleFrame.png')
    alienShieldTexture = pyglet.resource.image('images/alienShield.png')

    # Set the anchors for rotation
    alienShipTexture.anchor_x = alienShipTexture.width / 2
    alienShipTexture.anchor_y = alienShipTexture.height / 2
    alienShieldTexture.anchor_x = alienShieldTexture.width / 2
    alienShieldTexture.anchor_y = alienShieldTexture.height / 2

    # Create the FPS monitor
    fpsDisplay = pyglet.window.FPSDisplay(window=gameWindow)


def update(dt):
    global cameraOffset

    if mouseState[pyglet.window.mouse.LEFT]:
        alien.setAcceleartion((mouseLocation - alien.getShieldCenter() + cameraOffset))
    else:
        alien.setAcceleartion((0,0))

    alien.update(dt, cameraOffset)
    pass

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

    alien = Alien(alienShipTexture, alienShieldTexture,
                  alienBatch, shipGroup, shieldGroup, x=screenWidth / 2, y=screenHeight/2)

    swarm0 = Swarm(5, alienShipTexture, alienShieldTexture,
                  alienBatch, shipGroup, shieldGroup, x=screenWidth / 2, y=screenHeight/2)

    pyglet.clock.schedule_interval(update, 1/60.0)

    # TODO Rest window width and height
    pyglet.app.run()
