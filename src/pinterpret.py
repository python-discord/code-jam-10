import inspect
import math
import sys
import time
from enum import IntEnum
from os import PathLike
from string import whitespace
from typing import Optional, SupportsInt, Tuple
from warnings import warn

import numpy as np
from numpy.typing import ArrayLike
from PIL import Image

from imagereader import CodelInfo, Reader
from piet import PIET_COLORS

"""
TODO:

-block exec on black/edge
-noop on white
-perform DP/CC manipulation on block
-impl DEBUG features
    - last_step
    - last_instruction
- stop exec when all paths exhausted
"""


class DirectionPointerValues(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


class CodelChooserValues(IntEnum):
    LEFT = 0
    RIGHT = 1


class DirectionPointer:
    def __init__(self) -> None:
        self.position = DirectionPointerValues.RIGHT

    def rotate(self):
        if self.position == 3:
            self.position = DirectionPointerValues.RIGHT
        else:
            self.position = DirectionPointerValues(self.position + 1)

    def set(self, value):
        self.position = DirectionPointerValues(value)


class CodelChooser:
    def __init__(self) -> None:
        self.position = CodelChooserValues.LEFT

    def flip(self):
        self.position = CodelChooserValues(int(not self.position))

    def set(self, value):
        self.position = CodelChooserValues(value)


class PietStack:
    def __init__(self) -> None:
        self._stack = np.array([], dtype=np.int64)

    def __getitem__(self, val):
        return self._stack[val]

    @property
    def top(self) -> int:
        return self._stack[-1]

    def pop(self) -> np.int64:
        """Pop the top item off of the stack"""
        popped = self._stack[-1]
        self._stack = np.delete(self._stack, -1)
        return popped

    def popx(self, count: int = 2) -> np.ndarray:
        """Pop the top X items off the stack (default: 2)"""
        popped = self._stack[-count:]
        self._stack = np.delete(self._stack, tuple(range(-count, 0)))
        return popped

    def push(self, item: ArrayLike) -> None:
        """Push an item (int) on to the top of the stack"""
        if not isinstance(item, SupportsInt):
            raise ValueError(f"The pushed item must be an integer, not `{type(item)}`!")
        if isinstance(item, float):
            warn(
                "`PietStack.push()` expects an int, but float was recieved. Value will be rounded down.\n"
                "If this is undesirable, please check your inputs and try again.",
                RuntimeWarning,
            )
            item = int(np.floor(item))

        self._stack = np.append(self._stack, np.int64(item))


class PietRuntime:
    def __init__(self, input_buffer: str, stack: Optional[PietStack] = None) -> None:
        self.output = sys.stdout
        self.stack = stack or PietStack()
        self.pointer = DirectionPointer()
        self.codel_chooser = CodelChooser()
        self.input_buffer = input_buffer
        self.DELTA_TABLE = {
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

    def p_noop(self) -> None:
        pass

    def p_push(self, num_codel: int) -> None:
        self.stack.push(num_codel)

    def p_pop(self) -> None:
        _ = self.stack.pop()

    def p_add(self):
        self.stack.push(np.sum(self.stack.popx()))

    def p_subtract(self):
        self.stack.push(np.diff(np.flip(self.stack.popx())))

    def p_multiply(self):
        self.stack.push(np.prod(self.stack.popx()))

    def p_divide(self):
        self.stack.push(np.floor_divide(*self.stack.popx()))

    def p_modulo(self):
        self.stack.push(np.mod(*self.stack.popx()))

    def p_not(self):
        self.stack.push(np.int64(not bool(self.stack.pop())))

    def p_greater(self):
        self.stack.push(np.int64(np.greater(*self.stack.popx())))

    def p_pointer(self):
        self.pointer.set(np.mod(self.stack.pop(), 4))

    def p_switch(self):
        self.codel_chooser.set(np.mod(self.stack.pop(), 2))

    def p_duplicate(self):
        self.stack.push(self.stack.top)

    def p_roll(self):
        y, x = self.stack.popx()
        values = self.stack.popx(y)
        rolled = np.roll(values, x)
        for num in np.nditer(rolled):
            self.stack.push(int(num))  # type: ignore

    def p_input_num(self):
        buff = ""
        for char in self.input_buffer:
            if char in whitespace and buff:
                break
            self.input_buffer = self.input_buffer[1:]
            buff += char
            if char in whitespace and not buff:
                break

        try:
            self.stack.push(np.int64(buff))
        except ValueError:
            self.input_buffer = buff + self.input_buffer
            warn(f"Conversion of '{buff}' to integer failed. Check input.", RuntimeWarning)

    def p_input_char(self):
        char = self.input_buffer[0]
        self.input_buffer = self.input_buffer[1:]
        self.stack.push(np.int64(ord(char)))

    def p_output_num(self):
        self.output.write(str(self.stack.pop()))

    def p_output_char(self):
        self.output.write(chr(self.stack.pop()))  # type: ignore


class PietInterpreter:
    class _StepReport:
        def __init__(self, ie: bool, lc: CodelInfo, cc: CodelInfo) -> None:
            self.instruction_executed: bool = ie
            self.last_codel: CodelInfo = lc
            self.current_codel: CodelInfo = cc

    def __init__(
        self, image: PathLike, runtime: Optional[PietRuntime] = None, input_buffer: Optional[str] = None
    ) -> None:
        with open(image, "rb") as fp:
            self.reader = Reader(Image.open(fp))
        self.runtime = runtime or PietRuntime(input_buffer or "")
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

    def _determine_color_delta(self) -> Tuple[int, ...]:
        c1_pos = self._find_color_position(self.last_codel.color)
        c2_pos = self._find_color_position(self.current_codel.color)
        c_delta = [c2_pos[0] - c1_pos[0], c2_pos[1] - c1_pos[1]]

        if c_delta[0] < 0:
            c_delta[0] = c_delta[0] + 3
        if c_delta[1] < 0:
            c_delta[1] = c_delta[1] + 6

        return tuple(c_delta)

    def _get_polars(self, list):
        largest_x = 0
        largest_y = 0
        smallest_x = self.reader.im_rgb.size[0]
        smallest_y = self.reader.im_rgb.size[1]
        for y, x in list:
            if x > largest_x:
                largest_x = x
            if x < smallest_x:
                smallest_x = x
            if y > largest_y:
                largest_y = y
            if y < smallest_y:
                smallest_y = y
        return (
            largest_x,
            largest_y,
            smallest_x,
            smallest_y,
        )

    def _determine_farthest_pixel(self, codel: CodelInfo) -> Tuple[int, int]:
        # TODO: this can all obviously be optimized
        lx, ly, sx, sy = self._get_polars(codel.pixels)
        largest_x_places = []
        largest_y_places = []
        smallest_x_places = []
        smallest_y_places = []
        for y, x in codel.pixels:
            if x == lx:
                largest_x_places.append((y, x))
            if x == sx:
                smallest_x_places.append((y, x))
            if y == ly:
                largest_y_places.append((y, x))
            if y == sy:
                smallest_y_places.append((y, x))

        if self.runtime.pointer.position == DirectionPointerValues.RIGHT:
            lx, ly, sx, sy = self._get_polars(largest_x_places)
            if self.runtime.codel_chooser.position == CodelChooserValues.LEFT:
                return sy, lx
            else:
                return ly, lx
        elif self.runtime.pointer.position == DirectionPointerValues.DOWN:
            lx, ly, sx, sy = self._get_polars(largest_y_places)
            if self.runtime.codel_chooser.position == CodelChooserValues.LEFT:
                return ly, lx
            else:
                return ly, sx
        elif self.runtime.pointer.position == DirectionPointerValues.LEFT:
            lx, ly, sx, sy = self._get_polars(smallest_x_places)
            if self.runtime.codel_chooser.position == CodelChooserValues.LEFT:
                return ly, sx
            else:
                return sy, sx
        elif self.runtime.pointer.position == DirectionPointerValues.UP:
            lx, ly, sx, sy = self._get_polars(smallest_y_places)
            if self.runtime.codel_chooser.position == CodelChooserValues.LEFT:
                return sy, sx
            else:
                return sy, lx
        return (-1, -1)

    def _move(self):
        """Move one pixel in the direction of the DP"""
        if self.runtime.pointer.position == DirectionPointerValues.RIGHT:
            self.current_position = tuple(np.add(self.current_position, (0, 1)))
        elif self.runtime.pointer.position == DirectionPointerValues.DOWN:
            self.current_position = tuple(np.add(self.current_position, (1, 0)))
        elif self.runtime.pointer.position == DirectionPointerValues.LEFT:
            self.current_position = tuple(np.subtract(self.current_position, (0, 1)))
        elif self.runtime.pointer.position == DirectionPointerValues.UP:
            self.current_position = tuple(np.subtract(self.current_position, (1, 0)))

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
