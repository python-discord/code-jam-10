import sys
from enum import Enum
from io import BytesIO

from PIL import Image

from .common import BLACK, PIET_COLORS, WHITE, Color, ColorChange, OrderedPair, SelfExpandingList
from .interpreter import PietInterpreter
from .runtime import DirectionOffset, DirectionPointer, PointerDirection


class PietCommand(Enum):
    _PREVIOUS = -1
    _NONE = 0
    NOOP = Color(255, 255, 255)
    BLOCK = Color(0, 0, 0)
    PUSH = ColorChange(1, 0)
    POP = ColorChange(2, 0)
    ADD = ColorChange(0, 1)
    SUBTRACT = ColorChange(1, 1)
    MULTIPLY = ColorChange(2, 1)
    DIVIDE = ColorChange(0, 2)
    MOD = ColorChange(1, 2)
    NOT = ColorChange(2, 2)
    GREATER = ColorChange(0, 3)
    POINTER = ColorChange(1, 3)
    SWITCH = ColorChange(2, 3)
    DUPLICATE = ColorChange(0, 4)
    ROLL = ColorChange(1, 4)
    IN_NUMBER = ColorChange(2, 4)
    IN_CHAR = ColorChange(0, 5)
    OUT_NUMBER = ColorChange(1, 5)
    OUT_CHAR = ColorChange(2, 5)


