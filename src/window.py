from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QFrame, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMessageBox, QPushButton, QStackedLayout, QWidget
)

from level import Level
from dock import Dock


class Window(QMainWindow):
    """Main Window"""

    def __init__(self, level: Level) -> None:
        super().__init__()
        self.secret_answer = level.secret_answer
        self.level = level
        self.secret_code = ""
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize the User Interface"""
        self.window_name = 'Digital Shadows - Async Aggregators'
        self.setWindowTitle(f"{self.window_name} - Level {self.level.level_number}")
        layout = self._create_main_layout()

        widget = QWidget()
        widget.setLayout(layout)
        widget.setMinimumSize(850, 450)
        widget.setMaximumHeight(450)
        self.setCentralWidget(widget)

    def _create_main_layout(self) -> QGridLayout:
        """Create the main layout of the application"""
        main_layout = QGridLayout()

        spacer = QLabel()
        main_layout.addWidget(spacer, 0, 0)
        main_layout.addWidget(spacer, 3, 3)

        # Image display
        image_display = self._create_image_display()
        main_layout.addWidget(image_display, 1, 1)

        # Central dock
        self.dock = Dock(self.level, self.img_label, self._update_secret_code)  # Pass img_label as an argument
        main_layout.addWidget(self.dock, 2, 1)

        return main_layout

    def _create_image_display(self) -> QWidget:
        """Create and return the image display area."""
        frame = QFrame(self)
        frame.setObjectName("image_display_frame")
        frame.setStyleSheet('QFrame#image_display_frame {'
                            'border: 1px solid "black"; '
                            'border-radius: 6px; '
                            'background-color: "#e4e0e0"; }')

        layout = QHBoxLayout(frame)
        img = QPixmap(str(self.level.img_source)).scaled(450, 450, Qt.AspectRatioMode.KeepAspectRatio)

        # Convert img_label to an instance variable
        self.img_label = QLabel(self)
        self.img_label.setPixmap(img)

        layout.addWidget(self.img_label)
        layout.addLayout(self._create_tabbed_controls())

        return frame

    def _create_tabbed_controls(self) -> QStackedLayout:
        """Create the tabbed controls layout"""
        layout = QStackedLayout()

        for filter_item in self.level.filters:
            layout.addWidget(filter_item[1])

        return layout

    def _update_secret_code(self, input_code: str) -> None:
        """Update the internal secret code and check against the answer."""
        self.secret_code = input_code

        if self.secret_code != self.secret_answer:
            # If the input does not match the answer, show a notification
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Error')
            msg_box.setText('Incorrect secret code.')
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.exec()
        else:
            # If the input matches the answer, show a notification
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Success')
            msg_box.setText('Correct secret code.')
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.exec()

            self.level.level_number += 1
            self.setWindowTitle(f'{self.window_name} - Level {self.level.level_number}')
