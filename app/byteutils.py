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
