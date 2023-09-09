from pathlib import Path
from typing import Dict, List, Tuple, cast

from PIL import Image
from PyQt6.QtCore import Qt

from lib.hidden_in_ascii.hidden_in_ascii import (
    ascii_to_img, generate_ascii_file, prepare_input, seed_secret
)
from lib.motions.motions import MotionTransformer
from src.control_panel import ControlPanel

FilterItem = Tuple[Path, ControlPanel, Dict[str, Path | str | None | int]]
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
            return Path(image_dir_path, "reverse_ishihara.png")
        if self.level_number == 2:
            return Path(image_dir_path, "clockwork.jpg")
        if self.level_number == 3:
            return Path(image_dir_path, "number_hidden_image.png")
        if self.level_number == 4:
            input_img, coordinates = prepare_input(Path(image_dir_path, "desert.jpg"))
            output_img_path = Path(image_dir_path, "ascii_output.png")
            ascii_file_path = Path(image_dir_path, "ascii.txt")
            generate_ascii_file(input_img, ascii_file_path, 2)
            seed_secret(ascii_file_path, self.get_secret_answer(), False)
            ascii_to_img(ascii_file_path, coordinates, input_img.size, output_img_path)
            return output_img_path
        if self.level_number == 5:
            return Path(image_dir_path, "img2.jpg")
        return Path(image_dir_path, "default.png")

    def get_secret_answer(self) -> str:
        """
        Get the secret answer for the level

        :return: secret string
        """
        # This can be extended to provide answers dynamically based on the level
        if self.level_number == 1:
            return "42"
        if self.level_number == 2:
            return "secret2"
        if self.level_number == 3:
            return "200012"
        if self.level_number == 4:
            return "secret"
        if self.level_number == 5:
            return "secret"
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
                    Path(icons_dir_path, "rishihara.png"),
                    ControlPanel(
                        "Ishihara",
                        {
                            "sliders": [
                                ("A", (0, 100), Qt.Orientation.Horizontal, True),
                                ("B", (0, 100), Qt.Orientation.Horizontal, True),
                            ],
                            "dropdowns": [],
                        },
                    ),
                    {
                        "second_image": None,
                        "secret_code": "42",
                        "MotionTransformer": None,
                    },
                ),
            ],
            [
                (
                    Path(icons_dir_path, "button_sample2.png"),
                    ControlPanel(
                        "Double Exposure",
                        {
                            "sliders": [
                                (
                                    "Exposure",
                                    ("Image 1", "Image 2"),
                                    Qt.Orientation.Horizontal,
                                    False
                                )
                            ],
                            "dropdowns": [],
                        },
                    ),
                    {
                        "second_image": Path(image_dir_path, "doggo.jpg"),
                        "secret_code": "secret",
                        "MotionTransformer": None,
                    },
                ),
            ],
            [
                (
                    Path(icons_dir_path, "button_sample4.png"),
                    ControlPanel(
                        "Color Swap",
                        {
                            "sliders": [],
                            "dropdowns": [
                                ["Rust", "Chocolate", "Flamenco", "Casablanca", "Buff"]
                            ],
                            "buttons": ["swap"],
                        },
                    ),
                    {},
                )
            ],
            [
                (
                    Path(icons_dir_path, "rishihara.png"),
                    ControlPanel(
                        "Motion",
                        {
                            "sliders": [
                                (
                                    "horizontal wave",
                                    (0, 100),
                                    Qt.Orientation.Horizontal,
                                    False
                                ),
                                ("vertical wave", (0, 100), Qt.Orientation.Horizontal, False),
                                ("vertical spike", (0, 100), Qt.Orientation.Horizontal, False),
                                (
                                    "horizontal spike",
                                    (0, 100),
                                    Qt.Orientation.Horizontal,
                                    False)
                            ],
                            "dropdowns": [],
                        },
                    ),
                    {
                        "second_image": None,
                        "secret_code": "Turbo secret",
                        "MotionTransformer": MotionTransformer(
                            Image.open(image_dir_path / "img2.jpg")
                        ),
                    },
                ),
            ],
            [
                (
                    Path(icons_dir_path, "magnifying_glass.png"),
                    ControlPanel(
                        "Hidden in ASCII",
                        {
                            "sliders": [],
                            "dropdowns": [],
                            # "buttons": [
                            #     "zoom in",
                            #     "zoom out"
                            # ]
                        }
                    ),
                    {},
                )
            ]
        ]


        if 0 <= self.level_number - 1 < len(filters):
            return cast(FilterList, filters[self.level_number - 1])
        else:
            # Return an empty FilterList if out-of-bounds
            return []

    def level_up(self) -> None:
        """
        Level up the game

        :return: None
        """
        self.level_number += 1
        self.secret_answer = self.get_secret_answer()
        self.img_source = self.get_image_source()
        self.filters = self.get_filters()
