from collections import deque
from typing import NamedTuple

from PIL import Image

from .common import Color, OrderedPair
from .runtime import PointerDirection


class Codel(NamedTuple):
    color: Color
    pixels: set[OrderedPair]

    def __len__(self) -> int:
        return len(self.pixels)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(size={len(self)}, color={self.color})"


class ImageReader:
    def __init__(self, image: Image.Image) -> None:
        colors: list[list[Color]] = []
        for y in range(image.height):
            row = []
            for x in range(image.width):
                row.append(Color(*image.getpixel((x, y))))
            colors.append(row)
        self.colors = colors

    def codel_info(self, pos: OrderedPair, /) -> Codel:
        """Return information about the codel that contains pos (y,x)."""
        colors = self.colors
        color = colors[pos.y][pos.x]

        height, width = len(colors), len(colors[0])
        y_range = range(height)
        x_range = range(width)
        visited: set[OrderedPair] = set()

        queue = deque()
        visited.add(pos)
        queue.append(pos)
        while queue:
            pos = queue.popleft()
            for direction in PointerDirection:
                offset_pos = pos + direction.value
                if (
                    offset_pos.y in y_range
                    and offset_pos.x in x_range
                    and colors[offset_pos.y][offset_pos.x] == color
                    and offset_pos not in visited
                ):
                    queue.append(offset_pos)
                    visited.add(offset_pos)

        return Codel(color, visited)

    def smallest_codel(self) -> int:
        """Return the side length in pixels of the smallest codel."""
        colors = self.colors
        pixel = colors[0][0]
        height, width = len(colors), len(colors[0])
        smallest = height

        rsf = 0
        for y in range(height):
            for x in range(width):
                if x == 0:
                    pixel = colors[y][x]
                    rsf = 0
                next = colors[y][x]
                if next == pixel:
                    rsf += 1
                else:
                    if rsf < smallest:
                        smallest = rsf
                        pixel = colors[y][x]
                        rsf = 1

        rsf = 0
        for x in range(width):
            for y in range(height):
                if y == 0:
                    pixel = colors[y][x]
                    rsf = 0
                next = colors[y][x]
                if next == pixel:
                    rsf += 1
                else:
                    if rsf < smallest:
                        smallest = rsf
                        pixel = colors[y][x]
                        rsf = 1

        return smallest

    def image_size(self) -> OrderedPair:
        """Return the size of image after scaling it down to a codel size of 1 pixel."""
        height, width = len(self.colors), len(self.colors[0])
        codel_size = self.smallest_codel()
        return OrderedPair(width // codel_size, height // codel_size)
