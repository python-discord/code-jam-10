import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSlider, QStackedLayout, QVBoxLayout, QWidget
)


class MainWindow(QMainWindow):
    """Main Window"""

    def __init__(self) -> None:
        super().__init__()
        self.level = 1
        self.init_ui()

    def init_ui(self) -> None:
        """
        Initialize the User Interface

        :return: None
        """
        self.setWindowTitle("CodeJam Async Aggregators")
        img_source = 'Images/sample.png'

        layout = self.create_main_layout(img_source)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def create_main_layout(self, img_source: str) -> QGridLayout:
        """
        Create the main layout of the application

        :param img_source:
        :return: padding
        """
        # Layouts
        padding = QGridLayout()
        body = QVBoxLayout()
        display_panel = QHBoxLayout()
        dock = QHBoxLayout()
        filter_layout = QHBoxLayout()
        control_tabs = QStackedLayout()

        # Padding
        padding.addWidget(QLabel(), 0, 3)
        padding.addWidget(QLabel(), 3, 0)
        padding.addLayout(body, 2, 2)

        # Main displays (image + filter controls)
        body.addLayout(display_panel)
        display_panel.addWidget(self.create_image_widget(img_source))
        display_panel.addLayout(control_tabs)

        control_tabs.addWidget(self.create_control_panel())

        # Dock and filters
        body.addLayout(dock)
        dock.addLayout(filter_layout)
        dock.addWidget(QLineEdit('Secret Code'))

        for _ in range(5):
            filter_layout.addWidget(QPushButton())

            # Display Z-Index
            control_tabs.setCurrentIndex(self.level)

            return padding

    def create_image_widget(self, img_source: str) -> QLabel:
        """
        Create the image widget

        :param img_source:
        :return: image widget
        """
        img = QLabel(self)
        image = QPixmap(img_source).scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio)
        img.setPixmap(image)
        img.setObjectName("image")
        img.setProperty("id", "image-display")

        return img

    def create_control_panel(self) -> QWidget:
        """
        Create the control panel

        :return: control panel
        """
        container = QWidget()
        img_diff = QVBoxLayout(container)

        img_diff.addWidget(QLabel('Image Differencing'))
        img_diff.addWidget(QLabel('X'))
        img_diff.addWidget(QSlider(Qt.Orientation.Horizontal))
        img_diff.addWidget(QLabel('Y'))
        img_diff.addWidget(QSlider(Qt.Orientation.Horizontal))

        return container


# Driver Code
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
