"""
Menu Window
"""

import arcade
import arcade.gui
from src.Utils import Constants


class Quit(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
        arcade.exit()


class MenuWindow(arcade.Window):
    def __init__(self) -> None:
        super().__init__(800, 600, Constants.title, resizable=True)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.WHITE)  # Place Holder
        self.v_box = arcade.gui.UIBoxLayout()

        # Start Button
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        # Settings Button
        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        # Quit Button
        quit_button = Quit(text="Quit", width=200)
        self.v_box.add(quit_button)

        start_button.on_click = self.on_click_start
        settings_button.on_click = self.on_click_setting

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_start(self, event: arcade.gui.UIOnClickEvent) -> None:
        # TODO: Add functionality
        print("Start:", event)

    def on_click_setting(self, event: arcade.gui.UIOnClickEvent) -> None:
        # TODO: Add functionality
        print("Start:", event)

    def on_draw(self) -> None:
        self.clear()
        self.manager.draw()
