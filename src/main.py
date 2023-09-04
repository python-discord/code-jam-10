import sys

from PyQt6.QtWidgets import QApplication

from src.Level import Level
from src.Window import Window


def main() -> None:
    """Main function"""
    app = QApplication(sys.argv)
    # Assuming the player is at level 1
    current_level = Level(1)
    window = Window(current_level)

    # Apply CSS (QSS) Styling
    with open('styles/styles.css') as qss:
        app.setStyleSheet(qss.read())

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
