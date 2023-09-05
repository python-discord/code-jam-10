from enum import Enum
from typing import NamedTuple

import numpy as np
from PIL import Image


class Color(NamedTuple):
    r: int
    g: int
    b: int

    def __int__(self) -> int:
        return (self.r << 0) + (self.g << 8) + (self.b << 16)


class ColorChange(NamedTuple):
    hue: int
    lightness: int


#         lightness hue
#              v     v
PIET_COLORS: tuple[tuple[Color, ...], ...] = (
    (
        Color(255, 192, 192),
        Color(255, 255, 192),
        Color(192, 255, 192),
        Color(192, 255, 255),
        Color(192, 192, 255),
        Color(255, 192, 255),
    ),
    (
        Color(255, 000, 000),
        Color(255, 255, 000),
        Color(000, 255, 000),
        Color(000, 255, 255),
        Color(000, 000, 255),
        Color(255, 000, 255),
    ),
    (
        Color(192, 000, 000),
        Color(192, 192, 000),
        Color(000, 192, 000),
        Color(000, 192, 192),
        Color(000, 000, 192),
        Color(192, 000, 192),
    ),
)


class PietCommand(Enum):
    NONE = Color(255, 255, 255)
    BLOCK = Color(0, 0, 0)
    PUSH = ColorChange(0, 1)
    POP = ColorChange(0, 2)
    ADD = ColorChange(1, 0)
    SUBTRACT = ColorChange(1, 1)
    MULTIPLY = ColorChange(1, 2)
    DIVIDE = ColorChange(2, 0)
    MOD = ColorChange(2, 1)
    NOT = ColorChange(2, 2)
    GREATER = ColorChange(3, 0)
    POINTER = ColorChange(3, 1)
    SWITCH = ColorChange(3, 2)
    DUPLICATE = ColorChange(4, 0)
    ROLL = ColorChange(4, 1)
    IN_NUMBER = ColorChange(4, 2)
    IN_CHAR = ColorChange(5, 0)
    OUT_NUMBER = ColorChange(5, 1)
    OUT_CHAR = ColorChange(5, 2)


class PietProgram:
    def __init__(self, size: tuple[int, int]):
        self.commands = np.empty(size, dtype=PietCommand)
        self.size = size
        # self.current_x = 0
        # self.current_y = 0

    def add_command(self, command: PietCommand, position: tuple[int, int]):
        # self.commands[self.current_y][self.current_x] = command
        x, y = position
        self.commands[y][x] = command

    @property
    def colors(self) -> list[list[Color]]:
        colors = []
        current_hue = 0
        current_lightness = 0
        previous_color = PietCommand.BLOCK.value
        for row in self.commands:
            color_row = []
            for command in row:
                if command is None:
                    color_row.append(previous_color)
                elif isinstance(command.value, ColorChange):
                    if previous_color not in (PietCommand.BLOCK.value, PietCommand.NONE.value):
                        current_hue = (current_hue + command.value.hue) % 6
                        current_lightness = (current_lightness + command.value.lightness) % 3
                    color = PIET_COLORS[current_lightness][current_hue]
                    color_row.append(color)
                    previous_color = color
                elif isinstance(command.value, Color):
                    color_row.append(command.value)
                    previous_color = command.value
            colors.append(color_row)
        return colors


def colors_to_image(colors: list[list[Color]]) -> Image.Image:
    x = [int(color) for row in colors for color in row]
    # return Image.fromarray(np.array(x), mode="RGB")
    image = Image.new("RGB", (len(colors[0]), len(colors)))
    image.putdata(x)
    return image


def generate_image(data: bytes) -> Image.Image:
    # Construct a Piet program that outputs the data given.
    # TODO: Figure out how to split the data into multiple lines of pixels.
    program = PietProgram((3, 1024))
    x = 0
    y = 0
    for i, byte in enumerate(data):
        program.commands[y][x] = PietCommand.OUT_CHAR
        program.commands[y][x + byte] = PietCommand.PUSH
        x += byte + 1
        if i == len(data) - 1:
            program.commands[y][x] = PietCommand.OUT_CHAR
            program.commands[y][x + 1] = PietCommand.NONE

    # Add a terminating block of pixels to the end.
    program.commands[0][-1] = PietCommand.BLOCK
    program.commands[1][0] = PietCommand.NONE
    program.commands[1][-4] = PietCommand.BLOCK
    program.commands[1][-3:-1] = PietCommand.NONE
    program.commands[1][-1] = PietCommand.BLOCK
    program.commands[2][0] = PietCommand.NONE
    program.commands[2][-4:] = PietCommand.BLOCK

    colors = program.colors
    return colors_to_image(colors)


if __name__ == "__main__":
    # Run this file to generate a Piet program.
    # Test using https://piet.bubbler.one.
    # TODO: Make our own Piet interpreter according to the spec at https://esolangs.org/wiki/Piet.

    # with open(__file__, "rb") as file:
    #     data = file.read()
    # encoded = generate_image(data)
    encoded = generate_image(b"hi")
    encoded.save(f"{__file__}.png")
    encoded.show()
