import sys

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QApplication, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSlider, QStackedLayout, QVBoxLayout, QWidget, QFrame
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
        self.setWindowTitle("Digital Shadows - Async Aggregators")
        img_source = 'Images/sample.png'

        # Contains buttons + their filter panel
        # (button icon, filter, layer)
        filters = [('icons/button_sample.png', self.img_difference(),
                    lambda: self.control_tabs.setCurrentIndex(0)),
                   ('icons/button_sample2.png', self.double_exposure(),
                    lambda: self.control_tabs.setCurrentIndex(1)),
                   ('icons/button_sample3.png', self.motion_mani(),
                    lambda: self.control_tabs.setCurrentIndex(2))]

        layout = self.create_main_layout(img_source, filters)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setMinimumSize(850, 550)
        self.setCentralWidget(widget)

    def create_main_layout(self, img_source: str, filters: list) -> QGridLayout:
        """
        Create the main layout of the application

        :param img_source:
        :return: self.padding
        """
        # Layouts
        self.padding = QGridLayout()
        self.body = QVBoxLayout()

        self.display_frame = QFrame(self)
        self.display_frame.setObjectName("display_frame")
        self.display_frame.setMinimumSize(200, 0)
        self.display_panel = QHBoxLayout(self.display_frame)

        self.dockframe = QFrame(self)
        self.dockframe.setObjectName("dockframe")
        self.dockframe.setMinimumSize(200, 50)
        self.dock = QHBoxLayout(self.dockframe)

        self.filter_dock = QHBoxLayout()
        self.control_tabs = QStackedLayout()
        self.centre_dock = QHBoxLayout()

        self.padding.addWidget(QLabel(), 0, 3)
        self.padding.addWidget(QLabel(), 3, 0)
        self.padding.addLayout(self.body, 2, 2)

        # Main displays (image + filter controls)
        self.body.addWidget(self.display_frame)
        self.display_panel.addWidget(self.create_image_widget(img_source))
        self.display_panel.addLayout(self.control_tabs)

        # Add all panels for filters
        for i in filters:
            self.control_tabs.addWidget(i[1])

        # Dock and filters
        self.body.addLayout(self.centre_dock)
        spacing = QLabel()
        spacing.setMinimumSize(100, 0)
        self.centre_dock.addWidget(spacing)
        self.centre_dock.addWidget(self.dockframe)
        self.centre_dock.addWidget(spacing)

        # Secret code input field
        self.dock.addLayout(self.filter_dock)
        self.check_input = QLineEdit(' Secret Code')
        self.check_input.setObjectName("check_input")
        self.check_input.setMinimumSize(100, 40)
        self.dock.addWidget(self.check_input)

        # Clear secret code input field
        self.close = QPushButton()
        self.close.setMinimumSize(40, 40)
        self.close.setIcon(QIcon('icons\\close.png'))
        self.close.setIconSize(QSize(20, 20))
        self.close.pressed.connect(lambda: self.check_input.setText(''))
        self.filter_dock.addWidget(self.close)
        self.dock.addWidget(self.close)

        # Button filters (left side of dock)
        for j, i in enumerate(filters):
            btn = QPushButton()
            btn.setMinimumSize(40, 40)
            btn.setIcon(QIcon(i[0]))
            btn.setIconSize(QSize(40, 40))
            btn.pressed.connect(i[2])
            self.filter_dock.addWidget(btn)

        # Display first filter control panel
        self.control_tabs.setCurrentIndex(0)

        return self.padding

    def create_image_widget(self, img_source: str) -> QLabel:
        """
        Create the image widget

        :param img_source:
        :return: image widget
        """
        img = QLabel(self)
        image = QPixmap(img_source).scaled(450, 450, Qt.AspectRatioMode.KeepAspectRatio)
        img.setPixmap(image)

        return img

    def create_panel_title(self, name: str) -> QFrame:
        """
        Stylised control panel title for consistency

        :param name:
        :return: QFrame panel title
        """
        title_box = QFrame()
        object_name = '_'.join(name.lower().split())
        
        title_box.setObjectName(object_name + '_box')
        title_box.setMinimumSize(200, 0)
        title_box.setStyleSheet(f'QFrame#{object_name + "_box"}'
                                '{ border: 1px solid "black"; '
                                'border-radius: 6px; '
                                'background-color: "white"; }')

        title_centre = QHBoxLayout(title_box)

        title = QLabel(name)
        title.setStyleSheet('font-size: 22px')

        title_centre.addWidget(QLabel())
        title_centre.addWidget(title)
        title_centre.addWidget(QLabel())

        return title_box

    def style_slider(self, slider: QSlider,
                     range_value: tuple, horizontal: bool) -> QFrame:
        """
        Style PyQt6 sliders for consistency

        :param slider, range_value, horizontal:
        :return: QFrame slider
        """
        slider_frame = QFrame()
        slider_frame.setObjectName('sliderframe')
        slider_frame.setStyleSheet('QFrame#sliderframe { '
                                   'border: 1px solid "black";'
                                   'border-radius: 6px;'
                                   'background-color: "white"; }')

        if horizontal:
            slider_layout = QHBoxLayout(slider_frame)
        else:
            slider_layout = QVBoxLayout(slider_frame)

        slider_layout.addWidget(QLabel(str(range_value[0])))
        slider_layout.addWidget(slider)
        slider_layout.addWidget(QLabel(str(range_value[-1])))

        return slider_frame

    def img_difference(self) -> QWidget:
        """
        Image difference control panel (example)

        :return: image difference control panel
        """
        container = QWidget()
        img_diff = QVBoxLayout(container)

        title_box = self.create_panel_title('Image Differencing')
        img_diff.addWidget(title_box)

        img_diff.addWidget(QLabel('X'))
        slider_x = QSlider(Qt.Orientation.Horizontal)
        slider_xframe = self.style_slider(slider_x, (0, 100), True)
        slider_xframe.setMaximumHeight(45)
        img_diff.addWidget(slider_xframe)

        img_diff.addWidget(QLabel('Y'))
        slider_y = QSlider(Qt.Orientation.Horizontal)
        slider_yframe = self.style_slider(slider_y, (0, 100), True)
        slider_yframe.setMaximumHeight(45)
        img_diff.addWidget(slider_yframe)

        img_diff.addStretch()

        return container

    def motion_mani(self) -> QWidget:
        """
        Motion manipulation control panel (example)

        :return: motion manipulation control panel
        """
        container = QWidget()
        img_diff = QVBoxLayout(container)

        title_box = self.create_panel_title('Motion Manipulation')
        img_diff.addWidget(title_box)

        img_diff.addWidget(QLabel('Wavelength'))
        slider_x = QSlider(Qt.Orientation.Horizontal)
        slider_xframe = self.style_slider(slider_x, (0, 100), True)
        slider_xframe.setMaximumHeight(45)
        img_diff.addWidget(slider_xframe)

        img_diff.addWidget(QLabel('Gap'))
        slider_x = QSlider(Qt.Orientation.Horizontal)
        slider_xframe = self.style_slider(slider_x, (0, 100), True)
        slider_xframe.setMaximumHeight(45)
        img_diff.addWidget(slider_xframe)

        img_diff.addWidget(QLabel('Wave Height'))
        slider_x = QSlider(Qt.Orientation.Horizontal)
        slider_xframe = self.style_slider(slider_x, (0, 100), True)
        slider_xframe.setMaximumHeight(45)
        img_diff.addWidget(slider_xframe)

        img_diff.addStretch()

        return container

    def double_exposure(self) -> QWidget:
        """
        Double exposure control panel (example)

        :return: double exposure control panel
        """
        container = QWidget()
        img_diff = QVBoxLayout(container)

        title_box = self.create_panel_title('Double Exposure')
        img_diff.addWidget(title_box)

        img_diff.addWidget(QLabel('Exposure'))
        slider_x = QSlider(Qt.Orientation.Horizontal)
        slider_xframe = self.style_slider(slider_x, ('Image 1', 'Image 2'), True)
        slider_xframe.setMaximumHeight(45)
        img_diff.addWidget(slider_xframe)

        img_diff.addStretch()

        return container


# Driver Code
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    # Apply CSS (QSS) Styling
    with open('styles/styles.css') as qss:
        app.setStyleSheet(qss.read())

    window.show()
    sys.exit(app.exec())
