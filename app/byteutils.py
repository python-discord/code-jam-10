from typing import Generator


def iter_bits(bytes_: bytes) -> Generator[int, None, None]:
    """Enumerate over each bit in the given bytes.

    Args:
        bytes_ (bytes): bytes to enumerate over

    Yields:
        Generator[int, None, None]: Return each bit as an int (0/1)
    """
    for byte in bytes_:
        bitstring = f"{byte:0>8b}"
        for bit in bitstring:
            yield int(bit)


def set_bit(value: int, bit: int) -> int:
    """Set the bit as position on the value.

    Args:
        value (int): Value to set bit on
        bit (int): Bit position to set

    Returns:
        int: value with the bit at position `bit` set
    """
    return value | (1 << bit)


def clear_bit(value: int, bit: int) -> int:
    """Clear the bit at position on the value.

    Args:
        value (int): Value to clear bit on
        bit (int): Bit position to clear

    Returns:
        int: value with the bit at position `bit` cleared
    """
    return value & ~(1 << bit)
