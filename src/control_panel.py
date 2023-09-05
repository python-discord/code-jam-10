from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget
)


class ControlPanel(QWidget):
    """Control Panel"""

    def __init__(self, title: str, sliders_info: list):
        super().__init__()
        layout = QVBoxLayout(self)

        title_box = self.create_panel_title(title)
        layout.addWidget(title_box)

        for info in sliders_info:
            label, slider_range, orientation = info
            layout.addWidget(QLabel(label))
            slider = QSlider(orientation)
            slider_frame = self.style_slider(slider, slider_range, orientation == Qt.Orientation.Horizontal)
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

        title = QLabel(name)
        title.setStyleSheet('font-size: 22px')

        title_centre.addWidget(QLabel())
        title_centre.addWidget(title)
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

        if horizontal:
            slider_layout = QHBoxLayout(slider_frame)
        else:
            slider_layout = QVBoxLayout(slider_frame)

        slider_layout.addWidget(QLabel(str(range_value[0])))
        slider_layout.addWidget(slider)
        slider_layout.addWidget(QLabel(str(range_value[-1])))

        return slider_frame
