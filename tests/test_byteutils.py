# flake8: noqa
import pytest

from app import byteutils


def test_byteutils_iter_bits():
    # arrange
    want_bits = [0, 1, 1, 0, 0, 0, 0, 1]  # "a" = 97

    # act
    gen = byteutils.iter_bits("a".encode())

    # assert
    for want_bit in want_bits:
        assert next(gen) == want_bit

    with pytest.raises(StopIteration):
        next(gen)
