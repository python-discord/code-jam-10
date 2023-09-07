import numpy as np
from PIL import Image

from backend.steganography import ExistingImage
from backend.typingcolors import TypingColors
from gui.modules import *


class Palette:
    """Pallete object to map chars to colours"""

    palette = {" ": (0, 0, 0, 0), (0, 0, 0, 0): " "}

    def __init__(self, key: str):
        """Maps all characters to colours using the key"""
        self.key = self._generate_key(key)

        for n, char in enumerate(PRINTABLE):  # generate pallete
            val = self.key * n
            r, g, b, a = (
                (val & 255),
                (val >> 8) & 255,
                (val >> 16) & 255,
                (val >> 20) & 63,
            )
            color = (r, g, b, 255 - a)
            self.palette[char] = color
            self.palette[color] = char

    def _generate_key(self, key):
        """Generates an int key from the string"""
        return int.from_bytes(key.encode(), "little")

    def __getitem__(self, item):
        """Returns the color from char/char from color"""
        if item not in self.palette and isinstance(item, str):
            return self.palette["?"]
        return self.palette[item]  # raise keyerror if invalid decryption key


def decrypt(file_path, key):
    """
    Returns the backend object created from loading image in file path.

    Takes in a file path to the image and the decryption key
    returns TypingColors object if key and image works, raises KeyError otherwise
    """
    img = Image.open(file_path)
    imgarr = np.array(img)
    if imgarr[-1][-1][-2] & 7 == 1:
        object = ExistingImage(imgarr, key)
    else:
        object = TypingColors(imgarr.convert("RGBA").reshape(-1, 4))
        object.set_encryption(key)  # load the key
    return object, object.decode()  # return the text for the gui
