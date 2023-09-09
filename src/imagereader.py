import collections
from typing import NamedTuple, Tuple

import numpy as np
from PIL import Image

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class CodelInfo(NamedTuple):
    size: int
    color: tuple[int, int, int]
    pixels: set

    def __repr__(self) -> str:
        return f"CodelInfo(size={self.size}, color={self.color})"


class Reader:
    def __init__(self, im: Image.Image) -> None:
        self.im_array = np.asarray(im.convert("RGB"))

    def codel_info(self, pos: tuple[int, int]) -> CodelInfo:
        "returns information about the codel that contains pos(y,x)"
        y, x = pos
        im_array = self.im_array
        pixel = im_array[y][x]

        rows, cols, *_ = im_array.shape
        visited = set()

        size = 1
        q = collections.deque()
        visited.add((y, x))
        q.append((y, x))
        while q:
            row, col = q.popleft()
            for dr, dc in DIRECTIONS:
                r, c = row + dr, col + dc
                if (
                    r in range(rows)
                    and c in range(cols)
                    and np.array_equal(im_array[r, c], pixel)
                    and (r, c) not in visited
                ):
                    q.append((r, c))
                    visited.add((r, c))
                    size += 1

        r, g, b = pixel
        return CodelInfo(size, (r, g, b), visited)

    def smallest_codel(self) -> int:
        "returns side-length in pixels of the smallest codel"
        im_array = self.im_array
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

    def image_size(self) -> Tuple[int, int]:
        "returns size of image after scaling it down to a codel size of 1 pixel"
        height, width = self.im_array.shape
        codel_size = self.smallest_codel()
        return (width // codel_size, height // codel_size)
