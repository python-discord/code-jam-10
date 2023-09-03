import time

import PySimpleGUI as sg

import backend as backend  # noqa: F401
import loadsave  # noqa: F401
from menu import new_file, open_file, save_file, save_file_as

WIN_W, WIN_H = (800, 600)

menu_layout = [
    ['File', ['New', 'Open', 'Save', 'Save As', '---', 'Exit']]
]

left_side = [
    [sg.Sizer(WIN_W / 2, 0)],
    [sg.Text('> New file <', font=('Consolas', 10), key='KEY-FILENAME')],
    [sg.Multiline(
        key="KEY-USER-INPUT",
        enable_events=True,
        size=(15, WIN_H // 25),
        font=('Consolas', 16),
        rstrip=False,
        expand_x=True,
        expand_y=True
    )]
]

right_side = [
    [sg.Sizer(WIN_W / 2, 0)],
    [sg.Image(key="KEY-OUT-IMG")],
]

layout = [
    [sg.Menu(menu_layout)],
    [
        sg.Column(left_side, element_justification='center', size=(WIN_W // 2, WIN_H)),
        sg.VSeperator(),
        sg.Column(right_side, element_justification='center', size=(WIN_W // 2, WIN_H))
    ],
    # TODO Show word count and size of image here...
    [sg.StatusBar("Hello World !")]
]


class Gui:
    """Main GUI class to interact with the backend"""

    def __init__(self, typingColors):
        """Initializes variables and window"""
        # stores the backend class
        self.typingColors = typingColors

        # To delay invoking image updation when the user is continuously typing
        self.last_time = 0
        self.interval = 0.6
        self.UPDATE_FLAG = False

        self.file = None  # Opened files

        # Creates the window
        self.window = sg.Window('Pixel Studio',
                                layout,
                                resizable=True,
                                finalize=True,
                                size=(WIN_W, WIN_H),
                                return_keyboard_events=True)

    def update_img(self, value):
        """Updates Generated Image

        Args:
            value (str): user input
        """
        self.typingColors.update(value)
        img_data = self.typingColors.img_scaled()
        self.window["KEY-OUT-IMG"].update(data=img_data)

    def run(self):
        """Main loop to process events"""
        while True:
            event, values = self.window.read(timeout=100)
            if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
                break

            user_input = values['KEY-USER-INPUT']

            if event == '__TIMEOUT__':
                if self.UPDATE_FLAG:
                    self.UPDATE_FLAG = False
                    self.update_img(user_input)
                continue

            if event == "KEY-USER-INPUT":
                if time.time() - self.last_time < self.interval:
                    # Dont Update the Image if the user is continuously typing
                    self.UPDATE_FLAG = True
                else:
                    self.update_img(user_input)

                self.last_time = time.time()

            # Menu Events
            # '$letter:$code' are used to implement `ctrl + $letter` shortcuts

            if event in ('New', 'n:78'):
                self.file = None
                new_file(self.window)
                self.UPDATE_FLAG = True
            elif event in ('Open', 'o:79'):
                self.file = open_file(self.window)
                self.UPDATE_FLAG = True
            elif event in ('Save', 's:83'):
                save_file(self.window, self.file, user_input)
            elif event in ('Save As',):
                self.file = save_file_as(self.window, user_input)

        self.window.close()

# Testing
# if __name__ == "__main__":
#     gui = Gui(backend.TypingColors())
#     gui.run()
