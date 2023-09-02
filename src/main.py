"""Run File"""

import arcade
from Game import MainGame
from Utils import Constants

if __name__ == '__main__':
    window = arcade.Window(800, 600, Constants.title, resizable=True)
    window.show_view(MainGame.MainView())
    window.run()