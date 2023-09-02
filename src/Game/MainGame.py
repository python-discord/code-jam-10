"""
Menu.

Shows the usage of almost every gui widget, switching views and making a modal.
"""
import arcade
import arcade.gui as gui
from PIL import Image
import numpy as np


class MainView(arcade.View):
    """This is the class where your normal game would go."""

    def __init__(self):
        super().__init__()
        self.manager = gui.UIManager()
        # TODO: Add actual functionality



    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Enable the UIManager when the view is shown.
        self.manager.enable()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Draw the manager.
        self.manager.draw()






