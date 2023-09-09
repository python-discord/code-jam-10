import inspect
import math
import string
import sys
import time
from collections import deque
from enum import IntEnum
from typing import Callable, Iterable, NamedTuple, Optional
from warnings import warn

import numpy as np
from PIL import Image

from imagereader import CodelInfo, Reader

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Color(NamedTuple):
    r: int
    g: int
    b: int

    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, Color):
            return self.r == other.r and self.g == other.g and self.b == other.b
        if isinstance(other, tuple):
            if len(other) != 3:
                return False
            return self.r == other[0] and self.g == other[1] and self.b == other[2]
        if isinstance(other, int):
            return int(self) == other
        return False

    def __int__(self) -> int:
        return (self.r << 0) + (self.g << 8) + (self.b << 16)


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


class PointerDirection(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


class CodelChooserDirection(IntEnum):
    LEFT = -1
    RIGHT = 1


class DirectionPointer:
    def __init__(self):
        self.direction = PointerDirection.RIGHT

    def rotate(self, times: int = 1):
        self.direction = PointerDirection((self.direction + times) % 4)


class CodelChooser:
    def __init__(self):
        self.direction = CodelChooserDirection.LEFT

    def flip(self, times: int = 1):
        self.direction = CodelChooserDirection(self.direction * -1 if abs(times) % 2 else self.direction)


class PietStack:
    def __init__(self):
        self._stack = deque()

    def __getitem__(self, val) -> int:
        return self._stack[val]

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


class PietRuntime:
    def __init__(self, output_buffer=sys.stdout, input_buffer: str = "", stack: Optional[PietStack] = None):
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

    def p_pop(self):
        self.stack.pop()

    def p_add(self):
        self.stack.push(sum(self.stack.pop_multiple()))

    def p_subtract(self):
        first, second = self.stack.pop_multiple()
        self.stack.push(second - first)

    def p_multiply(self):
        first, second = self.stack.pop_multiple()
        self.stack.push(second * first)

    def p_divide(self):
        first, second = self.stack.pop_multiple()
        self.stack.push(second // first)

    def p_modulo(self):
        first, second = self.stack.pop_multiple()
        self.stack.push(second % first)

    def p_not(self):
        self.stack.push(int(not self.stack.pop()))

    def p_greater(self):
        first, second = self.stack.pop_multiple()
        self.stack.push(int(second > first))

    def p_pointer(self):
        self.pointer.rotate(int(self.stack.pop()))

    def p_switch(self):
        self.codel_chooser.flip(int(self.stack.pop()))

    def p_duplicate(self):
        self.stack.push(self.stack.top)

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

    def p_output_num(self):
        self.output.write(str(self.stack.pop()))

    def p_output_char(self):
        self.output.write(chr(self.stack.pop()))


class PietInterpreter:
    class _StepReport:
        def __init__(self, ie: bool, lc: CodelInfo, cc: CodelInfo) -> None:
            self.instruction_executed: bool = ie
            self.last_codel: CodelInfo = lc
            self.current_codel: CodelInfo = cc

    def __init__(
        self,
        image: Image.Image,
        *,
        step_limit: int = 1000000,
        debug: bool = False,
        runtime: Optional[PietRuntime] = None,
    ):
        self.step_limit = step_limit
        self.debug = debug
        self.reader = Reader(image)
        self.runtime = runtime or PietRuntime()
        self.stack = self.runtime.stack
        self.instructions = dict()
        self.current_position = (0, 0)
        self.event_queue = list()
        self.last_codel: CodelInfo
        self.current_codel: CodelInfo
        self.last_instruction = None
        self.last_step = None

        for name, obj in inspect.getmembers(self.runtime):
            if name.startswith("p_"):
                self.instructions.update({name: obj})

    @staticmethod
    def _find_color_position(c: tuple):
        row = next(i for i, x in enumerate((c in PIET_COLORS[0], c in PIET_COLORS[1], c in PIET_COLORS[2])) if x)
        column = next(
            i
            for i, x in enumerate(
                (
                    c == PIET_COLORS[row][0],
                    c == PIET_COLORS[row][1],
                    c == PIET_COLORS[row][2],
                    c == PIET_COLORS[row][3],
                    c == PIET_COLORS[row][4],
                    c == PIET_COLORS[row][5],
                )
            )
            if x
        )
        return (row, column)

    def _determine_color_delta(self) -> tuple[int, ...]:
        c1_pos = self._find_color_position(self.last_codel.color)
        c2_pos = self._find_color_position(self.current_codel.color)
        c_delta = [c2_pos[0] - c1_pos[0], c2_pos[1] - c1_pos[1]]

        if c_delta[0] < 0:
            c_delta[0] = c_delta[0] + 3
        if c_delta[1] < 0:
            c_delta[1] = c_delta[1] + 6

        return tuple(c_delta)

    def _get_polars(self, coords):
        largest_x = max(coords, key=lambda x: x[1])[1]
        largest_y = max(coords, key=lambda x: x[0])[0]
        smallest_x = min(coords, key=lambda x: x[1])[1]
        smallest_y = min(coords, key=lambda x: x[0])[0]
        # largest_x = 0
        # largest_y = 0
        # smallest_y, smallest_x, *_ = self.reader.im_array.shape
        # for y, x in coords:
        #     if x > largest_x:
        #         largest_x = x
        #     if x < smallest_x:
        #         smallest_x = x
        #     if y > largest_y:
        #         largest_y = y
        #     if y < smallest_y:
        #         smallest_y = y
        return (
            largest_x,
            largest_y,
            smallest_x,
            smallest_y,
        )

    def _determine_farthest_pixel(self, codel: CodelInfo) -> tuple[int, int]:
        lx, ly, sx, sy = self._get_polars(codel.pixels)
        if self.runtime.pointer.direction is PointerDirection.RIGHT:
            largest_x_places = [(y, x) for y, x in codel.pixels if x == lx]
            lx, ly, sx, sy = self._get_polars(largest_x_places)
            if self.runtime.codel_chooser.direction is CodelChooserDirection.LEFT:
                return sy, lx
            return ly, lx
        if self.runtime.pointer.direction is PointerDirection.DOWN:
            largest_y_places = [(y, x) for y, x in codel.pixels if y == ly]
            lx, ly, sx, sy = self._get_polars(largest_y_places)
            if self.runtime.codel_chooser.direction is CodelChooserDirection.LEFT:
                return ly, lx
            return ly, sx
        if self.runtime.pointer.direction is PointerDirection.LEFT:
            smallest_x_places = [(y, x) for y, x in codel.pixels if x == sx]
            lx, ly, sx, sy = self._get_polars(smallest_x_places)
            if self.runtime.codel_chooser.direction is CodelChooserDirection.LEFT:
                return ly, sx
            return sy, sx
        if self.runtime.pointer.direction is PointerDirection.UP:
            smallest_y_places = [(y, x) for y, x in codel.pixels if y == sy]
            lx, ly, sx, sy = self._get_polars(smallest_y_places)
            if self.runtime.codel_chooser.direction is CodelChooserDirection.LEFT:
                return sy, sx
            return sy, lx
        return (-1, -1)

    def _next_move(self) -> tuple[int, int]:
        if self.runtime.pointer.direction is PointerDirection.RIGHT:
            y, x = tuple(np.add(self.position, (0, 1)))
            return y, x
        if self.runtime.pointer.direction is PointerDirection.DOWN:
            y, x = tuple(np.add(self.position, (1, 0)))
            return y, x
        if self.runtime.pointer.direction is PointerDirection.LEFT:
            y, x = tuple(np.subtract(self.position, (0, 1)))
            return y, x
        if self.runtime.pointer.direction is PointerDirection.UP:
            y, x = tuple(np.subtract(self.position, (1, 0)))
            return y, x
        raise ValueError("Invalid direction pointer position.")

    def _move(self):
        """Move one pixel in the direction of the DP"""
        self.position = self._next_move()

    def _move_to_furthest_pixel(self):
        # move to farthest pixel in current codel
        if self.current_codel.color != WHITE:
            farthest_pixel = self._determine_farthest_pixel(self.current_codel)
            self.position = farthest_pixel

    def step(self):
        "Execute a single step."

        # move to farthest pixel in current codel
        farthest_pixel = self._determine_farthest_pixel(self.current_codel)
        self.current_position = farthest_pixel

        # move one pixel over to next codel
        self.last_codel = self.current_codel
        self._move()
        self.current_codel = self.reader.codel_info(self.current_position)

        # determine color delta between current and previous codel
        # and execute relevant instruction
        delta = self._determine_color_delta()
        instruction = self.runtime.DELTA_TABLE[delta]  # type: ignore
        args = []
        if delta == (1, 0):
            args.append(self.last_codel.size)
        instruction(*args)

        return

    def run(self, speed: int = -1):
        """Start execution at pos(0,0). Run at `speed` steps/sec (-1 is unlimited (default))."""
        # initialization
        self.current_codel = self.reader.codel_info((0, 0))
        self.current_position = (0, 0)

        last_second = math.floor(time.time())
        steps_this_second = 0
        while 1:
            this_second = math.floor(time.time())
            if this_second > last_second:
                last_second = this_second
                steps_this_second = 0
            if speed != -1 and steps_this_second == speed:
                continue

            self.step()
            steps_this_second += 1
        return
