from PIL.Image import Image as PILImage
from PIL.ImageColor import getrgb

from .obfuscate import Obfuscate


class ColourBox(Obfuscate):
    """ColourBox is a form of obfuscation where it sets all pixels in a given bounding box to the given colour."""

    def __init__(self, colour: tuple[int, int, int] | str):
        """Create a new ColourBox obfuscator

        Expects the bounding box to be valid for the image.

        Args:
            colour (tuple[int, int, int] | str): colour to set pixels in the bounding box to.
            Can be a string e.g. "black", or an RGB tuple e.g. (255,255,255)

        Raises:
            ValueError: If the supplied colour is invalid
        """
        if isinstance(colour, str):
            self.__colour = getrgb(colour)
        else:
            if len(colour) != 3:
                raise ValueError(
                    f"Colour tuple must have 3 elements (RGB). Got {len(colour)}"
                )
            self.__colour = colour

    def hide(self, box: tuple[int, int, int, int], image: PILImage):
        """Hide the pixels in the bounding box given in the image.

        Args:
            box (tuple[int, int, int, int]): Bounding box to obfuscate
            image (PILImage): Image to obfuscate
        """
        for i in range(box[0], box[2]):
            for j in range(box[1], box[3]):
                image.putpixel((i, j), self.__colour)
