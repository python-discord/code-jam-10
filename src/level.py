from pathlib import Path
from typing import Dict, List, Tuple

from PyQt6.QtCore import Qt

from src.control_panel import ControlPanel

FilterItem = Tuple[Path, ControlPanel, Dict[str, Path]]
FilterList = List[FilterItem]


class Level:
    """Class to represent a level in the game."""

    def __init__(self, level_number: int):
        self.level_number = level_number
        self.secret_answer = self.get_secret_answer()
        self.img_source = self.get_image_source()
        self.filters = self.get_filters()

    def get_image_source(self) -> Path:
        """
        Get the image source for the level

        :return: Path of the image file
        """
        # This can be extended to retrieve images dynamically based on the level
        image_dir_path = Path(Path(__file__).parent, "images")
        if self.level_number == 1:
            return Path(image_dir_path, "sample.png")
        if self.level_number == 2:
            return Path(image_dir_path, "clockwork.jpg")
        if self.level_number == 3:
            return Path(image_dir_path, "desert.png")
        return Path(image_dir_path, "default.png")

    def get_secret_answer(self) -> str:
        """
        Get the secret answer for the level

        :return: secret string
        """
        # This can be extended to provide answers dynamically based on the level
        if self.level_number == 1:
            return "secret"
        if self.level_number == 2:
            return "secret2"
        if self.level_number == 3:
            return "Very secret"
        return "pythoncodejam2023"

    def get_filters(self) -> FilterList:
        """
        Get the filters for the level

        :return: list of filters
        """
        # This can be extended to provide filters dynamically based on the level

        icons_dir_path = Path(Path(__file__).parent, "icons")
        image_dir_path = Path(Path(__file__).parent, "images")
        filters = [
            [
                (
                    Path(icons_dir_path, "button_sample.png"),
                    ControlPanel(
                        "Image Differencing",
                        [
                            ("X", (0, 100), Qt.Orientation.Horizontal),
                            ("Y", (0, 100), Qt.Orientation.Horizontal),
                        ],
                    ),
                    {"second_image": Path(image_dir_path, "desert.jpg")},
                ),
                (
                    Path(icons_dir_path, "button_sample2.png"),
                    ControlPanel(
                        "Double Exposure",
                        [
                            (
                                "Exposure",
                                ("Image 1", "Image 2"),
                                Qt.Orientation.Horizontal,
                            )
                        ],
                    ),
                    {"second_image": Path(image_dir_path, "desert.jpg")},
                ),
                (
                    Path(icons_dir_path, "button_sample3.png"),
                    ControlPanel(
                        "Motion Manipulation",
                        [
                            ("Wavelength", (0, 100), Qt.Orientation.Horizontal),
                            ("Gap", (0, 100), Qt.Orientation.Horizontal),
                            ("Wave Height", (0, 100), Qt.Orientation.Horizontal),
                        ],
                    ),
                    {"second_image": Path(image_dir_path, "desert.jpg")},
                ),
            ],
            [
                (
                    Path(icons_dir_path, "button_sample.png"),
                    ControlPanel(
                        "Image Differencing",
                        [
                            ("X", (0, 100), Qt.Orientation.Horizontal),
                            ("Y", (0, 100), Qt.Orientation.Horizontal),
                        ],
                    ),
                    {"second_image": Path(image_dir_path, "doggo.jpg")},
                ),
                (
                    Path(icons_dir_path, "button_sample2.png"),
                    ControlPanel(
                        "Double Exposure",
                        [
                            (
                                "Exposure",
                                ("Image 1", "Image 2"),
                                Qt.Orientation.Horizontal,
                            )
                        ],
                    ),
                    {"second_image": Path(image_dir_path, "doggo.jpg")},
                ),
                (
                    Path(icons_dir_path, "button_sample3.png"),
                    ControlPanel(
                        "Motion Manipulation",
                        [
                            ("Wavelength", (0, 100), Qt.Orientation.Horizontal),
                            ("Gap", (0, 100), Qt.Orientation.Horizontal),
                            ("Wave Height", (0, 100), Qt.Orientation.Horizontal),
                        ],
                    ),
                    {"second_image": Path(image_dir_path, "doggo.jpg")},
                ),
            ],
            [
                (
                    Path(icons_dir_path, "button_sample.png"),
                    ControlPanel(
                        "Hidden in ASCII",
                        []
                    ),
                    {"second_image": Path(image_dir_path, "doggo.jpg")},
                )
            ]
        ]
        return filters[self.level_number - 1]

    def level_up(self) -> None:
        """
        Level up the game

        :return: None
        """
        self.level_number += 1
        self.secret_answer = self.get_secret_answer()
        self.img_source = self.get_image_source()
        self.filters = self.get_filters()
