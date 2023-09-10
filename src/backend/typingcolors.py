from difflib import ndiff

import numpy as np
from PIL import Image, ImageDraw, ImageTk

import backend


class TypingColors:
    """The main backend object."""

    def __init__(self, img=None):
        self.text = ""
        self.ar_width, self.ar_height = self.width, self.height = self.size = (
            8,
            9,
        )  # aspect ratio & size
        self.canvas = (
            img.convert("RGBA") if img else Image.new("RGBA", self.size, (0, 0, 0, 0))
        )
        self.canvas_drawer = ImageDraw.Draw(self.canvas)

    def _idx2coord(self, idx):
        """
        Helper that converts string index to 2d image coordinate

        Example: 200 => X: 30, Y: 2
        """
        return [idx % self.width, idx // self.width]

    def set_key(self, key: str):
        """Sets the encryption key"""
        self.key = key
        self.palette = backend.utils.Palette(key)

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

    def force_update(self):
        """Re-draws the entire canvas"""
        text = self.text
        self.text = ""
        self.update(text)

    def img_scaled(self, scale_factor=10, max_width: int = 0):
        """Returns scaled TkImage for GUI"""
        if not scale_factor:
            scale_factor = 10
        size = (int(self.ar_width * scale_factor), int(self.ar_height * scale_factor))
        if max_width:
            if (
                size[0] > max_width
            ):  # Don't allow image to take more than 60% of the window width
                size[0] = max_width
        return ImageTk.PhotoImage(self.canvas.resize(size, Image.BOX))

    def save_as(self, filename):
        """Export to png"""
        self.canvas.load()[-1, -1] = (8, 8, 8, 8)
        self.canvas.save(filename)

    def decode(self):
        """Decoder method"""
        w, h = self.canvas.size
        self.canvas.load()[-1, -1] = (0, 0, 0, 0)
        self.imgarr = np.array(self.canvas).reshape(-1, 4)
        # get the text
        chararr = np.zeros(self.imgarr.shape[0], dtype=str)
        for key, val in self.palette.palette.items():
            r, g, b, a = val
            cond = (
                (self.imgarr[:, 0] == r)
                & (self.imgarr[:, 1] == g)
                & (self.imgarr[:, 2] == b)
                & (self.imgarr[:, 3] == a)
            )
            chararr[cond.nonzero()[0]] = key
        if (chararr == "").any():
            raise KeyError
        decoded_text = "".join(chararr).rstrip()
        # split into rows and turning spaces to newlines
        decoded_chunks = [
            decoded_text[i : i + w] for i in range(0, len(decoded_text), w)
        ]
        decoded_text = "".join(
            [
                (line.rstrip() + "\n") if line.endswith(" ") else line
                for line in decoded_chunks
            ]
        )
        self.update(decoded_text)
        return decoded_text
