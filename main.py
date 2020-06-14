from math import sin, cos, pi
import numpy as np
import pyglet
from pyglet.sprite import Sprite
from pyglet.window import key
from random import randint
from time import time

from Alien import Alien, Swarm

gameWindow = pyglet.window.Window(800, 600, fullscreen=False)


def loadResources():
    global alienShipTexture, alienShieldTexture

    # Set the locations to find resources
    pyglet.resource.path = ['resources']
    pyglet.resource.reindex()

    # Load the alien ship textures
    alienShipTexture = pyglet.resource.image('images/alienShipBW.png')
    alienShieldTexture = pyglet.resource.image('images/alienShieldBW.png')

    # Set the anchors for rotation
    alienShipTexture.anchor_x = alienShipTexture.width / 2
    alienShipTexture.anchor_y = alienShipTexture.height / 2
    alienShieldTexture.anchor_x = alienShieldTexture.width / 2
    alienShieldTexture.anchor_y = alienShieldTexture.height / 2

    print(vars(alienShieldTexture))
    print(vars(alienShipTexture))

def colorShip(texture, color, colorFade=(0,0,0), colorHighlight=(255,255,255)):
    global cachedTextures

    if (texture.__hash__(), color, colorFade, colorHighlight) in cachedTextures.keys():
        print(cachedTextures[(texture.__hash__(), color, colorFade, colorHighlight)])
        return cachedTextures[(texture.__hash__(), color, colorFade, colorHighlight)]

    else:
        textureData = texture.get_image_data().get_data('RGBA', texture.width * 4)
        newTextureData = b''
        baseColorValue = 72

        fadeDelta = (colorFade[0] - color[0], colorFade[1] - color[1], colorFade[2] - color[2])
        highlightDelta = (colorHighlight[0] - color[0], colorHighlight[1] - color[1], colorHighlight[2] - color[2])

        # Colorize the alien ship
        for i in range(0, len(textureData), 4):
            pixelData = textureData[i:i+4]

            value = pixelData[0]

            # If the value is less than the base color value, we want to fade to black
            if value < baseColorValue:
                r = int(color[0] + fadeDelta[0] * (baseColorValue - value) / baseColorValue)
                g = int(color[1] + fadeDelta[1] * (baseColorValue - value) / baseColorValue)
                b = int(color[2] + fadeDelta[2] * (baseColorValue - value) / baseColorValue)

            else:
                r = int(color[0] + highlightDelta[0] * (value - baseColorValue) / (255 - baseColorValue))
                g = int(color[1] + highlightDelta[1] * (value - baseColorValue) / (255 - baseColorValue))
                b = int(color[2] + highlightDelta[2] * (value - baseColorValue) / (255 - baseColorValue))

            newTextureData += bytes([r, g, b, pixelData[3]])

        newTexture = pyglet.image.ImageData(texture.width, texture.height, 'RGBA', newTextureData)
        newTexture.anchor_x = int(texture.anchor_x)
        newTexture.anchor_y = int(texture.anchor_y)

        cachedTextures[(texture.__hash__(), color, colorFade, colorHighlight)] = newTexture
        return newTexture

def update(dt):
    global cameraOffset

    if mouseState[pyglet.window.mouse.LEFT]:
        alien.setAcceleartion((mouseLocation - alien.getShieldCenter() + cameraOffset))
    else:
        alien.setAcceleartion((0,0))

    alien.update(dt)
    swarm0.update(dt)
    for i in swarm1:
        i.update(dt)

    centerCamera(alien.position)

    alien.setCameraPosition(cameraOffset)
    swarm0.setCameraPosition(cameraOffset)
    
    for i in swarm1:
        i.setCameraPosition(cameraOffset)

    pass

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

    alien = Alien(alienShipTexture, alienShieldTexture, alienBatch, shipGroup, shieldGroup, x=screenWidth / 2, y=screenHeight/2)

    swarmShip = colorShip(alienShipTexture, (255, 0, 255), (0, 0, 255), (255, 0, 0))
    swarmShield = colorShip(alienShieldTexture, (255, 0, 255), (0, 0, 255), (255, 0, 0))
    swarm0 = Swarm(0, swarmShip, swarmShield, alienBatch, shipGroup, shieldGroup, x=screenWidth / 2, y=screenHeight/2)

    swarm1 = []

    for i in range(32):
        c0 = (randint(0, 255), randint(0, 255), randint(0, 255))
        c1 = (randint(0, 255), randint(0, 255), randint(0, 255))
        c2 = (randint(0, 255), randint(0, 255), randint(0, 255))

        shipTex = colorShip(alienShipTexture, c0, c1, c2)
        shieldTex = colorShip(alienShieldTexture, c0, c1, c2)
        swarm1.append(Alien(shipTex, shieldTex, alienBatch, shipGroup, shieldGroup, x=screenWidth / 2, y=screenHeight/2))
    # Create the FPS monitor
    fpsDisplay = pyglet.window.FPSDisplay(window=gameWindow)
    

    for i, ship in enumerate(swarm0):
        theta = i * 2 * pi / len(swarm0)
        ship.setAcceleartion((sin(theta), cos(theta)))

    for i, ship in enumerate(swarm1):
        theta = (i + 0.5) * 2 * pi / len(swarm1)
        ship.setAcceleartion((sin(theta), cos(theta)))

    pyglet.clock.schedule_interval(update, 1/60.0)

    # TODO Rest window width and height
    pyglet.app.run()
