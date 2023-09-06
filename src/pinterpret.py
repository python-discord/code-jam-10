from enum import IntEnum
from string import whitespace
from typing import Optional, SupportsInt
from warnings import warn

import numpy as np
from numpy.typing import ArrayLike


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
        self.stack = stack or PietStack()
        self.pointer = DirectionPointer()
        self.codel_chooser = CodelChooser()
        self.input_buffer = input_buffer

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
        return self.stack.pop()

    def p_output_char(self):
        return chr(self.stack.pop())  # type: ignore
