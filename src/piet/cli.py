from io import BytesIO
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
    cols: Optional[int] = None,
    input: str = "",
    step_limit: int = 1_000_000,
    debug: bool = False,
):
    print("Generating a Piet program...")
    print("This process may take a while, depending on the size of the data.")
    if input_path.exists():
        data = input_path.read_bytes()
    else:
        data = str(input_path).encode()
    command = f'python -m {__package__} run "{output_path}"'
    generator = ImageGenerator(input=input, step_limit=step_limit, debug=debug)
    key = input.encode()
    if key:
        key *= len(data) // len(key) + 1
        command += f' --input "{key.decode()}"'
    image = generator.generate_image(data, key, cols)
    image.save(output_path)
    print("\n")
    print("Successfully generated a Piet program!")
    print(f"Image saved to: {output_path}")
    print(f"You can run it with: {command}")


@app.command()
def run(
    image_path: Path,
    output_path: Annotated[Optional[Path], typer.Argument()] = None,
    execute: bool = False,
    input: str = "",
    step_limit: int = 1_000_000,
    debug: bool = False,
):
    print("Executing Piet program...")
    data = image_path.read_bytes()
    image = Image.open(image_path).convert("RGB")
    if input:
        input *= len(data) // len(input) + 1
    interpreter = PietInterpreter(
        image,
        input=input,
        step_limit=step_limit,
        debug=debug,
    )
    interpreter.runtime.output = output_path.open("wb") if output_path else BytesIO()
    interpreter.run()
    if not output_path:
        print(interpreter.output.decode())
    if execute:
        exec(interpreter.output)
    print("\n")
    print("Successfully executed the Piet program!")


if __name__ == "__main__":
    app()
