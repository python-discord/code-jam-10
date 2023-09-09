from io import StringIO

import pytest

from src.piet import PietInterpreter, PietProgramGenerator, PietRuntime
from src.piet.interpreter import StepLimitReached


@pytest.mark.parametrize(
    ("data", "cols"),
    [
        (b"AB", 1),
        (b"Hello, world! This a test string.", 4),
    ],
)
def test_generator(data: bytes, cols: int):
    generator = PietProgramGenerator()
    encoded = generator.generate_image(data, cols)
    encoded.save(f"{__file__}.png")
    output_buffer = StringIO()
    interpreter = PietInterpreter(encoded, debug=True, runtime=PietRuntime(output_buffer=output_buffer))
    exc = interpreter.run()
    if isinstance(exc, StepLimitReached):
        raise exc
    assert output_buffer.getvalue().encode() == data, f"Output does not match input.\n{output_buffer.getvalue()}"
