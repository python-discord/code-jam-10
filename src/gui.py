import PySimpleGUI as sg

import backend as backend  # noqa: F401
import loadsave  # noqa: F401

# TODO
DEMO_PNG = ".\\assets\\demo.png"

WIN_W, WIN_H = (800, 600)


layout = [
    [
        sg.Column([
            [sg.Multiline(key="text", enable_events=True, size=(WIN_W // 2, WIN_H), font=('Consolas', 16))]
        ], element_justification='center', size=(WIN_W // 2, WIN_H),),
        sg.Column([
            [sg.Image(DEMO_PNG)]
        ], element_justification='center', size=(WIN_W // 2, WIN_H))
    ]
]


# Create the Window
window = sg.Window('Pixel Studio', layout, resizable=True, finalize=True, size=(WIN_W, WIN_H))

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        break

    print('You entered ', values['text'])

window.close()
