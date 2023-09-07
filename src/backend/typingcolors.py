from difflib import ndiff

from PIL import Image, ImageDraw, ImageTk

import backend


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

    def _idx2coord(self, idx):
        """
        Helper that converts string index to 2d image coordinate

        Example: 200 => X: 30, Y: 2
        """
        return [idx % self.width, idx // self.width]

    def set_encryption(self, key: str):
        """Sets the encryption key"""
        self.key = key
        self.palette = backend.typingcolors_utils.Palette(key)

    def update(self, new_text):
        """Makes changes to the image from the new text"""
        # deal with newlines - simply turn them to spaces
        text = "".join(
            [
                i + (" " * (self.width - len(i) % self.width))
                for i in new_text.split("\n")
            ]
        ).rstrip()
        textlen = len(text)

        # check if text too big
        if textlen / self.width > self.height:
            # expand till fit
            while textlen / self.width > self.height:
                self.width += self.ar_width
                self.height += self.ar_height
                self.size = (self.width, self.height)
                textlen = sum([max(len(i), self.width) for i in new_text.split("\n")])
            # redraw the canvas
            self.canvas = Image.new("RGBA", self.size)
            self.canvas_drawer = ImageDraw.Draw(self.canvas)
            self.text = ""
            text = "".join(
                [
                    i + (" " * (self.width - len(i) % self.width))
                    for i in new_text.split("\n")
                ]
            ).rstrip()

        # check if text too small
        textlen = sum(
            [max(len(i), self.width - self.ar_width) for i in new_text.split("\n")]
        )
        if (
            self.height > self.ar_height
            and (textlen / (self.width - self.ar_width)) < self.height - self.ar_height
        ):
            # shrink till fit
            while (
                self.height > self.ar_height
                and (textlen / (self.width - self.ar_width))
                < self.height - self.ar_height
            ):
                self.width -= self.ar_width
                self.height -= self.ar_height
                self.size = (self.width, self.height)
                textlen = sum(
                    [
                        max(len(i), self.width - self.ar_width)
                        for i in new_text.split("\n")
                    ]
                )
            # redraw the canvas
            self.canvas = Image.new("RGBA", self.size)
            self.canvas_drawer = ImageDraw.Draw(self.canvas)
            self.text = ""
            text = "".join(
                [
                    i + (" " * (self.width - len(i) % self.width))
                    for i in new_text.split("\n")
                ]
            ).rstrip()

        # stores pixels to be updated, process deletions first
        insertions = {}
        deletions = []
        # loop through ndiff to get needed changes
        pos = 0
        for original_pos, diff in enumerate(ndiff(self.text, text)):
            operation, char = diff[0], diff[-1]
            original_char = self.text[pos] if pos < len(self.text) else None
            coords = self._idx2coord(pos)

            if operation == "-":  # remove char (make it transparent again)
                deletions += coords
                pos -= 1  # shift the rest of the pixels left
            elif operation == "+":  # add char
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

    # def img_scaled(self, scale_factor=35):  # size around half the gui window
    #     """Returns scaled PNG bytes of image for GUI"""
    #     bio = BytesIO()
    #     size = (self.ar_width * scale_factor, self.ar_height * scale_factor)
    #     self.canvas.resize(size, Image.BOX).save(bio, format='PNG')
    #     return bio.getvalue()

    def img_scaled(self, scale_factor=35):
        """Returns scaled TkImage for GUI"""
        size = (self.ar_width * scale_factor, self.ar_height * scale_factor)
        return ImageTk.PhotoImage(self.canvas.resize(size, Image.BOX))
