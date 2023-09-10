import pytest

from src.piet import ImageGenerator, PietInterpreter
from src.piet.interpreter import StepLimitReached


@pytest.mark.parametrize(
    ("data", "cols"),
    [
        (b"AB", 1),
        (b"Hello, world! This a test string.", 4),
    ],
)
def test_generator(data: bytes, cols: int):
    generator = ImageGenerator()
    encoded = generator.generate_image(data, cols)
    encoded.save(f"{__file__}.png")
    interpreter = PietInterpreter(encoded, debug=True)
    exc = interpreter.run()
    if isinstance(exc, StepLimitReached):
        raise exc
    result = interpreter.output
    assert result == data, f"Output does not match input.\n{result}"


@pytest.mark.parametrize(
    ("data", "cols", "key"),
    [
        (b"AB", 1, b"passkey"),
        (b"Hello, world! This a test string.", 4, b"a longer passkey"),
    ],
)
def test_generator_with_key(data: bytes, cols: int, key: bytes):
    key *= len(data) // len(key) + 1
    generator = ImageGenerator()
    encoded = generator.generate_image(data, cols, key)
    encoded.save(f"{__file__}.png")
    interpreter = PietInterpreter(encoded, input=key, debug=True)
    exc = interpreter.run()
    if isinstance(exc, StepLimitReached):
        raise exc
    result = interpreter.output
    assert result == data, f"Output does not match input.\n{result}"
