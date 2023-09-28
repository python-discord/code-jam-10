import pytest
from piet import ImageGenerator, PietInterpreter
from piet.interpreter import StepLimitReached


@pytest.mark.parametrize(
    "data",
    [
        b"AB",
        b"Hello, world! This a test string.",
    ],
)
def test_generator(data: bytes):
    generator = ImageGenerator()
    encoded = generator.generate_image(data)
    encoded.save(f"{__file__}.png")
    interpreter = PietInterpreter(encoded, debug=True)
    exc = interpreter.run()
    if isinstance(exc, StepLimitReached):
        raise exc
    result = interpreter.output
    assert result == data, f"Output does not match input.\n{result}"


@pytest.mark.parametrize(
    ("data", "key"),
    [
        (b"AB", b"passkey"),
        (b"Hello, world! This a test string.", b"a longer passkey"),
    ],
)
def test_generator_with_key(data: bytes, key: bytes):
    key *= len(data) // len(key) + 1
    generator = ImageGenerator()
    encoded = generator.generate_image(data, key)
    encoded.save(f"{__file__}.png")
    interpreter = PietInterpreter(encoded, input=key, debug=True)
    exc = interpreter.run()
    if isinstance(exc, StepLimitReached):
        raise exc
    result = interpreter.output
    assert result == data, f"Output does not match input.\n{result}"
