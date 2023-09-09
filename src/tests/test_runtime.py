import random
import string
from io import StringIO

import pytest

from src.piet.runtime import CodelChooserDirection, PietRuntime, PietStack, PointerDirection


@pytest.fixture(name="piet_runtime")
def fixture_piet_runtime():
    return PietRuntime(output_buffer=StringIO())


def test_push_instruction(piet_runtime: PietRuntime):
    piet_runtime.p_push(1)
    assert piet_runtime.stack[0] == 1


def test_pop_instruction(piet_runtime: PietRuntime):
    piet_runtime.p_push(1)
    piet_runtime.p_pop()
    assert len(piet_runtime.stack) == 0


def test_add_instruction(piet_runtime: PietRuntime):
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    piet_runtime.p_push(num1)
    piet_runtime.p_push(num2)
    piet_runtime.p_add()
    assert piet_runtime.stack[0] == num1 + num2
    piet_runtime.p_pop()


def test_subtract_instruction(piet_runtime: PietRuntime):
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    piet_runtime.p_push(num1)
    piet_runtime.p_push(num2)
    piet_runtime.p_subtract()
    assert piet_runtime.stack[0] == num1 - num2
    piet_runtime.p_pop()


def test_multiply_instruction(piet_runtime: PietRuntime):
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    piet_runtime.p_push(num1)
    piet_runtime.p_push(num2)
    piet_runtime.p_multiply()
    assert piet_runtime.stack[0] == num1 * num2
    piet_runtime.p_pop()


def test_division_instruction(piet_runtime: PietRuntime):
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    piet_runtime.p_push(num1)
    piet_runtime.p_push(num2)
    piet_runtime.p_divide()
    assert piet_runtime.stack[0] == num1 // num2
    piet_runtime.p_pop()


def test_modulo_instruction(piet_runtime: PietRuntime):
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    piet_runtime.p_push(num1)
    piet_runtime.p_push(num2)
    piet_runtime.p_modulo()
    assert piet_runtime.stack[0] == num1 % num2
    piet_runtime.p_pop()


def test_not_instruction(piet_runtime: PietRuntime):
    choice = random.choice([1, 0])
    piet_runtime.p_push(choice)
    piet_runtime.p_not()
    assert piet_runtime.stack[0] == (not choice)
    piet_runtime.p_pop()


def test_greater_instruction(piet_runtime: PietRuntime):
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    piet_runtime.p_push(num1)
    piet_runtime.p_push(num2)
    piet_runtime.p_greater()
    assert piet_runtime.stack[0] == (num1 > num2)
    piet_runtime.p_pop()


def test_pointer_instruction(piet_runtime: PietRuntime):
    piet_runtime.p_push(2)
    piet_runtime.p_pointer()
    assert piet_runtime.pointer.direction == PointerDirection.LEFT


def test_switch_instruction(piet_runtime: PietRuntime):
    piet_runtime.p_push(1)
    piet_runtime.p_switch()
    assert piet_runtime.codel_chooser.direction == CodelChooserDirection.RIGHT


def test_duplicate_instruction(piet_runtime: PietRuntime):
    num = random.choice(range(1, 100))
    piet_runtime.p_push(num)
    piet_runtime.p_duplicate()
    assert piet_runtime.stack.pop_multiple() == [num, num]


def test_roll_instruction(piet_runtime: PietRuntime):
    base_stack = PietStack(random.randbytes(random.choice(range(1, 10))))
    edge_stack = PietStack(random.randbytes(random.choice(range(1, 10))))
    roll_count = random.choice(range(1, 10))
    piet_runtime.stack.extend(base_stack)
    piet_runtime.stack.extend(edge_stack)
    piet_runtime.stack.extend((len(edge_stack), roll_count))
    edge_stack.rotate(roll_count)
    piet_runtime.p_roll()
    base_stack.extend(edge_stack)
    assert piet_runtime.stack == base_stack


def test_input_num_instruction(piet_runtime: PietRuntime):
    piet_runtime.input = StringIO("69 test")
    piet_runtime.p_input_num()
    result = piet_runtime.input.read()
    assert piet_runtime.stack.top == 69
    assert result == " test"


def test_input_char_instruction(piet_runtime: PietRuntime):
    piet_runtime.input = StringIO("test")
    piet_runtime.p_input_char()
    piet_runtime.p_input_char()
    piet_runtime.p_input_char()
    piet_runtime.p_input_char()
    assert piet_runtime.stack == PietStack((116, 101, 115, 116))


def test_output_num_instruction(piet_runtime: PietRuntime):
    num = random.choice(range(1, 100))
    piet_runtime.p_push(num)
    piet_runtime.p_output_num()
    piet_runtime.output.seek(0)
    assert piet_runtime.output.read() == str(num)


def test_output_char_instruction(piet_runtime: PietRuntime):
    char = random.choice(string.ascii_letters)
    piet_runtime.p_push(ord(char))
    piet_runtime.p_output_char()
    piet_runtime.output.seek(0)
    assert piet_runtime.output.read() == char
