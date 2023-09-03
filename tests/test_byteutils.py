# flake8: noqa
import pytest

from app import byteutils


def test_iter_bits():
    # arrange
    want_bits = [0, 1, 1, 0, 0, 0, 0, 1]  # "a" = 97

    # act
    gen = byteutils.iter_bits("a".encode())

    # assert
    for want_bit in want_bits:
        assert next(gen) == want_bit

    with pytest.raises(StopIteration):
        next(gen)


def test_set_bit():
    cases = [
        (4, 0, 5),
        (5, 0, 5),
        (2, 3, 10),
    ]
    for case in cases:
        got = byteutils.set_bit(case[0], case[1])
    assert got == case[2]


def test_clear_bit():
    cases = [(4, 0, 4), (5, 0, 4), (10, 3, 2)]
    for case in cases:
        got = byteutils.clear_bit(case[0], case[1])
        assert got == case[2]
