# TODO: support newlines
from difflib import ndiff
from random import randrange

from PIL import Image, ImageDraw


class TypingColors:
    """The main backend object."""

    def __init__(self, img=None):
        self.text = ""
        if img is None:  # start blank
            self.size = (25, 50)
            self.canvas = Image.new("RGBA", self.size, (0, 0, 0, 0))
        else:
            self.size = img.size
            self.canvas = img
        self.width, self.height = self.size
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
        # stores all pixels needed to be changed in list of (index, char)
        to_remove = []
        to_insert = []

        # loop through ndiff to get needed changes
        for pos, diff in enumerate(ndiff(self.text, text)):
            operation, char = diff[0], diff[-1]
            if operation in ('+', ' '):
                to_insert.append([pos, char])
            else:
                to_remove.append([pos, char])

        for pos, char in to_remove:
            for n, (ipos, _) in enumerate(to_insert):
                if ipos >= pos:  # shift insert left
                    to_insert[n][0] -= 1

        for pos, char in to_insert:
            color = self._pallete_check(char)
            self.canvas_drawer.point(self._idx2coord(pos), color)

        # remove pixels out of updated text range
        # if updated text is longer than old text
        for pos in range(len(text), len(self.text)):
            self.canvas_drawer.point(self._idx2coord(pos), (0, 0, 0, 0))

        self.text = text  # update old to new text

# for testing
# from PIL import ImageShow
# test = TypingColors()
# while True:
#     test.update(input("> "))
#     ImageShow.show(test.canvas)
