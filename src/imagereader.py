import collections

import numpy as np

from PIL import Image, PyAccess
from pinterpret import PietRuntime
from piet import PietCommand, Color


class Reader:
    def __init__(self, im: Image.Image) -> None:
        self.im_rgb = im.convert("RGB")
        self.current = self.im_rgb.getpixel((0, 0))

    def color_block_size(self, pos: tuple[int, int]):
        "returns size of a color block, given a codel in a color block with position [row, column]"
        im = self.im_rgb
        y, x = pos
        im_array = np.asarray(im)
        pixel = im_array[y][x]

        rows, cols = len(im_array), len(im_array[0])
        visited = set()

        size = 1
        q = collections.deque()
        visited.add((y, x))
        q.append((y, x))
        while q:
            row, col = q.popleft()
            directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if (r in range(rows) and
                        c in range(cols) and
                        np.array_equal(im_array[r, c], pixel) and
                        (r, c) not in visited):
                    q.append((r, c))
                    visited.add((r, c))
                    size += 1

        return size

    def smallest_codel(self) -> int:
        "returns side-length in pixels of the smallest codel"
        im = self.im_rgb
        im_array = np.asarray(im)
        pixel = im_array[0][0]
        rows, cols = len(im_array), len(im_array[0])
        smallest = rows

        rsf = 0
        for r in range(rows):
            for c in range(cols):
                if c == 0:
                    pixel = im_array[r][c]
                    rsf = 0
                next = im_array[r][c]
                if np.array_equal(next, pixel):
                    rsf += 1
                else:
                    if rsf < smallest:
                        smallest = rsf
                        pixel = im_array[r][c]
                        rsf = 1

        rsf = 0
        for c in range(cols):
            for r in range(rows):
                if r == 0:
                    pixel = im_array[r][c]
                    rsf = 0
                next = im_array[r][c]
                if np.array_equal(next, pixel):
                    rsf += 1
                else:
                    if rsf < smallest:
                        smallest = rsf
                        pixel = im_array[r][c]
                        rsf = 1

        return smallest

    def image_size(self) -> (int, int):
        "returns size of image after scaling it down to a codel size of 1 pixel"
        im = self.im_rgb
        width, height = im.size
        codel_size = self.smallest_codel()
        return (width // codel_size, height // codel_size)