from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget
)


class Filter(QWidget):
    """Filter"""

    def __init__(self, name: str, sliders_info: list):
        """Init

        Create a filter panel with a title and a set of sliders.

        :param name: Name of the filter.
        :param sliders_info: List of tuples. Each tuple should contain:
                             - label name (str)
                             - range for the slider (tuple)
                             - orientation of the slider (Qt.Orientation)
        """
        super().__init__()
        layout = QVBoxLayout(self)

        # Create and add title box
        title_box = self.create_panel_title(name)
        layout.addWidget(title_box)

        # Dynamically create sliders based on the provided sliders_info
        for slider_label, slider_range, slider_orientation in sliders_info:
            layout.addWidget(QLabel(slider_label))
            slider = QSlider(slider_orientation)
            slider_frame = self.style_slider(slider,
                                             slider_range,
                                             slider_orientation == Qt.Orientation.Horizontal)
            slider_frame.setMaximumHeight(45)
            layout.addWidget(slider_frame)

        layout.addStretch()

    @staticmethod
    def create_panel_title(name: str) -> QFrame:
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
        title_label = QLabel(name)
        title_label.setStyleSheet('font-size: 22px')
        title_centre.addWidget(QLabel())
        title_centre.addWidget(title_label)
        title_centre.addWidget(QLabel())

        return title_box

    @staticmethod
    def style_slider(slider: QSlider, range_value: tuple, horizontal: bool) -> QFrame:
        """
        Style PyQt6 sliders for consistency

        :param range_value:
        :param slider:
        :param slider, range_value, horizontal:
        :return: QFrame slider
        """
        slider_frame = QFrame()
        slider_frame.setObjectName('sliderframe')
        slider_frame.setStyleSheet('QFrame#sliderframe { '
                                   'border: 1px solid "black";'
                                   'border-radius: 6px;'
                                   'background-color: "white"; }')

        slider_layout = QHBoxLayout(slider_frame) if horizontal else QVBoxLayout(slider_frame)
        slider_layout.addWidget(QLabel(str(range_value[0])))
        slider_layout.addWidget(slider)
        slider_layout.addWidget(QLabel(str(range_value[-1])))

        return slider_frame
