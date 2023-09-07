import sys

from PyQt6.QtWidgets import QApplication

from src.level import Level
from src.window import Window


def main() -> None:
    """Main function"""
    app = QApplication(sys.argv)
    # Assuming the player is at level 1
    current_level = Level(2)
    window = Window(current_level)

    window.show()
    sys.exit(app.exec())
