import random
import string
from io import BytesIO

import pytest
from piet.runtime import CodelChooserDirection, PietRuntime, PietStack, PointerDirection


@pytest.fixture(name="runtime")
def fixture_runtime():
    return PietRuntime()


def test_push_instruction(runtime: PietRuntime):
    runtime.p_push(1)
    assert runtime.stack[0] == 1


def test_pop_instruction(runtime: PietRuntime):
    runtime.p_push(1)
    runtime.p_pop()
    assert len(runtime.stack) == 0


def test_add_instruction(runtime: PietRuntime):
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    runtime.p_push(num1)
    runtime.p_push(num2)
    runtime.p_add()
    assert runtime.stack[0] == num1 + num2
    runtime.p_pop()


def test_subtract_instruction(runtime: PietRuntime):
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    runtime.p_push(num1)
    runtime.p_push(num2)
    runtime.p_subtract()
    assert runtime.stack[0] == num1 - num2
    runtime.p_pop()


def test_multiply_instruction(runtime: PietRuntime):
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    runtime.p_push(num1)
    runtime.p_push(num2)
    runtime.p_multiply()
    assert runtime.stack[0] == num1 * num2
    runtime.p_pop()


def test_division_instruction(runtime: PietRuntime):
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    runtime.p_push(num1)
    runtime.p_push(num2)
    runtime.p_divide()
    assert runtime.stack[0] == num1 // num2
    runtime.p_pop()


def test_modulo_instruction(runtime: PietRuntime):
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    runtime.p_push(num1)
    runtime.p_push(num2)
    runtime.p_modulo()
    assert runtime.stack[0] == num1 % num2
    runtime.p_pop()


def test_not_instruction(runtime: PietRuntime):
    choice = random.choice([1, 0])
    runtime.p_push(choice)
    runtime.p_not()
    assert runtime.stack[0] == (not choice)
    runtime.p_pop()


def test_greater_instruction(runtime: PietRuntime):
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    runtime.p_push(num1)
    runtime.p_push(num2)
    runtime.p_greater()
    assert runtime.stack[0] == (num1 > num2)
    runtime.p_pop()


def test_pointer_instruction(runtime: PietRuntime):
    runtime.p_push(2)
    runtime.p_pointer()
    assert runtime.pointer.direction == PointerDirection.LEFT


def test_switch_instruction(runtime: PietRuntime):
    runtime.p_push(1)
    runtime.p_switch()
    assert runtime.codel_chooser.direction == CodelChooserDirection.RIGHT


def test_duplicate_instruction(runtime: PietRuntime):
    num = random.choice(range(1, 100))
    runtime.p_push(num)
    runtime.p_duplicate()
    assert runtime.stack.pop_multiple() == [num, num]


def test_roll_instruction(runtime: PietRuntime):
    base_stack = PietStack(random.randbytes(random.choice(range(1, 10))))
    edge_stack = PietStack(random.randbytes(random.choice(range(1, 10))))
    roll_count = random.choice(range(1, 10))
    runtime.stack.extend(base_stack)
    runtime.stack.extend(edge_stack)
    runtime.stack.extend((len(edge_stack), roll_count))
    edge_stack.rotate(roll_count)
    runtime.p_roll()
    base_stack.extend(edge_stack)
    assert runtime.stack == base_stack


def test_input_num_instruction(runtime: PietRuntime):
    runtime.input = BytesIO(b"69 test")
    runtime.p_input_num()
    result = runtime.input.read()
    assert runtime.stack.top == 69
    assert result == b" test"


def test_input_char_instruction(runtime: PietRuntime):
    runtime.input = BytesIO(b"test")
    runtime.p_input_char()
    runtime.p_input_char()
    runtime.p_input_char()
    runtime.p_input_char()
    assert runtime.stack == PietStack((116, 101, 115, 116))


def test_output_num_instruction(runtime: PietRuntime):
    num = random.choice(range(1, 100))
    runtime.p_push(num)
    runtime.p_output_num()
    runtime.output.seek(0)
    assert runtime.output.read() == str(num).encode()


def test_output_char_instruction(runtime: PietRuntime):
    char = random.choice(string.ascii_letters).encode()
    runtime.p_push(ord(char))
    runtime.p_output_char()
    runtime.output.seek(0)
    assert runtime.output.read() == char
