import PySimpleGUI as sg

import backend as backend  # noqa: F401
import loadsave  # noqa: F401

# create gui, somehow take in loaded object with init function
# or start with blank canvas by default

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('Some text on Row 1')],
          [sg.Text('Enter something on Row 2'), sg.InputText()],
          [sg.Text('Enter something on Row 2'), sg.InputText()],
          [sg.Button('Ok'), sg.Button('Cancel')]]


# Create the Window
window = sg.Window('Window Title', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    print('You entered ', values)

window.close()
