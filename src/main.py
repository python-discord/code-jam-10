import sys

from PyQt6.QtWidgets import QApplication
from sklearn.externals._packaging.version import parse

from src.level import Level
from src.window import Window


def parse_level_input(args):
    max_level = 5
    if len(args) == 0:
        level = 1
    elif len(args) == 1:
        try:
            level = int(args[0])
        except ValueError:
            raise ValueError("First argument is not an integer")
    else:
        raise ValueError("Too many arguments specified")
    if level < 1 or level > max_level:
        raise ValueError(
            f"Invalid level number. Please pick a number between 1 and {max_level}"
        )
    return level


def main(args: list) -> None:
    """Main function"""
    app = QApplication(sys.argv)
    current_level = Level(parse_level_input(args))
    window = Window(current_level)
    window.showMaximized()
    sys.exit(app.exec())
