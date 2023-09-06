import random
import string

import numpy as np

from pinterpret import CodelChooserValues, DirectionPointerValues, PietRuntime

global piet_runtime


def test_runtime_create():
    global piet_runtime
    piet_runtime = PietRuntime("69 test")


def test_push_instruction():
    global piet_runtime
    piet_runtime.p_push(1)
    assert piet_runtime.stack[0] == 1


def test_pop_instruction():
    global piet_runtime
    piet_runtime.p_pop()
    assert piet_runtime.stack._stack.size == 0


def test_add_instruction():
    global piet_runtime
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    piet_runtime.p_push(num1)
    piet_runtime.p_push(num2)
    piet_runtime.p_add()
    assert piet_runtime.stack[0] == num1 + num2
    piet_runtime.p_pop()


def test_subtract_instruction():
    global piet_runtime
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    piet_runtime.p_push(num1)
    piet_runtime.p_push(num2)
    piet_runtime.p_subtract()
    assert piet_runtime.stack[0] == num1 - num2
    piet_runtime.p_pop()


def test_multiply_instruction():
    global piet_runtime
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    piet_runtime.p_push(num1)
    piet_runtime.p_push(num2)
    piet_runtime.p_multiply()
    assert piet_runtime.stack[0] == num1 * num2
    piet_runtime.p_pop()


def test_division_instruction():
    global piet_runtime
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    piet_runtime.p_push(num1)
    piet_runtime.p_push(num2)
    piet_runtime.p_divide()
    assert piet_runtime.stack[0] == num1 // num2
    piet_runtime.p_pop()


def test_modulo_instruction():
    global piet_runtime
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    piet_runtime.p_push(num1)
    piet_runtime.p_push(num2)
    piet_runtime.p_modulo()
    assert piet_runtime.stack[0] == num1 % num2
    piet_runtime.p_pop()


def test_not_instruction():
    global piet_runtime
    choice = random.choice([1, 0])
    piet_runtime.p_push(choice)
    piet_runtime.p_not()
    assert piet_runtime.stack[0] == (not choice)
    piet_runtime.p_pop()


def test_greater_instruction():
    global piet_runtime
    num1, num2 = random.choice(range(1, 100)), random.choice(range(1, 100))
    piet_runtime.p_push(num1)
    piet_runtime.p_push(num2)
    piet_runtime.p_greater()
    assert piet_runtime.stack[0] == (num1 > num2)
    piet_runtime.p_pop()


def test_pointer_instruction():
    global piet_runtime
    piet_runtime.p_push(2)
    piet_runtime.p_pointer()
    assert piet_runtime.pointer.position == DirectionPointerValues.LEFT


def test_switch_instruction():
    global piet_runtime
    piet_runtime.p_push(1)
    piet_runtime.p_switch()
    assert piet_runtime.codel_chooser.position == CodelChooserValues.RIGHT


def test_duplicate_instruction():
    global piet_runtime
    num = random.choice(range(1, 100))
    piet_runtime.p_push(num)
    piet_runtime.p_duplicate()
    assert np.array_equal(piet_runtime.stack._stack, np.array([num, num], dtype=np.int64))
    _ = piet_runtime.stack.popx()


def test_roll_instruction():
    global piet_runtime
    base_array = np.array(list(random.randbytes(random.choice(range(1, 10)))))
    edge_array = np.array(list(random.randbytes(random.choice(range(1, 10)))))
    roll_count = random.choice(range(1, 10))
    piet_runtime.stack._stack = np.copy(
        np.append(np.append(base_array, edge_array), np.array([edge_array.size, roll_count], dtype=np.int64))
    )
    rolled_array = np.roll(edge_array, roll_count)
    piet_runtime.p_roll()
    assert np.array_equal(piet_runtime.stack._stack, np.append(base_array, rolled_array))
    piet_runtime.stack._stack = np.array([], dtype=np.int64)


def test_input_num_instruction():
    global piet_runtime
    piet_runtime.p_input_num()
    assert (piet_runtime.input_buffer == " test") and (piet_runtime.stack[0] == 69)
    piet_runtime.p_pop()


def test_input_char_instruction():
    global piet_runtime
    piet_runtime.p_input_char()
    piet_runtime.p_input_char()
    piet_runtime.p_input_char()
    piet_runtime.p_input_char()
    piet_runtime.p_input_char()
    assert np.array_equal(piet_runtime.stack._stack, np.array([32, 116, 101, 115, 116], dtype=np.int64))
    piet_runtime.stack._stack = np.array([], dtype=np.int64)


def test_output_num_instruction():
    global piet_runtime
    num = random.choice(range(1, 100))
    piet_runtime.p_push(num)
    assert piet_runtime.p_output_num() == num


def test_output_char_instruction():
    global piet_runtime
    char = random.choice(string.ascii_letters)
    piet_runtime.p_push(ord(char))
    assert piet_runtime.p_output_char() == char
