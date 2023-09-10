import click

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


@main.command()
def cli():
    """Main entry point to the cli"""
    print("cli")
