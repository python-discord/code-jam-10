from pathlib import Path

import click

from app import steganography

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


@cli.command()
def obfuscate():
    """Entrypoint to obfuscate command"""
    print("TODO - obfuscation on CLI")
