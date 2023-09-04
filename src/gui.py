import time

import PySimpleGUI as sg

import backend as backend  # noqa: F401
import loadsave  # noqa: F401
from menu import new_file, open_file, save_file, save_file_as

WIN_W, WIN_H = (800, 600)



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
        self.window = self.create_window1()
        self.window2 = self.create_decrypt_encrypt()
        self.window.hide()
    
    # function to create the place to write text to create image
    
    def create_window1(self):
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
        transition_page = [
            [sg.Sizer(WIN_W / 2, 0)],
            [sg.Button('Encrypt/Decrypt', key='TRANSITION')]
            ]
        layout = [
            [sg.Menu(menu_layout)],
            [
            sg.Column(left_side, element_justification='center', size=(WIN_W // 2, WIN_H //2)),
            sg.VSeperator(),
            sg.Column(right_side, element_justification='center', size=(WIN_W // 2, WIN_H))
            ],
            [
            sg.Column(transition_page, element_justification='center', size=(WIN_W // 2, WIN_H))
            ],
            # TODO Show word count and size of image here...
            [sg.StatusBar("Hello World !")]
            ]
        return sg.Window('Pixel Studio', 
                         layout, 
                         resizable=True, 
                         finalize=True, 
                         size = (WIN_W, WIN_H), 
                         return_keyboard_events=True)
    # function to create a window to input encryption key  
    def create_decrypt_encrypt(self):
        menu_layout = [
            ['File', ['New', 'Open', 'Save', 'Save As', '---', 'Exit']]
        ]

        encryption_button = [
            [sg.Sizer(WIN_W / 2, 0)],
            [sg.Button('Encrypt', key='ENCRYPT_BUTTON')]
        ]
        decryption_button = [
            [sg.Sizer(WIN_W / 2, 0)],
            [sg.Button('Decrypt', key = 'DECRYPT_BUTTON')]
        ]

        encryption_decryption = [
            [sg.Sizer(WIN_W, 0)],
            [sg.Text('Encryption Key', font=('Consolas', 10), key='ENCRYPT')],
            [sg.InputText(
                key="ENCRYPTION-KEY",
                enable_events=True,
                size=(15, WIN_H // 25),
                font=('Consolas', 16),
                expand_x=True,
                expand_y=True
            )]
        ]

        layout2 = [
        [sg.Menu(menu_layout)],
        [sg.Column(encryption_decryption, element_justification='center', size=(WIN_W, WIN_H // 3))],
        [
            sg.Column(encryption_button, element_justification='center', size=(WIN_W //2, WIN_H // 3)),
            sg.Column(decryption_button, element_justification='center', size=(WIN_W //2, WIN_H // 3))
        ], 
        [sg.StatusBar("Hello World !")]
    ]
        return sg.Window('Pixel Studio2',
                                    layout2,
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
        while True:
            event2, value2 = self.window2.read(timeout=100)
            if event2 in (sg.WIN_CLOSED, 'Exit'):  # if user closes window or clicks cancel
                self.window.close()
                break
            if event2 == "ENCRYPT_BUTTON":
                self.typingColors.set_encryption(value2['ENCRYPTION-KEY'])
                self.window2.close()
                self.window.un_hide()
                break
            if event2 == "DECRYPT_BUTTON":
                self.typingColors.set_encryption(value2['ENCRYPTION-KEY'])
                self.window2.close()
                self.window.un_hide()
                break


        """Main loop to process events"""
        while True:
            event, values = self.window(timeout=100)
            if event in (sg.WIN_CLOSED, 'Exit'):  # if user closes window or clicks cancel
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
            if event == "TRANSITION":
                self.window2.un_hide()
                self.window.hide()
            
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
