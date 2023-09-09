import functools
import string
import sys
from collections import deque
from enum import Enum, IntEnum
from io import StringIO
from typing import Callable, TextIO
from warnings import warn

from .common import OrderedPair


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


class PietStack(deque[int]):
    @property
    def top(self) -> int:
        return self[-1]

    def pop_multiple(self, count: int = 2, /) -> list[int]:
        """Pop the top `count` items off the stack (default: 2)"""
        return [self.pop() for _ in range(count)]

    def push(self, item: int, /):
        """Push an item (int) on to the top of the stack"""
        self.append(item)


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
    def __init__(
        self,
        output_buffer: TextIO = sys.stdout,
        input_buffer: TextIO | None = None,
        stack: PietStack | None = None,
    ):
        self.output = output_buffer
        self.input = input_buffer or StringIO("")
        self.stack = stack or PietStack()
        self.pointer = DirectionPointer()
        self.codel_chooser = CodelChooser()
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
        values = deque(reversed(self.stack.pop_multiple(second)))
        values.rotate(first)
        self.stack.extend(values)

    def p_input_num(self):
        buffer = ""
        pos = self.input.tell()
        while True:
            char = self.input.read(1)
            if char in string.whitespace and buffer:
                self.input.seek(pos + len(buffer))
                break
            buffer += char
            if char in string.whitespace and not buffer:
                self.input.seek(pos + len(buffer))
                break
        try:
            self.stack.push(int(buffer))
        except ValueError:
            self.input.seek(pos)
            warn(f"Conversion of '{buffer}' to integer failed. Check input.", RuntimeWarning)

    def p_input_char(self):
        char = self.input.read(1)
        if char:
            self.stack.push(ord(char))

    @pass_on_empty_stack
    def p_output_num(self):
        self.output.write(str(self.stack.pop()))

    @pass_on_empty_stack
    def p_output_char(self):
        self.output.write(chr(self.stack.pop()))
