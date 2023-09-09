from enum import Enum
from io import StringIO
from typing import NamedTuple

import numpy as np
from PIL import Image

from pinterpret import PietInterpreter, PietRuntime, PointerDirection, StepLimitReached


def color_to_int(color) -> int:
    return int(color[0] << 0) + int(color[1] << 8) + int(color[2] << 16)


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
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)


class PietCommand(Enum):
    _PREVIOUS = -1
    _NONE = 0
    NOOP = Color(255, 255, 255)
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


class PietProgramGenerator:
    def __init__(self):
        # self.commands = np.full(size, PietCommand._NONE, dtype=PietCommand)
        self.commands = np.full((2, 2), PietCommand._NONE, dtype=PietCommand)
        self.colors = np.full((2, 2), WHITE, dtype=np.dtype((np.uint8, 3)))
        # self.size = size
        self._interpreter = PietInterpreter(self.image, debug=False)
        self._current_hue = 0
        self._current_lightness = 0
        self._previous_color = WHITE

    # @property
    # def current_command(self) -> PietCommand:
    #     y, x = self.interpreter.position
    #     return self.commands[y][x]

    def set_next_command(self, command: PietCommand, multiplier: int = 1, offset: tuple[int, int] = (0, 0)):
        if multiplier < 1:
            return
        # Update the reader with our current image.
        self._interpreter.reader.im_array = self.colors
        # Simulate steps to move the pointer.
        next_y, next_x = self._interpreter._next_move()
        next_command = self.commands[next_y][next_x]
        while next_command is not PietCommand._NONE:
            self._interpreter.step()
            next_y, next_x = self._interpreter._next_move()
            try:
                next_command = self.commands[next_y][next_x]
            except IndexError:
                next_command = PietCommand._NONE
        # Next command is now NONE (0)
        y, x = np.add((next_y, next_x), offset)
        self.set_command(command, (y, x))

        if multiplier > 1:
            if self._interpreter.runtime.pointer.direction is PointerDirection.RIGHT:
                if x + multiplier + 1 >= self.commands.shape[1]:
                    self.commands = np.hstack(
                        (
                            self.commands,
                            np.full(
                                (self.commands.shape[0], x + multiplier + 1 - self.commands.shape[1]),
                                PietCommand._NONE,
                                dtype=PietCommand,
                            ),
                        )
                    )
                    self.colors = np.hstack(
                        (
                            self.colors,
                            np.full(
                                (self.colors.shape[0], x + multiplier + 1 - self.colors.shape[1]),
                                WHITE,
                                dtype=np.dtype((np.uint8, 3)),
                            ),
                        )
                    )
                self.commands[y, x + 1 : x + multiplier] = PietCommand._PREVIOUS
                self.colors[y, x + 1 : x + multiplier] = self._previous_color
            elif self._interpreter.runtime.pointer.direction is PointerDirection.LEFT:
                self.commands[y, x - multiplier + 1 : x] = PietCommand._PREVIOUS
                self.colors[y, x - multiplier + 1 : x] = self._previous_color
            elif self._interpreter.runtime.pointer.direction is PointerDirection.DOWN:
                if y + multiplier + 1 >= self.commands.shape[0]:
                    self.commands = np.vstack(
                        (
                            self.commands,
                            np.full(
                                (y + multiplier + 1 - self.commands.shape[0], self.commands.shape[1]),
                                PietCommand._NONE,
                                dtype=PietCommand,
                            ),
                        )
                    )
                    self.colors = np.vstack(
                        (
                            self.colors,
                            np.full(
                                (y + multiplier + 1 - self.colors.shape[0], self.colors.shape[1]),
                                WHITE,
                                dtype=np.dtype((np.uint8, 3)),
                            ),
                        )
                    )
                self.commands[y + 1 : y + multiplier, x] = PietCommand._PREVIOUS
                self.colors[y + 1 : y + multiplier, x] = self._previous_color
            elif self._interpreter.runtime.pointer.direction is PointerDirection.UP:
                self.commands[y - multiplier + 1 : y, x] = PietCommand._PREVIOUS
                self.colors[y - multiplier + 1 : y, x] = self._previous_color
            else:
                raise ValueError("Invalid direction pointer position.")

    def set_command(self, command: PietCommand, position: tuple[int, int]):
        y, x = position
        if y + 1 >= self.commands.shape[0]:
            self.commands = np.vstack(
                (
                    self.commands,
                    np.full(
                        (y + 1 - self.commands.shape[0], self.commands.shape[1]), PietCommand._NONE, dtype=PietCommand
                    ),
                )
            )
            self.colors = np.vstack(
                (
                    self.colors,
                    np.full(
                        (y + 1 - self.colors.shape[0], self.colors.shape[1]), WHITE, dtype=np.dtype((np.uint8, 3))
                    ),
                )
            )
        if x + 1 >= self.commands.shape[1]:
            self.commands = np.hstack(
                (
                    self.commands,
                    np.full(
                        (self.commands.shape[0], x + 1 - self.commands.shape[1]), PietCommand._NONE, dtype=PietCommand
                    ),
                )
            )
            self.colors = np.hstack(
                (
                    self.colors,
                    np.full(
                        (self.colors.shape[0], x + 1 - self.colors.shape[1]), WHITE, dtype=np.dtype((np.uint8, 3))
                    ),
                )
            )
        self.commands[y][x] = command
        if isinstance(command.value, ColorChange):
            if self._previous_color not in (PietCommand.BLOCK.value, PietCommand.NOOP.value):
                self._current_hue = (self._current_hue + command.value.hue) % 6
                self._current_lightness = (self._current_lightness + command.value.lightness) % 3
            color = PIET_COLORS[self._current_lightness][self._current_hue]
        elif isinstance(command.value, Color):
            color = command.value
        else:
            color = WHITE
        self.colors[y][x] = color
        self._previous_color = color

    def set_offset_command(self, command: PietCommand, offset: tuple[int, int]):
        y, x = tuple(np.add(self._interpreter.position, offset))
        self.set_command(command, (y, x))

    # @property
    # def colors(self) -> list[list[Color]]:
    #     colors = []
    #     current_hue = 0
    #     current_lightness = 0
    #     previous_color = PietCommand.NOOP.value
    #     for row in self.commands:
    #         color_row = []
    #         for command in row:
    #             command: PietCommand
    #             if command is PietCommand._NONE:
    #                 color_row.append(PietCommand.NOOP.value)
    #             elif command is PietCommand._PREVIOUS:
    #                 color_row.append(previous_color)
    #             elif isinstance(command.value, ColorChange):
    #                 if previous_color not in (PietCommand.BLOCK.value, PietCommand.NOOP.value):
    #                     current_hue = (current_hue + command.value.hue) % 6
    #                     current_lightness = (current_lightness + command.value.lightness) % 3
    #                 color = PIET_COLORS[current_lightness][current_hue]
    #                 color_row.append(color)
    #                 previous_color = color
    #             elif isinstance(command.value, Color):
    #                 color_row.append(command.value)
    #                 previous_color = command.value
    #         colors.append(color_row)
    #     return colors

    @property
    def image(self) -> Image.Image:
        colors = self.colors
        x = [color_to_int(color) for row in colors for color in row]
        # return Image.fromarray(np.array(x), mode="RGB")
        image = Image.new("RGB", (len(colors[0]), len(colors)))
        image.putdata(x)
        return image


