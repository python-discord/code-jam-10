from difflib import ndiff
from random import randrange

from PIL import Image, ImageDraw


class PaintingColors:
    """The main backend object."""

    def __init__(self):
        self.text = ""
        self.size = (85, 110)
        self.width, self.height = self.size
        self.canvas = Image.new("RGBA", self.size, (0, 0, 0, 0))
        self.canvas_drawer = ImageDraw.Draw(self.canvas)
        self.pallete = {}  # maps characters to colours

    def _idx2coord(self, idx):
        """
        Helper that converts string index to 2d image coordinate

        Example: 200 => X: 30, Y: 2
        """
        return (idx % self.width, idx // self.width)

    def _pallete_check(self, char):
        """Returns the mapped colour to the char"""
        if char == ' ':
            color = (0, 0, 0, 0)  # transparent whitespace
        elif char not in self.pallete:  # adding to the pallete
            color = (randrange(256), randrange(256), randrange(256), 255)
            self.pallete[char] = color
        else:  # character already exists
            color = self.pallete[char]
        return color

    def update(self, text):
        """Makes changes to the image from the new text"""
        # stores all pixels needed to be changed
        to_remove = {}
        to_insert = {}

        # loop through ndiff to get needed changes
        for pos, diff in enumerate(ndiff(self.text, text)):
            operation, char = diff[0], diff[-1]
            if operation in ('+', ' '):
                to_insert[pos] = char
            else:
                to_remove[pos] = char

        for pos, char in to_remove.items():
            self.canvas_drawer.point(self._idx2coord(pos), (0, 0, 0, 0))
            for ipos in list(to_insert):  # avoid dict keys changed during iter
                if ipos >= pos:  # shift insert left if pos greater
                    to_insert[ipos-1] = to_insert[ipos]
                    del to_insert[ipos]

        for pos, char in to_insert.items():
            color = self._pallete_check(char)
            self.canvas_drawer.point(self._idx2coord(pos), color)

        # remove pixels out of updated text range
        # if updated text is longer than old text
        for pos in range(len(text), len(self.text)):
            self.canvas_drawer.point(self._idx2coord(pos), (0, 0, 0, 0))

        self.text = text  # update old to new text

# for testing
# test = PaintingColors()
# while True:
#     test.update(input("> "))
#     ImageShow.show(test.canvas)
