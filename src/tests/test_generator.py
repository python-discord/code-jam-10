from io import BytesIO

import pytest

from src.piet import ImageGenerator, PietInterpreter
from src.piet.interpreter import StepLimitReached
from src.piet.runtime import PietRuntime


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
    output_buffer = BytesIO()
    interpreter = PietInterpreter(encoded, debug=True, runtime=PietRuntime(output_buffer=output_buffer))
    exc = interpreter.run()
    if isinstance(exc, StepLimitReached):
        raise exc
    result = output_buffer.getvalue()
    assert result == data, f"Output does not match input.\n{result}"
