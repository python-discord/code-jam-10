import numpy as np
from PIL import Image

from backend.typingcolors import TypingColors

PRINTABLE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t'


class Palette:
    """Pallete object to map chars to colours"""

    palette = {" ": (0, 0, 0, 0), (0, 0, 0, 0): " "}

    def __init__(self, key: str):
        """Maps all characters to colours using the key"""
        if not (3 < len(key) < 25):
            raise ValueError("key should be between 4 and 24 characters")

        self.key = self._generate_key(key)

        for n, char in enumerate(PRINTABLE):  # generate pallete
            val = self.key + n**n
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
        """Generates a int key from the string"""
        if not key:
            raise ValueError("String for encryption cannot be empty")
        return int.from_bytes(key.encode(), "little")

    def __getitem__(self, item):
        """Returns the color from char/char from color"""
        if type(item) not in (
            str,
            tuple,  # will not work if the color is specified as ndarray
        ):
            raise KeyError  # invalid decryption
        return self.palette.get(item, "?")


def load(file_path, key):
    """
    Returns the backend object created from loading image in file path.

    Takes in a file path to the image and the decryption key
    returns TypingColors object if key and image works, raises KeyError otherwise
    """
    img = Image.open(file_path).convert("RGBA")
    w, h = img.size
    object = TypingColors(img)
    object.set_encryption(key)  # load the key
    decoded_text = "".join([
        object.palette[(r, g, b, a)]
        for r, g, b, a in np.array(img)[0]
    ]).rstrip()  # get the text
    # split into rows and turning spaces to newlines
    decoded_chunks = [decoded_text[i:i+w]
                      for i in range(0, len(decoded_text), w)]
    decoded_text = ''.join([(line.rstrip()+'\n') if line.endswith(' ') else line
                            for line in decoded_chunks])
    object.update(decoded_text)
    return object, decoded_text  # return the text for the gui
