from pathlib import Path
from typing import Annotated, Optional

import typer
from PIL import Image

from .generator import ImageGenerator
from .interpreter import PietInterpreter
from .runtime import PietRuntime

app = typer.Typer()


@app.command()
def generate(
    input_path: Path,
    output_path: Path,
    cols: int = 2,
):
    if input_path.exists():
        data = input_path.read_bytes()
    else:
        data = str(input_path).encode()
    generator = ImageGenerator()
    image = generator.generate_image(data, cols)
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
    extra_args = {}
    if output_path:
        output_buffer = output_path.open("wb")
        extra_args["runtime"] = PietRuntime(output_buffer=output_buffer)
    interpreter = PietInterpreter(
        image,
        input=input,
        step_limit=step_limit,
        debug=debug,
        **extra_args,
    )
    interpreter.run()


if __name__ == "__main__":
    app()
