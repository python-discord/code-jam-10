from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class Dock(QWidget):
    """Dock"""

    def __init__(self, filters: list):
        super().__init__()
        layout = QHBoxLayout(self)

        # ... [setup code]

        # Button filters
        for _, icon, action in filters:
            btn = QPushButton()
            btn.setMinimumSize(40, 40)
            btn.setIcon(QIcon(icon[0]))
            btn.setIconSize(QSize(40, 40))
            btn.pressed.connect(action)
            layout.addWidget(btn)

        # ... [rest of the setup code]

    # Any other dock-related methods can be added here
