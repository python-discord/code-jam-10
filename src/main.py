import os
import sys

from PyQt6.QtWidgets import QApplication

from level import Level
from window import Window

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def main() -> None:
    """Main function"""
    app = QApplication(sys.argv)
    # Assuming the player is at level 1
    current_level = Level(1)
    window = Window(current_level)

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
