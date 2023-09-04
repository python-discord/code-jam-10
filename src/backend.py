import string
from difflib import ndiff
from io import BytesIO
from random import choices

from PIL import Image, ImageDraw


class Pallete:
    """Pallete object to map chars to colours"""

    def __init__(self, key=None):
        self.palette = {}
        self.rgbtocol = {(0, 0, 0): ' '}

        if key:
            self.key = self._generate_key(key)
        else:
            self.key = self._generate_key(''.join(choices(string.printable, k=16)))

        for n, char in enumerate(string.printable):  # generate pallete
            val = (self.key * (n + 1)) % 16777216  # 16777216=256^3
            r, g, b = (val & 255), (val >> 8) & 255, (val >> 16) & 255
            color = (r, g, b, 255)
            self.palette[char] = color
            self.rgbtocol[(r, g, b)] = char

    def _generate_key(self, key):
        """Generates a int key from the string"""
        if not key:
            raise ValueError("String for encryption cannot be empty")
        return int.from_bytes(key.encode(), 'little')

    def __getitem__(self, char):
        """Returns the color from char"""
        if char == " ":  # transparent whitespace
            color = (0, 0, 0, 0)
        else:
            color = self.palette[char]
        return color


class TypingColors:
    """The main backend object."""

    def __init__(self, img=None, key=None):
        self.text = ""
        if img is None:  # start blank
            self.size = (30, 45)
            self.canvas = Image.new("RGBA", self.size, (0, 0, 0, 0))
        else:
            self.size = img.size
            self.canvas = img
        self.width, self.height = self.size
        self.canvas_drawer = ImageDraw.Draw(self.canvas)
        self.palette = Pallete(key)  # maps characters to colours

    def _idx2coord(self, idx):
        """
        Helper that converts string index to 2d image coordinate

        Example: 200 => X: 30, Y: 2
        """
        return [idx % self.width, idx // self.width]

    def update(self, text):
        """Makes changes to the image from the new text"""
        insertions = {}  # stores pixels to be inserted, process deletions first

        # deal with newlines - simply turn them to spaces
        text = ''.join([i+(' '*(self.width-len(i))) for i in text.split('\n')]).rstrip()

        # loop through ndiff to get needed changes
        pos = 0
        for original_pos, diff in enumerate(ndiff(self.text, text)):
            operation, char = diff[0], diff[-1]
            original_char = self.text[pos] if pos < len(self.text) else None

            if operation == '-':  # remove char (make it transparent again)
                self.canvas_drawer.point(self._idx2coord(pos), (0, 0, 0, 0))
                pos -= 1  # shift the rest of the pixels left
            elif operation == '+':  # add char
                insertions[pos] = char
            elif original_pos != pos or original_char != char:
                # shift left if removed before/replace if char is different
                insertions[pos] = char

            # move to next pixel to process
            pos += 1

        for pos, char in insertions.items():  # process inserts/replaces
            color = self.palette[char]
            self.canvas_drawer.point(self._idx2coord(pos), color)

        # remove pixels out of updated text range
        # if text is longer than new text
        for pos in range(len(text), len(self.text)):
            self.canvas_drawer.point(self._idx2coord(pos), (0, 0, 0, 0))

        self.text = text  # update old to new text

    def img_scaled(self, size=(390, 585)):  # size around half the gui window
        """Returns scaled PNG bytes of image for GUI"""
        bio = BytesIO()
        self.canvas.resize(size, Image.BOX).save(bio, format='PNG')
        return bio.getvalue()
