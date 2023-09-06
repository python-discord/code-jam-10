from difflib import ndiff
from io import BytesIO
from random import choices

from PIL import Image, ImageDraw, ImageTk

PRINTABLE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t'


class Palette:
    """Pallete object to map chars to colours"""

    palette = {" ": (0, 0, 0, 0), (0, 0, 0, 0): " "}

    def __init__(self, key: str = None):
        """Maps all characters to colours using the key"""
        if not key:
            key = "".join(choices(PRINTABLE, k=16))
        if not (3 < len(key) < 25):
            raise ValueError("key should be between 4 and 24 characters")

        # self.keylen = len(key) * 8
        self.key = self._generate_key(key)
        # print(self.key)

        for n, char in enumerate(PRINTABLE):  # generate pallete
            val = self.key + n**n  # * (n**self.keylen)  # % (255 * 255 * 255 * 64)
            # print(val)
            r, g, b, a = (
                (val & 255),
                (val >> 8) & 255,
                (val >> 16) & 255,
                (val >> 20) & 63,
            )
            # print(r, g, b, a)
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



class TypingColors:
    """The main backend object."""

    def __init__(self, img=None):
        self.text = ""
        self.size = (8, 9)
        if img is None:  # start blank
            self.canvas = Image.new("RGBA", self.size, (0, 0, 0, 0))
        else:
            self.canvas = img
        self.ar_width, self.ar_height = self.size  # aspecct ratio
        self.width, self.height = self.size
        self.canvas_drawer = ImageDraw.Draw(self.canvas)
        self.palette = None  # will be set later
        self.key = None

    def _idx2coord(self, idx):
        """
        Helper that converts string index to 2d image coordinate

        Example: 200 => X: 30, Y: 2
        """
        return [idx % self.width, idx // self.width]

    def set_encryption(self, key: str = None):
        """Sets the encryption key"""
        self.key = key
        self.palette = Palette(key)

    def update(self, new_text):
        """Makes changes to the image from the new text"""
        # deal with newlines - simply turn them to spaces
        text = ''.join([
            i + (' ' * (self.width - len(i) % self.width)) for i in new_text.split('\n')
        ]).rstrip()
        textlen = len(text)

        # check if text too big
        if textlen/self.width > self.height:
            # expand till fit
            while textlen/self.width > self.height:
                self.width += self.ar_width
                self.height += self.ar_height
                self.size = (self.width, self.height)
                textlen = sum([max(len(i), self.width) for i in new_text.split('\n')])
            # redraw the canvas
            self.canvas = Image.new("RGBA", self.size)
            self.canvas_drawer = ImageDraw.Draw(self.canvas)
            self.text = ''
            text = ''.join([
                i + (' ' * (self.width - len(i) % self.width)) for i in new_text.split('\n')
            ]).rstrip()

        # check if text too small
        textlen = sum([max(len(i), self.width-self.ar_width) for i in new_text.split('\n')])
        if self.height > self.ar_height and (textlen/(self.width-self.ar_width)) < self.height-self.ar_height:
            # shrink till fit
            while self.height > self.ar_height and (textlen/(self.width-self.ar_width)) < self.height-self.ar_height:
                self.width -= self.ar_width
                self.height -= self.ar_height
                self.size = (self.width, self.height)
                textlen = sum([max(len(i), self.width-self.ar_width) for i in new_text.split('\n')])
            # redraw the canvas
            self.canvas = Image.new("RGBA", self.size)
            self.canvas_drawer = ImageDraw.Draw(self.canvas)
            self.text = ''
            text = ''.join([
                i + (' ' * (self.width - len(i) % self.width)) for i in new_text.split('\n')
            ]).rstrip()

        # stores pixels to be updated, process deletions first
        insertions = {}
        deletions = []
        # loop through ndiff to get needed changes
        pos = 0
        for original_pos, diff in enumerate(ndiff(self.text, text)):
            operation, char = diff[0], diff[-1]
            original_char = self.text[pos] if pos < len(self.text) else None
            coords = self._idx2coord(pos)

            if operation == '-':  # remove char (make it transparent again)
                deletions += coords
                pos -= 1  # shift the rest of the pixels left
            elif operation == '+':  # add char
                insertions.setdefault(char, [])
                insertions[char] += coords
            elif original_pos != pos or original_char != char:
                # shift left if removed before/replace if char is different
                insertions.setdefault(char, [])
                insertions[char] += coords

            # move to next pixel to process
            pos += 1

        # process all changes
        if deletions:
            self.canvas_drawer.point(deletions, (0, 0, 0, 0))  # transparent removed

        for char, coords in insertions.items():
            color = self.palette[char]
            self.canvas_drawer.point(coords, color)

        # remove pixels out of updated text range
        # if text is longer than new text
        for pos in range(len(text), len(self.text)):
            self.canvas_drawer.point(self._idx2coord(pos), (0, 0, 0, 0))

        self.text = text  # update old to new text

    def img_scaled(self, scale_factor=35):  # size around half the gui window
        """Returns scaled PNG bytes of image for GUI"""
        bio = BytesIO()
        size = (self.ar_width * scale_factor, self.ar_height * scale_factor)
        self.canvas.resize(size, Image.BOX).save(bio, format='PNG')
        return bio.getvalue()

    def img_tk(self, scale_factor=35):
        """Same as img_scaled but for tkinter"""
        size = (self.ar_width * scale_factor, self.ar_height * scale_factor)
        return ImageTk.PhotoImage(self.canvas.resize(size, Image.BOX))
