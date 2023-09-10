from pathlib import Path

import click
from PIL import Image
from rich.console import Console

from app import obfuscate, steganography

from .ui import main as ui_main


@click.group(invoke_without_command=False)
@click.pass_context
def main(ctx):
    """Main entry point to application"""
    pass


@main.command()
def ui():
    """Main entry point to the ui"""
    ui_main()


@main.group(invoke_without_command=False)
def cli():
    """Main entry point to the cli"""
    pass


@cli.group(invoke_without_command=False)
def watermark():
    """Entrypoint to watermark subcommand"""
    pass


@watermark.command("encode")
@click.argument("text", type=str)
@click.argument(
    "infile",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
)
@click.argument(
    "outfile",
    type=click.Path(exists=False, dir_okay=False, file_okay=True, writable=True),
)
def watermark_encode(text: str, infile: Path, outfile: Path):
    """Entrypoint to watermark encode command"""
    steganography.encode(text, infile, outfile, steganography.Lsb())


@watermark.command("decode")
@click.argument(
    "infile",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
)
def watermark_decode(infile: Path):
    """Entrypoint to watermark decode command"""
    lsb = steganography.Lsb()
    result = steganography.decode(infile, lsb)
    if result:
        click.echo(result)
    else:
        click.echo(f"no encoded data found in {infile}")


@cli.command("obfuscate")
@click.option("--mode", "-m", type=click.Choice(["blur", "colour"]))
@click.option("--colour", "-c", type=str, default="black", required=False)
@click.option("--regex/--no-regex", type=bool, default=False)
@click.argument(
    "infile",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
)
@click.argument(
    "outfile",
    type=click.Path(exists=False, dir_okay=False, file_okay=True, writable=True),
)
@click.argument("filters", type=str, nargs=-1)
def obfuscate_cmd(
    mode: str, colour: str, regex: bool, infile: Path, outfile: Path, filters: list[str]
):
    """Entrypoint to obfuscate command"""
    # setup obfuscator
    obfuscator = obfuscate.ColourBox(colour)
    if mode == "blur":
        obfuscator = obfuscate.BlurBox()
    elif mode == "colour":
        obfuscator = obfuscate.ColourBox(colour)

    img = Image.open(infile)

    console = Console()
    with console.status("[bold green]Working on obfuscation..."):
        for text in filters:
            bounds = obfuscate.find_bounds(infile, text, regex)
            for bound in bounds:
                obfuscator.hide(bound, img)
            console.log(f"text '{text}' obfuscated")
    img.save(outfile)
