import numpy as np
from PIL import Image

from backend.typingcolors import TypingColors
from random import choices

PRINTABLE = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~\t"


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
        """Generates a int key from the string"""
        if key == "":
            key = ''.join(choices(PRINTABLE, k=16))
            print(key)
        return int.from_bytes(key.encode(), "little")

    def __getitem__(self, item):
        """Returns the color from char/char from color"""
        if item not in self.palette and isinstance(item, str):
            return self.palette["?"]
        return self.palette[item]  # raise keyerror if invalid decryption key


def typingcolors_load(file_path, key):
    """
    Returns the backend object created from loading image in file path.

    Takes in a file path to the image and the decryption key
    returns TypingColors object if key and image works, raises KeyError otherwise
    """
    img = Image.open(file_path).convert("RGBA")
    w, h = img.size
    object = TypingColors(img)
    object.set_encryption(key)  # load the key
    imgarr = np.array(img).reshape(-1, 4)
    # get the text
    chararr = np.zeros(imgarr.shape[0], dtype=str)
    for key, val in object.palette.palette.items():
        if isinstance(key, tuple):
            r, g, b, a = key
            cond = (
                (imgarr[:, 0] == r)
                & (imgarr[:, 1] == g)
                & (imgarr[:, 2] == b)
                & (imgarr[:, 3] == a)
            )
            chararr[cond.nonzero()[0]] = val
    if (chararr == "").any():
        raise KeyError
    decoded_text = "".join(chararr).rstrip()
    # split into rows and turning spaces to newlines
    decoded_chunks = [decoded_text[i : i + w] for i in range(0, len(decoded_text), w)]
    decoded_text = "".join(
        [
            (line.rstrip() + "\n") if line.endswith(" ") else line
            for line in decoded_chunks
        ]
    )
    object.update(decoded_text)
    return object, decoded_text  # return the text for the gui
