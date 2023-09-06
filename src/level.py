from pathlib import Path

from PyQt6.QtCore import Qt

from control_panel import ControlPanel


class Level:
    """Class to represent a level in the game/application."""

    def __init__(self, level_number: int):
        self.level_number = level_number
        self.secret_answer = self.get_secret_answer()
        self.img_source = self.get_image_source()
        self.filters = self.get_filters()

    def set_level(self, level_number: int):
        image_dir_path = Path(Path(__file__).parent, 'images')

        self.level_number = level_number
        self.img_source = Path(image_dir_path, 'clockwork.jpg')
        self.secret_answer = self.get_secret_answer()
        self.filters = self.get_filters()

    def get_image_source(self) -> Path:
        """
        Get the image source for the level

        :return: str
        """
        # This can be extended to retrieve images dynamically based on the level

        image_dir_path = Path(Path(__file__).parent, 'images')
        if self.level_number == 1:
            return Path(image_dir_path, 'sample.png')
        if self.level_number == 2:
            return Path(image_dir_path, 'clockwork.jpg')
        return Path(image_dir_path, 'default.png')

    def get_secret_answer(self) -> str:
        """
        Get the secret answer for the level

        :return: str
        """
        # This can be extended to provide answers dynamically based on the level
        if self.level_number == 1:
            return 'secret'
        if self.level_number == 2:
            return 'secret2'
        return 'pythoncodejam2023'

    def get_filters(self) -> list:
        """
        Get the filters for the level

        :return: list
        """
        # This can be extended to provide filters dynamically based on the level

        icons_dir_path = Path(Path(__file__).parent, 'icons')
        image_dir_path = Path(Path(__file__).parent, 'images')
        if self.level_number == 1:
            filters = [
                (
                    Path(icons_dir_path, 'button_sample.png'),
                    ControlPanel(
                        'Image Differencing',
                        [('X', (0, 100), Qt.Orientation.Horizontal),
                         ('Y', (0, 100), Qt.Orientation.Horizontal)]
                    ),
                    {"second_image": Path(image_dir_path, 'desert.jpg')}
                ),
                (
                    Path(icons_dir_path, 'button_sample2.png'),
                    ControlPanel(
                        'Double Exposure',
                        [('Exposure', ('Image 1', 'Image 2'), Qt.Orientation.Horizontal)]
                    ),
                    {"second_image": Path(image_dir_path, 'desert.jpg')}
                ),
                (
                    Path(icons_dir_path, 'button_sample3.png'),
                    ControlPanel(
                        'Motion Manipulation',
                        [('Wavelength', (0, 100), Qt.Orientation.Horizontal),
                         ('Gap', (0, 100), Qt.Orientation.Horizontal),
                         ('Wave Height', (0, 100), Qt.Orientation.Horizontal)]
                    ),
                    {"second_image": Path(image_dir_path, 'desert.jpg')}
                )
            ]
            return filters
        if self.level_number == 2:
            return [
                (
                    Path(icons_dir_path, 'button_sample.png'),
                    ControlPanel(
                        'Image Differencing',
                        [
                            ('X', (0, 100), Qt.Orientation.Horizontal),
                            ('Y', (0, 100), Qt.Orientation.Horizontal)
                        ]
                    ),
                    {}
                ),
                (
                    Path(icons_dir_path, 'button_sample2.png'),
                    ControlPanel(
                        'Double Exposure',
                        [('Exposure', ('Image 1', 'Image 2'), Qt.Orientation.Horizontal)]
                    ),
                    {}
                ),
                (
                    Path(icons_dir_path, 'button_sample3.png'),
                    ControlPanel(
                        'Motion Manipulation',
                        [
                            ('Wavelength', (0, 100), Qt.Orientation.Horizontal),
                            ('Gap', (0, 100), Qt.Orientation.Horizontal),
                            ('Wave Height', (0, 100), Qt.Orientation.Horizontal)
                        ]
                    ),
                    {}
                )
            ]

        return []