class ImageGenerator:
    def __init__(
        self,
        *,
        input: str | bytes = b"",
        step_limit: int = 1_000_000,
        debug: bool = False,
    ):
        self.commands = SelfExpandingList(default=SelfExpandingList[PietCommand](default=PietCommand._NONE))
        self.colors = SelfExpandingList(default=SelfExpandingList(default=BLACK))
        self.interpreter = PietInterpreter(self.image, input=input, step_limit=step_limit, debug=debug)
        self.interpreter.runtime.output = open(sys.stdout.fileno(), "wb", closefd=False)
        self._current_hue = 0
        self._current_lightness = 0
        self._previous_color = WHITE

    def set_command(self, command: PietCommand, position: OrderedPair):
        y, x = position
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

    def set_offset_command(self, command: PietCommand, offset: DirectionOffset):
        pointer = DirectionPointer()
        pointer.direction = self.interpreter.runtime.pointer.direction
        pointer.position = self.interpreter.runtime.pointer.position
        pointer.rotate(offset.value)
        pointer.move_to_next()
        if offset.value > 3:
            pointer.rotate()
            pointer.move_to_next()
        self.set_command(command, pointer.position)

    def set_next_command(self, command: PietCommand, multiplier: int = 1, offset: OrderedPair | None = None):
        # pylint: disable=protected-access
        if multiplier < 1:
            return
        # Update the reader with our current image.
        self.interpreter.reader.colors = self.colors  # type: ignore
        # Simulate steps to move the pointer.
        next_pos = self.interpreter.pointer.next_position()
        next_command = self.commands[next_pos.y][next_pos.x]
        while next_command is not PietCommand._NONE:
            self.interpreter.step()
            next_pos = self.interpreter.pointer.next_position()
            try:
                next_command = self.commands[next_pos.y][next_pos.x]
            except IndexError:
                next_command = PietCommand._NONE
        # Next command is now NONE (0)
        if offset is not None:
            next_pos += offset
        self.set_command(command, next_pos)
        y, x = next_pos

        if multiplier > 1:
            if self.interpreter.runtime.pointer.direction is PointerDirection.RIGHT:
                self.commands[y][x + 1 : x + multiplier] = PietCommand._PREVIOUS
                self.colors[y][x + 1 : x + multiplier] = self._previous_color
            elif self.interpreter.runtime.pointer.direction is PointerDirection.LEFT:
                self.commands[y][x - multiplier + 1 : x] = PietCommand._PREVIOUS
                self.colors[y][x - multiplier + 1 : x] = self._previous_color
            elif self.interpreter.runtime.pointer.direction is PointerDirection.DOWN:
                for y in range(y + 1, y + multiplier):
                    self.commands[y][x] = PietCommand._PREVIOUS
                    self.colors[y][x] = self._previous_color
            elif self.interpreter.runtime.pointer.direction is PointerDirection.UP:
                for y in range(y - multiplier + 1, y):
                    self.commands[y][x] = PietCommand._PREVIOUS
                    self.colors[y][x] = self._previous_color
            else:
                raise ValueError("Invalid direction pointer position.")

    @property
    def image(self) -> Image.Image:
        colors = self.colors
        if not colors:
            return Image.new("RGB", (1, 1), WHITE)
        height = len(colors)
        width = len(max(colors, key=len))
        color_ints = []
        for y in range(height):
            for x in range(width):
                color_ints.append(int(colors[y][x]))
        image = Image.new("RGB", (width, height))
        image.putdata(color_ints)
        return image

    def generate_image(self, data: bytes, cols: int = 4, key: bytes = b"") -> Image.Image:
        """Construct a Piet program that outputs the data given."""
        length = len(data)
        self.set_next_command(PietCommand.NOOP, 6)
        for i, byte in enumerate(data):
            if key:
                self.interpreter.runtime.input = BytesIO(key)
                # shift = key[i % len(key)]
                shift = key[i]
                shifted_byte = (byte + shift) % 256
                self.set_next_command(PietCommand.NOOP, 256 - shifted_byte)
                # self._current_lightness = random.randint(0, 2)
                # self._current_hue = random.randint(0, 5)
                self.set_next_command(PietCommand.OUT_CHAR, shifted_byte)
                # self.set_next_command(
                #     random.choice([x for x in PietCommand if isinstance(x.value, ColorChange)]),
                #     byte,
                # )
                self.set_next_command(PietCommand.PUSH)
                self.set_next_command(PietCommand.IN_CHAR)
                self.set_next_command(PietCommand.SUBTRACT, 16)
                self.set_next_command(PietCommand.PUSH)
                self.set_next_command(PietCommand.DUPLICATE)
                self.set_next_command(PietCommand.MULTIPLY)
                self.set_next_command(PietCommand.MOD)
            else:
                self.set_next_command(PietCommand.NOOP, 256 - byte)
                self.set_next_command(PietCommand.OUT_CHAR, byte)
                self.set_next_command(PietCommand.PUSH)

            if (i + 1) % cols == 0:
                self.set_next_command(PietCommand.OUT_CHAR, 3 if (i + 1) % (cols * 2) == 0 else 1)
                self.set_next_command(PietCommand.PUSH)
                self.set_next_command(PietCommand.DUPLICATE)
                self.set_next_command(PietCommand.POINTER)
                self.set_next_command(PietCommand.POINTER)
                self.set_next_command(PietCommand.NOOP, 6 if (i + 1) % (cols * 2) == 0 else 4)
            else:
                self.set_next_command(PietCommand.OUT_CHAR)
            if i == length - 1:
                # Add a terminating block of pixels to the end.
                self.set_next_command(PietCommand.NOOP)
                if self.interpreter.runtime.pointer.direction is PointerDirection.LEFT:
                    # The ADD command here is arbitrary, since a transition from white to a color is a no-op.
                    self.set_next_command(PietCommand.ADD, 3)
                    self.set_next_command(PietCommand.PUSH)
                    self.set_next_command(PietCommand.DUPLICATE)
                    self.set_next_command(PietCommand.POINTER)
                    self.set_next_command(PietCommand.POINTER)
                self.set_next_command(PietCommand.NOOP, 4)
                self.set_next_command(PietCommand.BLOCK)
                self.set_next_command(PietCommand.NOOP, 2)
                self.set_next_command(PietCommand.BLOCK)
                self.set_offset_command(PietCommand.BLOCK, DirectionOffset.LEFT)
                self.set_offset_command(PietCommand.BLOCK, DirectionOffset.BACK_LEFT)
                self.set_next_command(PietCommand.NOOP)
                self.set_next_command(PietCommand.BLOCK)
                self.set_offset_command(PietCommand.BLOCK, DirectionOffset.LEFT)
                self.set_offset_command(PietCommand.BLOCK, DirectionOffset.RIGHT)
        return self.image
