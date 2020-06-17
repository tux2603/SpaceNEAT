import pyglet

class Utils:
    _cachedColorizedtextures = {}

    @staticmethod
    def colorTexture(texture, color, colorLow=(0,0,0), colorHighlight=(255,255,255), midColorValue=72):
        """Colorizes a black and white texture. the parameter color will be used as a base color, assigned 
            to any regions that have a value equal to midColorValue. Any regions with a higher value will
            be faded linearly to colorHighlight, and any regions with a lower value will be faded to color
            fade. Alpha values and anchors are preserved as-is. textures are memoized to (hopefully) improve
            efficiency. In any case, it won't hurt, right?

        Args:
            texture (pyglet.image.AbstractTexture): The texture to be shaded
            color (tuple): The base color to be applied to the image. 
            colorLow (tuple, optional): The color to be applied to darker areas of the image. Defaults to (0,0,0).
            colorHighlight (tuple, optional): The color to be applied to brighter areas of the image. Defaults to (255,255,255).
            midColorValue (int, optional): An integer ranging from 0 to 255 To be used as the "reference" value when blending colors. Defaults to 72.

        Returns:
            [pyglet.image.ImageData]: The shaded texture. If the texture has been shaded with this color combo
                before, it returns a reference to that texture
        """

        # Check to see if we have already processed this texture. 
        if (texture.__hash__(), color, colorLow, colorHighlight) in Utils._cachedColorizedtextures.keys():
            return Utils._cachedColorizedtextures[(texture.__hash__(), color, colorLow, colorHighlight)]

        else:
            # Extract the raw color data from the texture
            textureData = texture.get_image_data().get_data('RGBA', texture.width * 4)

            # Create a byte string to store the colorized data in
            newTextureData = b''

            # Compute the differences between the fade colors and the base colors. This will be used
            #   to create a linear gradient when the colorized data is generated
            fadeDelta = (colorLow[0] - color[0], colorLow[1] - color[1], colorLow[2] - color[2])
            highlightDelta = (colorHighlight[0] - color[0], colorHighlight[1] - color[1], colorHighlight[2] - color[2])

            # Colorize the texture pixel by pixel
            for i in range(0, len(textureData), 4):

                # Get the substring with the pixel data
                pixelData = textureData[i:i+4]

                # The texture input is assumed to be grayscale, so it doesn't matter which channel
                #   is read from
                value = pixelData[0]

                # If the value is less than the base color value, we want to fade to the low color
                if value < midColorValue:
                    r = int(color[0] + fadeDelta[0] * (midColorValue - value) / midColorValue)
                    g = int(color[1] + fadeDelta[1] * (midColorValue - value) / midColorValue)
                    b = int(color[2] + fadeDelta[2] * (midColorValue - value) / midColorValue)

                # Else, we want to fade to the highlight color
                else:
                    r = int(color[0] + highlightDelta[0] * (value - midColorValue) / (255 - midColorValue))
                    g = int(color[1] + highlightDelta[1] * (value - midColorValue) / (255 - midColorValue))
                    b = int(color[2] + highlightDelta[2] * (value - midColorValue) / (255 - midColorValue))

                # Append the new pixel data
                newTextureData += bytes([r, g, b, pixelData[3]])

            # Create a new texture with the data and set the anchor points
            newTexture = pyglet.image.ImageData(texture.width, texture.height, 'RGBA', newTextureData)
            newTexture.anchor_x = int(texture.anchor_x)
            newTexture.anchor_y = int(texture.anchor_y)

            # memoize this texture
            Utils._cachedColorizedtextures[(texture.__hash__(), color, colorLow, colorHighlight)] = newTexture
            
            return newTexture
