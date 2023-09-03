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
        super(MainWindow, self).__init__()

        self.setWindowTitle("CodeJam Async Aggregators")
        img_source = 'Images/sample.png'
        level = 1

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

        # Image
        img = QLabel(self)
        image = QPixmap(img_source).scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio)

        img.setPixmap(image)
        img.setObjectName("image")
        img.setProperty("id", "image-display")
        display_panel.addWidget(img)

        display_panel.addLayout(control_tabs)

        # Control panel
        container = QWidget()

        # Layer Stack (z-index)
        img_diff = QVBoxLayout(container)

        control_tabs.addWidget(container)

        # Image Differencing (Example)
        img_diff.addWidget(QLabel('Image Differencing'))
        img_diff.addWidget(QLabel('X'))
        img_diff.addWidget(QSlider(Qt.Orientation.Horizontal))
        img_diff.addWidget(QLabel('Y'))
        img_diff.addWidget(QSlider(Qt.Orientation.Horizontal))

        body.addLayout(dock)
        dock.addLayout(filter_layout)

        # Submit
        dock.addWidget(QLineEdit('Secret Code'))

        # Filters buttons (located on the dock)
        filter_layout.addWidget(QPushButton())
        filter_layout.addWidget(QPushButton())
        filter_layout.addWidget(QPushButton())
        filter_layout.addWidget(QPushButton())
        filter_layout.addWidget(QPushButton())

        # Display Z-Index
        control_tabs.setCurrentIndex(level)

        widget = QWidget()
        widget.setLayout(padding)
        self.setCentralWidget(widget)


# Driver Code
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
