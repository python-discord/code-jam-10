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
    """Calls the appropriate decryptor and returns the encryptor class and secret message"""
    print(file_path, key)
    img = Image.open(file_path)
    lastPixel = img.load()[-1, -1]

    if lastPixel[-2] & 7 == 1:
        object = ExistingImage(img, key)
    else:
        img.convert("RGBA")
        object = TypingColors(img)
        object.set_key(key)  # load the key
    return object, object.decode()  # return the text for the gui
