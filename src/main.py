import sys

import loadsave
from backend import TypingColors
from gui import Gui

if len(sys.argv) > 1:  # load file based on sys args
    typingColors = loadsave.load(sys.argv[-1])
else:  # create new canvas in backend if nonexist
    typingColors = TypingColors()
    typingColors.set_key('abc')


# run gui with canvas
gui = Gui(typingColors)
gui.run()
