# TODO: support newlines
import io, string
from difflib import ndiff
from random import choices

from PIL import Image, ImageDraw

class TypingColors:
    """The main backend object."""

    def __init__(self, key=None, img=None):
        self.text = ""
        if img is None:  # start blank
            self.size = (30, 45)
            self.canvas = Image.new("RGBA", self.size, (0, 0, 0, 0))
        else:
            self.size = img.size
            self.canvas = img
        self.width, self.height = self.size
        self.canvas_drawer = ImageDraw.Draw(self.canvas)
        self.palette = {}  # maps characters to colours
        self.key = self._generate_key(key if key else ''.join(choices(string.printable, k=16))) # The encryption key/code for the image

    def _generate_key(self, s:str="", byteorder='little'):
        if s == "": raise ValueError("String for encryption cannot be empty")
        return int.from_bytes(s.encode(), byteorder) # or big

    def _idx2coord(self, idx):
        """
        Helper that converts string index to 2d image coordinate

        Example: 200 => X: 30, Y: 2
        """
        return [idx % self.width, idx // self.width]

    def _palette_check(self, char:str):
        """Generates a palette of colors based on the key"""
        if char == " ": # transparent whitespace
            color = (0, 0, 0, 0,)
        elif char not in self.palette: # adding to palette
            val = self.key + (string.printable.index(char)*10)
            sub = 255 + string.printable.index(char) # Making colors more distinctive
            r = val % sub
            g = (val // 255) % sub
            b = ((val // 255) // 255) % sub
            color = (r, g, b, 255)
            self.palette[char] = color
        else:  # character already exists
            color = self.palette[char]
        return color

    def update(self, text):
        """Makes changes to the image from the new text"""
        insertions = {}  # stores pixels to be inserted, process deletions first

        # preprocess new text
        text = ''.join([i+(' '*(self.width-len(i))) for i in text.split('\n')]).rstrip()

        # loop through ndiff to get needed changes
        pos = 0
        for original_pos, diff in enumerate(ndiff(self.text, text)):
            operation, char = diff[0], diff[-1]
            # can't use modified text length here
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
            color = self._palette_check(char)
            self.canvas_drawer.point(self._idx2coord(pos), color)

        # remove pixels out of updated text range
        # if text is longer than new text
        for pos in range(len(text), len(self.text)):
            self.canvas_drawer.point(self._idx2coord(pos), (0, 0, 0, 0))

        self.text = text  # update old to new text

    def img_scaled(self, size=(390, 585)):  # size around half the gui window
        """Returns scaled PNG bytes of image for GUI"""
        bio = io.BytesIO()
        self.canvas.resize(size, Image.BOX).save(bio, format='PNG')
        return bio.getvalue()
    
    def set_encryption(self, encryption):
        self.encryption_key = encryption
