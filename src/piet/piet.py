import collections
import functools
import math
import string
import sys
import time
from collections import deque
from copy import deepcopy
from enum import Enum, IntEnum
from typing import Callable, Iterable, NamedTuple, TypeVar, overload
from warnings import warn

from PIL import Image

T = TypeVar("T")


class SelfExpandingList(list[T]):
    def __init__(self, iterable: Iterable[T] = (), /, *, default: T = None):
        self._default = deepcopy(default)
        super().__init__(iterable)

    @overload
    def __getitem__(self, index: int, /) -> T:
        ...

    @overload
    def __getitem__(self, index: slice, /) -> "SelfExpandingList[T]":
        ...

    def __getitem__(self, index: int | slice, /) -> T | "SelfExpandingList[T]":
        try:
            if isinstance(index, slice):
                items = []
                for i in range(index.start or 0, index.stop or len(self), index.step or 1):
                    try:
                        items.append(super().__getitem__(i))
                    except IndexError:
                        items.append(deepcopy(self._default))
                return self.__class__(items, default=deepcopy(self._default))
            if index < -1:
                raise IndexError("SelfExpandingList index out of range")
            return super().__getitem__(index)
        except IndexError:
            if isinstance(index, slice):
                i: int = index.stop
            else:
                i = index
            self.extend([deepcopy(self._default) for _ in range((i - len(self) + 1))])
            return self.__getitem__(index)

    @overload
    def __setitem__(self, index: int, value: T, /):
        ...

    @overload
    def __setitem__(self, index: slice, value: T | Iterable[T], /):
        ...

    def __setitem__(self, index, value, /):
        try:
            if isinstance(index, slice):
                indices = range(index.start or 0, index.stop or len(self), index.step or 1)
                for i in indices:
                    self.__setitem__(i, value)
            else:
                if index < -1:
                    raise IndexError("SelfExpandingList index out of range")
                super().__setitem__(index, value)
        except IndexError:
            if isinstance(index, slice):
                i: int = index.stop
            else:
                i = index
            self.extend([deepcopy(self._default) for _ in range((i - len(self) + 1))])
            self.__setitem__(index, value)


