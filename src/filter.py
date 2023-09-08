from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget
)

from src.Utils.apply_color_swap import apply_color_swap
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

    def _on_slider_value_changed(self, label: str, value: int) -> None:
        """
        Forward the signal from the slider to the main window

        :param label:
        :param value:
        :return:
        """
        self.sliderValueChanged.emit(label, value)

    def get_slider_value(self, label: str) -> int:
        """
        Get the value of a slider

        :param label:
        :return:
        """
        return self.sliders[label].value()

    @staticmethod
    def create_panel_title(name: str) -> QFrame:
        """
        Stylised control panel title for consistency

        :param name:
        :return: QFrame panel title
        """
        title_box = QFrame()
        object_name = "_".join(name.lower().split())
        title_box.setObjectName(object_name + "_box")
        title_box.setMinimumSize(200, 0)
        title_box.setStyleSheet(
            f"QFrame#{object_name + '_box'}"
            "{ border: 1px solid 'black'; "
            "border-radius: 6px; "
            "background-color: 'white'; }"
        )

        title_centre = QHBoxLayout(title_box)
        title_label = QLabel(name)
        title_label.setStyleSheet("font-size: 22px")
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
        slider_frame.setObjectName("sliderframe")
        slider_frame.setStyleSheet(
            "QFrame#sliderframe { "
            "border: 1px solid 'black';"
            "border-radius: 6px;"
            "background-color: 'white'; }"
        )

        slider_layout = (
            QHBoxLayout(slider_frame) if horizontal else QVBoxLayout(slider_frame)
        )
        slider_layout.addWidget(QLabel(str(range_value[0])))
        slider_layout.addWidget(slider)
        slider_layout.addWidget(QLabel(str(range_value[-1])))

        return slider_frame


def apply_filter(filter_name: str, args: dict, secret: str) -> QPixmap:
    """
    Apply a filter to an image

    :param filter_name:
    :param args:
    :param secret: level secret
    :return: img
    """
    if filter_name == "Double Exposure":
        return apply_double_exposure(
            args["image_to_edit"], args["second_image"], args["slider_value"]
        )
    if filter_name == "Color Swap":
        return apply_color_swap(
            args["image_to_edit"], args["first_color"], args["second_color"]
        )
    if filter_name == "Hidden in ASCII":
        input_img, coordinates = prepare_input(args["image_to_edit"])
        lib_dir_path = Path(Path(__file__).parent.parent, "lib")
        image_dir_path = Path(Path(__file__).parent, "images")
        ascii_file_path = Path(lib_dir_path, "hidden_in_ascii/ascii.txt")
        output_img_path = Path(image_dir_path, "ascii_output.png")
        generate_ascii_file(input_img, ascii_file_path, 2)   # TODO density should be read from args
        seed_secret(ascii_file_path, secret, False)  # TODO binary mode should be read from args
        output_img = ascii_to_img(ascii_file_path, coordinates, input_img.size, output_img_path)
        qimage = QImage(
            output_img.tobytes(),
            output_img.width,
            output_img.height,
            output_img.width * 3,  # Assuming RGB color mode
            QImage.Format_RGB888,
        )
        return QPixmap.fromImage(qimage)

    pass
