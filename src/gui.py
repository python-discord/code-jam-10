import time

import PySimpleGUI as sg

import backend as backend  # noqa: F401
import loadsave  # noqa: F401

# TODO
DEMO_PNG = ".\\assets\\demo.png"

WIN_W, WIN_H = (800, 600)

# To delay invoking image updation when the user is continuously typing
last_time = 0
interval = 0.6
UPDATE_FLAG = False

layout = [
    [
        sg.Column([
            [sg.Multiline(key="-USER-INPUT-", enable_events=True, size=(30, WIN_H // (25)), font=('Consolas', 16))]
        ], element_justification='center', size=(WIN_W // 2, WIN_H),),
        sg.VSeperator(),
        sg.Column([
            [sg.Image(DEMO_PNG, key="-OUT-IMG-")]
        ], element_justification='center', size=(WIN_W // 2, WIN_H))
    ]
]


typingColors = backend.TypingColors()

# Create the Window
window = sg.Window('Pixel Studio', layout, resizable=True, finalize=True, margins=(0, 0), size=(WIN_W, WIN_H))

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read(timeout=500)
    if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        break

    if event == '__TIMEOUT__':
        if UPDATE_FLAG:
            UPDATE_FLAG = False
            typingColors.update(values['-USER-INPUT-'])
            img_data = typingColors.img_scaled()
            window["-OUT-IMG-"].update(data=img_data)

    if (values['-USER-INPUT-']):
        if time.time() - last_time < interval:
            # Dont Update the Image if the user is continuously typing
            UPDATE_FLAG = True
        else:
            typingColors.update(values['-USER-INPUT-'])
            img_data = typingColors.img_scaled()
            window["-OUT-IMG-"].update(data=img_data)

        last_time = time.time()


window.close()
