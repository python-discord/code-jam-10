from PIL import Image
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget
)

from src.Utils.apply_double_exposure import apply_double_exposure


class Filter(QWidget):
    """Filter"""

    # Define a custom signal to be emitted when any slider changes its value
    sliderValueChanged = pyqtSignal(str, int)

    def __init__(self, name: str, sliders_info: list):
        """Init"""
        super().__init__()

        self.name = name
        self.sliders = {}  # Dictionary to store sliders with their labels as keys

        layout = QVBoxLayout(self)

        title_box = self.create_panel_title(name)
        layout.addWidget(title_box)

        for slider_label, slider_range, slider_orientation in sliders_info:
            layout.addWidget(QLabel(slider_label))
            slider = QSlider(slider_orientation)
            slider.setRange(*slider_range)
            slider.valueChanged.connect(lambda value, lbl=slider_label: self._on_slider_value_changed(lbl, value))
            slider_frame = self.style_slider(slider, slider_range, slider_orientation == Qt.Orientation.Horizontal)
            layout.addWidget(slider_frame)

            self.sliders[slider_label] = slider

        layout.addStretch()

    def _on_slider_value_changed(self, label, value):
        self.sliderValueChanged.emit(label, value)

    def get_slider_value(self, label):
        return self.sliders[label].value()

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


def apply_filter(level, filter_name, args: dict) -> QPixmap:
    """
    Apply a filter to an image

    :param level:
    :param filter_name:
    :param args:
    :return: img
    """
    print("Type of args: ", type(args))
    print("Args: ", args)

    if filter_name == "Double Exposure":
        new_img = apply_double_exposure(args["img_to_edit"], args["img_path"], args["slider_value"])
        return new_img

    pass