def generate_image(data: bytes) -> Image.Image:
    """Construct a Piet program that outputs the data given."""
    length = len(data)
    program = PietProgramGenerator()
    program.set_next_command(PietCommand.NOOP, 6)
    for i, byte in enumerate(data):
        program.set_next_command(PietCommand.NOOP, 256 - byte)
        # program._current_lightness = random.randint(0, 2)
        # program._current_hue = random.randint(0, 5)
        program.set_next_command(PietCommand.OUT_CHAR, byte)
        # program.set_next_command(random.choice([x for x in PietCommand if isinstance(x.value, ColorChange)]), byte)
        program.set_next_command(PietCommand.PUSH)
        program.set_next_command(PietCommand.OUT_CHAR, 1 + (2 * (i % 2)))
        program.set_next_command(PietCommand.PUSH)
        program.set_next_command(PietCommand.DUPLICATE)
        program.set_next_command(PietCommand.POINTER)
        program.set_next_command(PietCommand.POINTER)
        program.set_next_command(PietCommand.NOOP, 4 + (2 * (i % 2)))
        if i == length - 1:
            # Add a terminating block of pixels to the end.
            program.set_next_command(PietCommand.BLOCK)
            program.set_next_command(PietCommand.NOOP, 2)
            program.set_next_command(PietCommand.BLOCK)
            program.set_offset_command(PietCommand.BLOCK, (0, 1))
            program.set_offset_command(PietCommand.BLOCK, (-1, 1))
            program.set_next_command(PietCommand.NOOP)
            program.set_next_command(PietCommand.BLOCK)
            program.set_offset_command(PietCommand.BLOCK, (1, 0))
            program.set_offset_command(PietCommand.BLOCK, (-1, 0))

    return program.image


if __name__ == "__main__":
    # Run this file to generate a Piet program.
    # Test using https://piet.bubbler.one.

    with open(__file__, "rb") as file:
        input_data = file.read()[:256]
    # data = b"AB"
    encoded = generate_image(input_data)
    encoded.save(f"{__file__}.png")
    encoded.show()
    output_buffer = StringIO()
    interpreter = PietInterpreter(encoded, debug=True, runtime=PietRuntime(output_buffer=output_buffer))
    exc = interpreter.run()
    if isinstance(exc, StepLimitReached):
        raise exc
    assert output_buffer.getvalue().encode() == input_data
