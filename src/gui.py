import time

import PySimpleGUI as sg

import backend as backend  # noqa: F401
import loadsave  # noqa: F401
from menu import new_file, open_file, save_file, save_file_as

WIN_W, WIN_H = (800, 600)

# To delay invoking image updation when the user is continuously typing
last_time = 0
interval = 0.6
UPDATE_FLAG = False

# Opened Files
file = None

menu_layout = [
    ['File', ['New', 'Open', 'Save', 'Save As', '---', 'Exit']]
]

layout = [
    [sg.Menu(menu_layout)],
    [
        sg.Column([
            [sg.Text('> New file <', font=('Consolas', 10), size=(WIN_W, 1), key='KEY-FILENAME')],
            [sg.Multiline(key="KEY-USER-INPUT", enable_events=True, size=(30, WIN_H // (25)), font=('Consolas', 16))]
        ], element_justification='center', size=(WIN_W // 2, WIN_H),),
        sg.VSeperator(),
        sg.Column([
            [sg.Image(key="KEY-OUT-IMG")]
        ], element_justification='center', size=(WIN_W // 2, WIN_H))
    ]
]


typingColors = backend.TypingColors()

# Create the Window
window = sg.Window('Pixel Studio',
                   layout,
                   resizable=True,
                   finalize=True,
                   margins=(0, 0),
                   size=(WIN_W, WIN_H),
                   return_keyboard_events=True)

window["KEY-USER-INPUT"].expand(True, True, True)


def update_img(value):
    """Updates Generated Image

    Args:
        value (str): user input
    """
    typingColors.update(value)
    img_data = typingColors.img_scaled()
    window["KEY-OUT-IMG"].update(data=img_data)


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        break

    user_input = values['KEY-USER-INPUT']

    if event == '__TIMEOUT__':
        if UPDATE_FLAG:
            UPDATE_FLAG = False
            update_img(user_input)
        continue

    if event == "KEY-USER-INPUT":
        if time.time() - last_time < interval:
            # Dont Update the Image if the user is continuously typing
            UPDATE_FLAG = True
        else:
            update_img(user_input)

        last_time = time.time()

    # Menu Events
    # '$letter:$code' are used to implement `ctrl + $letter` shortcuts

    if event in ('New', 'n:78'):
        file = None
        new_file(window, file)
        update_img(user_input)
    if event in ('Open', 'o:79'):
        file = open_file(window)
        update_img(user_input)
    if event in ('Save', 's:83'):
        save_file(window, file, user_input)
    if event in ('Save As',):
        file = save_file_as(window, user_input)


window.close()
