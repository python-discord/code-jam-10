import unittest

from PIL import Image
from pixelate_and_swap import pixelate_and_group_colors_sampled, swap_colors


class TestPixelate(unittest.TestCase):
    """Test cases for pixelate_and_swap.py"""

    def test_pixelate_and_group_colors_sampled(self) -> None:
        """
        Test that the number of colors in an image after pixelation is less than the number of colors before pixelation

        :return: None
        """
        image = Image.open("dahlias.jpg")
        # Count the number of colors in the image before pixelation
        colors_before = len(set(image.getdata()))
        # Pixelate and group colors
        pixelated = pixelate_and_group_colors_sampled(image, 8)
        # Count the number of colors in the image after pixelation
        colors_after = len(set(pixelated.getdata()))
        # Assert that the number of colors after pixelation is less than the number of colors before pixelation
        self.assertLess(colors_after, colors_before)
        print(f"Number of colors before pixelation: {colors_before}")
        print(f"Number of colors after pixelation: {colors_after}")
        assert colors_before > colors_after
        assert colors_before != colors_after

    def test_swap_colors(self) -> None:
        """
        Test that the number of white pixels after swapping is equal to the number of black pixels before swapping

        :return: None
        """
        # Create a test image
        test_image = Image.new("RGB", (100, 100), "white")
        # Count the number of white and black pixels in the image
        white_pixels_before_swap = 0
        black_pixels_before_swap = 0
        for pixel in test_image.getdata():
            if pixel == (255, 255, 255):
                white_pixels_before_swap += 1
            elif pixel == (0, 0, 0):
                black_pixels_before_swap += 1

        # Swap white and black colors
        swapped = swap_colors(test_image, (255, 255, 255), (0, 0, 0))
        # Count the number of white and black pixels in the image
        white_pixels_after_swap = 0
        black_pixels_after_swap = 0
        for pixel in swapped.getdata():
            if pixel == (255, 255, 255):
                white_pixels_after_swap += 1
            elif pixel == (0, 0, 0):
                black_pixels_after_swap += 1
        # Assert that the number of white pixels after swapping is equal to the number of black pixels before swapping
        self.assertEqual(white_pixels_after_swap, black_pixels_before_swap)
        # Assert that the number of black pixels after swapping is equal to the number of white pixels before swapping
        self.assertEqual(black_pixels_after_swap, white_pixels_before_swap)
        print(f"Number of white pixels before swapping: {white_pixels_before_swap}")
        print(f"Number of black pixels before swapping: {black_pixels_before_swap}")
        print(f"Number of white pixels after swapping: {white_pixels_after_swap}")
        print(f"Number of black pixels after swapping: {black_pixels_after_swap}")
        # Assert that there are no other colors in the image
        for pixel in swapped.getdata():
            self.assertIn(pixel, [(255, 255, 255), (0, 0, 0)])