class OrderedPair(NamedTuple):
    y: int
    x: int

    def __add__(self, other: "OrderedPair | tuple[int, int]", /) -> "OrderedPair":
        return OrderedPair(self.y + other[0], self.x + other[1])

    def __sub__(self, other: "OrderedPair | tuple[int, int]", /) -> "OrderedPair":
        return OrderedPair(self.y - other[0], self.x - other[1])

    def __mul__(self, other: "OrderedPair | tuple[int, int]", /) -> "OrderedPair":
        return OrderedPair(self.y * other[0], self.x * other[1])

    def __floordiv__(self, other: "OrderedPair | tuple[int, int]", /) -> "OrderedPair":
        return OrderedPair(self.y // other[0], self.x // other[1])

    def __mod__(self, other: "OrderedPair | tuple[int, int]", /) -> "OrderedPair":
        return OrderedPair(self.y % other[0], self.x % other[1])

    def __pow__(self, other: "OrderedPair | tuple[int, int]", /) -> "OrderedPair":
        return OrderedPair(self.y ** other[0], self.x ** other[1])


class Color(NamedTuple):
    r: int
    g: int
    b: int

    def __eq__(self, other: "Color | tuple[int, int, int] | int", /) -> bool:
        if isinstance(other, (Color, tuple)):
            if len(other) != 3:
                return False
            return self.r == other[0] and self.g == other[1] and self.b == other[2]
        if isinstance(other, int):
            return int(self) == other
        return False

    def __int__(self) -> int:
        return (self.r << 0) + (self.g << 8) + (self.b << 16)


class ColorChange(NamedTuple):
    lightness: int
    hue: int


class PointerDirection(Enum):
    RIGHT = OrderedPair(0, 1)
    DOWN = OrderedPair(1, 0)
    LEFT = OrderedPair(0, -1)
    UP = OrderedPair(-1, 0)


class DirectionOffset(IntEnum):
    FRONT = 0
    RIGHT = 1
    BACK = 2
    LEFT = 3
    FRONT_RIGHT = 4
    BACK_RIGHT = 5
    BACK_LEFT = 6
    FRONT_LEFT = 7


class CodelChooserDirection(IntEnum):
    LEFT = -1
    RIGHT = 1


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

        queue = collections.deque()
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


class DirectionPointer:
    def __init__(self):
        self.direction = PointerDirection.RIGHT
        self.position = OrderedPair(0, 0)

    def rotate(self, times: int = 1):
        directions = tuple(PointerDirection)
        self.direction = directions[(directions.index(self.direction) + times) % 4]

    def next_position(self) -> OrderedPair:
        return self.position + self.direction.value

    def move_to_next(self):
        """Move one pixel in the direction of the DP"""
        self.position = self.next_position()


class CodelChooser:
    def __init__(self):
        self.direction = CodelChooserDirection.LEFT

    def flip(self, times: int = 1):
        self.direction = CodelChooserDirection(self.direction * -1 if abs(times) % 2 else self.direction)


class PietStack:
    def __init__(self):
        self._stack = deque()

    @property
    def top(self) -> int:
        return self._stack[-1]

    def pop(self) -> int:
        """Pop the top item off of the stack"""
        return self._stack.pop()

    def pop_multiple(self, count: int = 2, /) -> list[int]:
        """Pop the top `count` items off the stack (default: 2)"""
        return [self.pop() for _ in range(count)]

    def push(self, item: int, /):
        """Push an item (int) on to the top of the stack"""
        self._stack.append(item)

    def extend(self, items: Iterable[int], /):
        """Push multiple items on to the stack"""
        self._stack.extend(items)


def pass_on_empty_stack(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except IndexError:
            warn("Attempted to pop from empty stack.", RuntimeWarning)
            return None

    return wrapper


class PietRuntime:
    def __init__(self, output_buffer=sys.stdout, input_buffer: str = "", stack: PietStack | None = None):
        self.output = output_buffer
        self.stack = stack or PietStack()
        self.pointer = DirectionPointer()
        self.codel_chooser = CodelChooser()
        self.input_buffer = input_buffer
        self.delta_map: dict[tuple[int, int], Callable] = {
            (0, 0): self.p_noop,
            (0, 1): self.p_add,
            (0, 2): self.p_divide,
            (0, 3): self.p_greater,
            (0, 4): self.p_duplicate,
            (0, 5): self.p_input_char,
            (1, 0): self.p_push,
            (1, 1): self.p_subtract,
            (1, 2): self.p_modulo,
            (1, 3): self.p_pointer,
            (1, 4): self.p_roll,
            (1, 5): self.p_output_num,
            (2, 0): self.p_pop,
            (2, 1): self.p_multiply,
            (2, 2): self.p_not,
            (2, 3): self.p_switch,
            (2, 4): self.p_input_num,
            (2, 5): self.p_output_char,
        }

    def p_blocked(self):
        pass

    def p_noop(self):
        pass

    def p_push(self, value: int, /):
        self.stack.push(value)

    @pass_on_empty_stack
    def p_pop(self):
        self.stack.pop()

    @pass_on_empty_stack
    def p_add(self):
        self.stack.push(sum(self.stack.pop_multiple()))

    @pass_on_empty_stack
    def p_subtract(self):
        first, second = self.stack.pop_multiple()
        self.stack.push(second - first)

    @pass_on_empty_stack
    def p_multiply(self):
        first, second = self.stack.pop_multiple()
        self.stack.push(second * first)

    @pass_on_empty_stack
    def p_divide(self):
        first, second = self.stack.pop_multiple()
        self.stack.push(second // first)

    @pass_on_empty_stack
    def p_modulo(self):
        first, second = self.stack.pop_multiple()
        self.stack.push(second % first)

    @pass_on_empty_stack
    def p_not(self):
        self.stack.push(int(not self.stack.pop()))

    @pass_on_empty_stack
    def p_greater(self):
        first, second = self.stack.pop_multiple()
        self.stack.push(int(second > first))

    @pass_on_empty_stack
    def p_pointer(self):
        self.pointer.rotate(self.stack.pop())

    @pass_on_empty_stack
    def p_switch(self):
        self.codel_chooser.flip(self.stack.pop())

    @pass_on_empty_stack
    def p_duplicate(self):
        self.stack.push(self.stack.top)

    @pass_on_empty_stack
    def p_roll(self):
        first, second = self.stack.pop_multiple()
        values = deque(self.stack.pop_multiple(second))
        values.rotate(first)
        self.stack.extend(values)

    def p_input_num(self):
        buffer = ""
        for char in self.input_buffer:
            if char in string.whitespace and buffer:
                break
            self.input_buffer = self.input_buffer[1:]
            buffer += char
            if char in string.whitespace and not buffer:
                break
        try:
            self.stack.push(int(buffer))
        except ValueError:
            self.input_buffer = buffer + self.input_buffer
            warn(f"Conversion of '{buffer}' to integer failed. Check input.", RuntimeWarning)

    def p_input_char(self):
        char = self.input_buffer[0]
        self.input_buffer = self.input_buffer[1:]
        self.stack.push(ord(char))

    @pass_on_empty_stack
    def p_output_num(self):
        self.output.write(str(self.stack.pop()))

    @pass_on_empty_stack
    def p_output_char(self):
        self.output.write(chr(self.stack.pop()))


class StepTrace(NamedTuple):
    iteration: int
    position: OrderedPair
    instruction: Callable
    did_flip: bool
    last_codel: Codel
    current_codel: Codel

    def __repr__(self) -> str:
        return (
            f"StepTrace({self.iteration:0>4},"
            f" instruction={self.instruction.__name__},"
            f" position={self.position},"
            f" did_flip={self.did_flip},"
            f" last_codel={self.last_codel},"
            f" current_codel={self.current_codel})"
        )


class EndOfProgram(BaseException):
    pass


class StepLimitReached(EndOfProgram):
    pass


class PietInterpreter:
    def __init__(
        self,
        image: Image.Image,
        *,
        step_limit: int = 1_000_000,
        debug: bool = False,
        runtime: PietRuntime | None = None,
    ):
        self.step_limit = step_limit
        self.debug = debug
        self.reader = ImageReader(image)
        self.runtime = runtime or PietRuntime()
        self.iteration = 0
        self.steps: list[StepTrace] = []
        self._last_codel = self.reader.codel_info(self.position)
        self._current_codel = self.reader.codel_info(self.position)
        self._flips = 0
        self._move_to_furthest_pixel()

    @property
    def stack(self) -> PietStack:
        return self.runtime.stack

    @property
    def pointer(self) -> DirectionPointer:
        return self.runtime.pointer

    @property
    def position(self) -> OrderedPair:
        return self.runtime.pointer.position

    @property
    def last_step(self) -> StepTrace | None:
        try:
            return self.steps[-1]
        except IndexError:
            return None

    @staticmethod
    def _find_color_position(color: Color) -> OrderedPair:
        row = next(
            i for i, v in enumerate((color in PIET_COLORS[0], color in PIET_COLORS[1], color in PIET_COLORS[2])) if v
        )
        column = next(
            i
            for i, v in enumerate(
                (
                    color == PIET_COLORS[row][0],
                    color == PIET_COLORS[row][1],
                    color == PIET_COLORS[row][2],
                    color == PIET_COLORS[row][3],
                    color == PIET_COLORS[row][4],
                    color == PIET_COLORS[row][5],
                )
            )
            if v
        )
        return OrderedPair(row, column)

    def _determine_color_change(self) -> ColorChange:
        c1_pos = self._find_color_position(self._last_codel.color)
        c2_pos = self._find_color_position(self._current_codel.color)
        lightness, hue = c2_pos[0] - c1_pos[0], c2_pos[1] - c1_pos[1]

        if lightness < 0:
            lightness += 3
        if hue < 0:
            hue += 6

        return ColorChange(lightness, hue)

    def _get_polars(self, coords: Iterable[OrderedPair]) -> tuple[OrderedPair, OrderedPair]:
        largest_x = max(coords, key=lambda coord: coord.x).x
        largest_y = max(coords, key=lambda coord: coord.y).y
        smallest_x = min(coords, key=lambda coord: coord.x).x
        smallest_y = min(coords, key=lambda coord: coord.y).y
        return (
            OrderedPair(largest_y, largest_x),
            OrderedPair(smallest_y, smallest_x),
        )

    def _determine_farthest_pixel(self, codel: Codel) -> OrderedPair:
        largest, smallest = self._get_polars(codel.pixels)
        if self.runtime.pointer.direction is PointerDirection.RIGHT:
            largest_x_places = [pos for pos in codel.pixels if pos.x == largest.x]
            largest, smallest = self._get_polars(largest_x_places)
            if self.runtime.codel_chooser.direction is CodelChooserDirection.LEFT:
                return OrderedPair(smallest.y, largest.x)
            return largest
        if self.runtime.pointer.direction is PointerDirection.DOWN:
            largest_y_places = [pos for pos in codel.pixels if pos.y == largest.y]
            largest, smallest = self._get_polars(largest_y_places)
            if self.runtime.codel_chooser.direction is CodelChooserDirection.LEFT:
                return largest
            return OrderedPair(largest.y, smallest.x)
        if self.runtime.pointer.direction is PointerDirection.LEFT:
            smallest_x_places = [pos for pos in codel.pixels if pos.x == smallest.x]
            largest, smallest = self._get_polars(smallest_x_places)
            if self.runtime.codel_chooser.direction is CodelChooserDirection.LEFT:
                return OrderedPair(largest.y, smallest.x)
            return smallest
        if self.runtime.pointer.direction is PointerDirection.UP:
            smallest_y_places = [pos for pos in codel.pixels if pos.y == smallest.y]
            largest, smallest = self._get_polars(smallest_y_places)
            if self.runtime.codel_chooser.direction is CodelChooserDirection.LEFT:
                return smallest
            return OrderedPair(smallest.y, largest.x)
        return OrderedPair(-1, -1)

    def _move_to_furthest_pixel(self):
        # move to farthest pixel in current codel
        if self._current_codel.color != WHITE:
            farthest_pixel = self._determine_farthest_pixel(self._current_codel)
            self.runtime.pointer.position = farthest_pixel

    def step(self):
        "Execute a single step."
        if self.iteration >= self.step_limit:
            raise StepLimitReached("Step limit reached.")
        if self._flips >= 4:
            raise EndOfProgram("End of program reached.")

        args = []
        did_flip = False

        next_y, next_x = self.pointer.next_position()
        try:
            blocked = self.reader.colors[next_y][next_x] == BLACK or next_y < 0 or next_x < 0
        except IndexError:
            blocked = True

        if not blocked:
            # move one pixel over to next codel
            self._last_codel = self._current_codel
            self.pointer.move_to_next()
            if self.reader.colors[self.position.y][self.position.x] == WHITE:
                # Skip the codel_info call if the current codel is white for performance reasons.
                self._current_codel = Codel(WHITE, {self.position})
                # Skip to the last white pixel in the direction of the DP.
                next_pos = self.pointer.next_position()
                while self.reader.colors[next_pos.y][next_pos.x] == WHITE:
                    self._current_codel.pixels.add(next_pos)
                    self.pointer.move_to_next()
                    next_pos = self.pointer.next_position()
            else:
                self._current_codel = self.reader.codel_info(self.position)
                self._move_to_furthest_pixel()

            # determine color delta between current and previous codel
            # and execute relevant instruction
            if WHITE in (self._last_codel.color, self._current_codel.color):
                instruction = self.runtime.p_noop
                if self._last_codel.color != self._current_codel.color:
                    self._flips = 0
            else:
                delta = self._determine_color_change()
                instruction = self.runtime.delta_map[delta]
                if delta == (1, 0):
                    args.append(len(self._last_codel))
                self._flips = 0
        else:
            if self.last_step and not self.last_step.did_flip:
                self.runtime.codel_chooser.flip()
                self._move_to_furthest_pixel()
                instruction = self.runtime.p_blocked
                did_flip = True
                self._flips += 1
            else:
                self.runtime.pointer.rotate()
                self._move_to_furthest_pixel()
                instruction = self.runtime.p_blocked
        instruction(*args)
        step = StepTrace(
            self.iteration,
            self.position,
            instruction,
            did_flip,
            self._last_codel,
            self._current_codel,
        )
        self.steps.append(step)
        self.iteration += 1
        if self.debug:
            print(step, file=sys.stderr)

    def run(self, speed: int = -1) -> EndOfProgram:
        """Start execution at pos(0,0). Run at `speed` steps/sec (-1 is unlimited (default))."""

        last_second = math.floor(time.time())
        steps_this_second = 0
        while True:
            this_second = math.floor(time.time())
            if this_second > last_second:
                last_second = this_second
                steps_this_second = 0
            if speed != -1 and steps_this_second == speed:
                continue

            try:
                self.step()
            except EndOfProgram as exc:
                return exc
            steps_this_second += 1


class PietProgramGenerator:
    def __init__(self):
        self.commands = SelfExpandingList(default=SelfExpandingList[PietCommand](default=PietCommand._NONE))
        self.colors = SelfExpandingList(default=SelfExpandingList(default=BLACK))
        self.interpreter = PietInterpreter(self.image, debug=False)
        self._current_hue = 0
        self._current_lightness = 0
        self._previous_color = WHITE

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


def generate_image(data: bytes, cols: int = 4) -> Image.Image:
    """Construct a Piet program that outputs the data given."""
    length = len(data)
    generator = PietProgramGenerator()
    generator.set_next_command(PietCommand.NOOP, 6)
    for i, byte in enumerate(data):
        generator.set_next_command(PietCommand.NOOP, 256 - byte)
        # program._current_lightness = random.randint(0, 2)
        # program._current_hue = random.randint(0, 5)
        generator.set_next_command(PietCommand.OUT_CHAR, byte)
        # program.set_next_command(random.choice([x for x in PietCommand if isinstance(x.value, ColorChange)]), byte)
        generator.set_next_command(PietCommand.PUSH)
        if (i + 1) % cols == 0:
            generator.set_next_command(PietCommand.OUT_CHAR, 3 if (i + 1) % (cols * 2) == 0 else 1)
            generator.set_next_command(PietCommand.PUSH)
            generator.set_next_command(PietCommand.DUPLICATE)
            generator.set_next_command(PietCommand.POINTER)
            generator.set_next_command(PietCommand.POINTER)
            generator.set_next_command(PietCommand.NOOP, 6 if (i + 1) % (cols * 2) == 0 else 4)
        else:
            generator.set_next_command(PietCommand.OUT_CHAR)
        if i == length - 1:
            # Add a terminating block of pixels to the end.
            generator.set_next_command(PietCommand.NOOP)
            if generator.interpreter.runtime.pointer.direction is PointerDirection.LEFT:
                # The ADD command here is arbitrary, since a transition from white to a color is a no-op.
                generator.set_next_command(PietCommand.ADD, 3)
                generator.set_next_command(PietCommand.PUSH)
                generator.set_next_command(PietCommand.DUPLICATE)
                generator.set_next_command(PietCommand.POINTER)
                generator.set_next_command(PietCommand.POINTER)
            generator.set_next_command(PietCommand.NOOP, 4)
            generator.set_next_command(PietCommand.BLOCK)
            generator.set_next_command(PietCommand.NOOP, 2)
            generator.set_next_command(PietCommand.BLOCK)
            generator.set_offset_command(PietCommand.BLOCK, DirectionOffset.LEFT)
            generator.set_offset_command(PietCommand.BLOCK, DirectionOffset.BACK_LEFT)
            generator.set_next_command(PietCommand.NOOP)
            generator.set_next_command(PietCommand.BLOCK)
            generator.set_offset_command(PietCommand.BLOCK, DirectionOffset.LEFT)
            generator.set_offset_command(PietCommand.BLOCK, DirectionOffset.RIGHT)

    return generator.image
