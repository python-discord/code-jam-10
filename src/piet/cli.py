from pathlib import Path
from typing import Annotated, Optional

import typer
from PIL import Image

from .generator import ImageGenerator
from .interpreter import PietInterpreter

app = typer.Typer()


@app.command()
def generate(
    input_path: Path,
    output_path: Path,
    cols: int = 2,
    input: str = "",
    step_limit: int = 1_000_000,
    debug: bool = False,
):
    if input_path.exists():
        data = input_path.read_bytes()
    else:
        data = str(input_path).encode()
    generator = ImageGenerator(input=input, step_limit=step_limit, debug=debug)
    key = input.encode()
    key *= len(data) // len(key) + 1
    image = generator.generate_image(data, cols, key)
    image.save(output_path)


@app.command()
def run(
    image_path: Path,
    output_path: Annotated[Optional[Path], typer.Argument()] = None,
    input: str = "",
    step_limit: int = 1_000_000,
    debug: bool = False,
):
    image = Image.open(image_path).convert("RGB")
    interpreter = PietInterpreter(
        image,
        input=input,
        step_limit=step_limit,
        debug=debug,
    )
    if output_path:
        interpreter.runtime.output = output_path.open("wb")
    interpreter.run()
    print(interpreter.output.decode())


if __name__ == "__main__":
    app()
