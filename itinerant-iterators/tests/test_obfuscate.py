# flake8: noqa
import tempfile
from pathlib import Path

import pytest
from PIL import Image

from app.obfuscate import ColourBox, validate_bounding_box


def test_obfuscate_colour_box_colour_string():
    # arrange
    # create a new blank image with all white pixels
    img = Image.new("RGB", (100, 100), (255, 255, 255))
    # obfuscate by setting pixels to black
    b = ColourBox("black")

    # act
    b.hide((25, 25, 75, 75), img)

    # assert
    all_pixels = list(img.getdata())
    white = 0
    black = 0
    for pixel in all_pixels:
        if pixel == (0, 0, 0):
            black += 1
        elif pixel == (255, 255, 255):
            white += 1
        else:
            raise Exception(
                f"obfuscated image contained pixel of unexpected colour: {pixel}"
            )

    assert img.size == (100, 100)
    assert black == 2500
    assert white == 7500


def test_obfuscate_colour_box_colour_tuple():
    # arrange
    # create a new blank image with all white pixels
    img = Image.new("RGB", (100, 100), (255, 255, 255))
    # obfuscate by setting pixels to black
    b = ColourBox((0, 0, 0))

    # act
    b.hide((25, 25, 75, 75), img)

    # assert
    all_pixels = list(img.getdata())
    white = 0
    black = 0
    for pixel in all_pixels:
        if pixel == (0, 0, 0):
            black += 1
        elif pixel == (255, 255, 255):
            white += 1
        else:
            raise Exception(
                f"obfuscated image contained pixel of unexpected colour: {pixel}"
            )

    assert img.size == (100, 100)
    assert black == 2500
    assert white == 7500


def test_obfuscate_colour_box_invalid_colour_string_raises_exception():
    with pytest.raises(ValueError):
        b = ColourBox("i am not a colour")


def test_obfuscate_colour_box_invalid_colour_tuple_raises_exception():
    cases = [
        (255, 255),  # too short
        (255, 255, 255, 255),  # too long
    ]
    for test_case in cases:
        with pytest.raises(ValueError):
            b = ColourBox(test_case)


def test_obfuscate_colour_box_same_colour_does_nothing():
    # arrange
    # create a new blank image with all white pixels
    img = Image.new("RGB", (100, 100), (255, 255, 255))
    # set to white
    b = ColourBox("white")

    # act
    b.hide((25, 25, 75, 75), img)

    # assert
    assert all([pixel == (255, 255, 255) for pixel in img.getdata()])


def test_obfuscate_validate_bounding_box():
    # arrange
    # create a new blank image with all white pixels
    img = Image.new("RGB", (100, 100), (255, 255, 255))
    cases = {
        (0, 0, 100, 100): True,
        (20, 20, 60, 60): True,
        (-1, 0, 100, 100): False,
        (0, -1, 100, 100): False,
        (0, 0, 101, 100): False,
        (0, 0, 100, 101): False,
        (20, 20, 10, 40): False,
        (20, 20, 40, 10): False,
    }
    # act & assert
    for bbox, want_valid in cases.items():
        assert validate_bounding_box(bbox, img) is want_valid
