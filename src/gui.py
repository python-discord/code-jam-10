import time

import PySimpleGUI as sg

import backend as backend  # noqa: F401
import loadsave  # noqa: F401
from menu import new_file, open_file, save_file, save_file_as

WIN_W, WIN_H = (800, 600)
POP_W, POP_H = (400, 300)


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
        self.main_window = self.create_main_window()
        # self.popup_window = self.create_decrypt_encrypt_window()
        # self.main_window.hide()

        self.ask_key()

    def ask_key(self):
        # TODO: What to do when the user changes the key when we already has some output on the left
        # coz the previously set color pixels wont change rn
        """Asks For encryption key from the user"""
        key = sg.popup_get_text('Enter encryption key', title="Enter Key")
        self.typingColors.set_encryption(key)

    # function to create the place to write text to create image

    def create_main_window(self):
        """Creates Window for the application"""
        menu_layout = [
            ['File', ['New', 'Open', 'Save', 'Save As', '---', 'Exit']],
            ['Config', ['Set Key']],
            ['Options', ['Import', 'Export']]
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
        # transition_page = [
        #     [sg.Sizer(WIN_W / 2, 0)],
        #     [sg.Button('Encrypt/Decrypt', key='KEY-TRANSITION')]
        # ]
        layout = [
            [sg.Menu(menu_layout)],
            [
                sg.Column(left_side, element_justification='center', size=(WIN_W // 2, WIN_H // 2)),
                sg.VSeperator(),
                sg.Column(right_side, element_justification='center', size=(WIN_W // 2, WIN_H))
            ],
            # [
            #     sg.Column(transition_page, element_justification='center', size=(WIN_W // 2, WIN_H))
            # ],
            # TODO Show word count and size of image here...
            [sg.StatusBar("Hello World !")]
        ]

        return sg.Window('Pixel Studio',
                         layout,
                         resizable=True,
                         finalize=True,
                         size=(WIN_W, WIN_H),
                         return_keyboard_events=True)

    def create_decrypt_encrypt_window(self):
        """Function to create a window to input encryption key"""
        menu_layout = [
            ['File', ['New', 'Open', 'Save', 'Save As', '---', 'Exit']]
        ]

        encryption_button = [
            [sg.Sizer(POP_W / 2, 0)],
            [sg.Button('Encrypt', key='KEY-ENCRYPT-BUTTON')]
        ]
        decryption_button = [
            [sg.Sizer(POP_W / 2, 0)],
            [sg.Button('Decrypt', key='KEY-DECRYPT-BUTTON')]
        ]

        encryption_decryption = [
            [sg.Sizer(POP_W, 0)],
            [sg.Text('Encryption Key', font=('Consolas', 10))],
            [sg.InputText(
                key="KEY-ENCRYPTION-INPUT",
                enable_events=True,
                size=(15, POP_H // 25),
                font=('Consolas', 16),
                expand_x=True,
                expand_y=True
            )]
        ]

        layout2 = [
            [sg.Menu(menu_layout)],
            [sg.Column(encryption_decryption, element_justification='center', size=(POP_W, POP_H // 3))],
            [
                sg.Column(encryption_button, element_justification='center', size=(POP_W // 2, POP_H // 3)),
                sg.Column(decryption_button, element_justification='center', size=(POP_W // 2, POP_H // 3))
            ],
        ]

        return sg.Window('Pixel Studio2',
                         layout2,
                         resizable=True,
                         finalize=True,
                         size=(POP_W, POP_H),
                         return_keyboard_events=True)

    def update_img(self, value):
        """Updates Generated Image

        Args:
            value (str): user input
        """
        self.typingColors.update(value)
        img_data = self.typingColors.img_scaled()
        self.main_window["KEY-OUT-IMG"].update(data=img_data)

    def run(self):
        """Application Event loop"""
        # while True:
        #     event, value = self.popup_window.read(timeout=100)
        #     if event in (sg.WIN_CLOSED, 'Exit'):  # if user closes window or clicks cancel
        #         self.main_window.close()
        #         break
        #     elif event == "KEY-ENCRYPT-BUTTON":
        #         self.typingColors.set_key(value['KEY-ENCRYPTION-INPUT'])
        #         self.popup_window.hide()
        #         self.main_window.un_hide()
        #         break
        #     elif event == "KEY-DECRYPT-BUTTON":
        #         self.typingColors.set_key(value['KEY-ENCRYPTION-INPUT'])
        #         self.popup_window.hide()
        #         self.main_window.un_hide()
        #         break

        """Main loop to process events"""
        while True:
            event, values = self.main_window(timeout=100)
            if event in (sg.WIN_CLOSED, 'Exit'):  # if user closes window or clicks cancel
                break

            user_input = values['KEY-USER-INPUT']

            if event == '__TIMEOUT__':
                if self.UPDATE_FLAG:
                    self.UPDATE_FLAG = False
                    self.update_img(user_input)
                continue

            elif event == "KEY-USER-INPUT":
                if time.time() - self.last_time < self.interval:
                    # Dont Update the Image if the user is continuously typing
                    self.UPDATE_FLAG = True
                else:
                    self.update_img(user_input)

                self.last_time = time.time()

            elif event == "KEY-TRANSITION":
                self.popup_window.un_hide()
                self.main_window.hide()

            # Menu Events
            # '$letter:$code' are used to implement `ctrl + $letter` shortcuts

            # 'File' submenu events
            if event in ('New', 'n:78'):
                self.file = None
                new_file(self.main_window)
                self.UPDATE_FLAG = True
            elif event in ('Open', 'o:79'):
                self.file = open_file(self.main_window)
                self.UPDATE_FLAG = True
            elif event in ('Save', 's:83'):
                save_file(self.main_window, self.file, user_input)
            elif event == 'Save As':
                self.file = save_file_as(self.main_window, user_input)

            # 'Config' submenu events==
            elif event == 'Set Key':
                self.ask_key()

            elif event == 'Import':
                # load png in backend
                filename = sg.popup_get_file('Open', no_window=True, keep_on_top=True)
                self.typingColors = loadsave.load(filename, self.typingColors.key)
                # load text and image in gui
                decoded_text = self.typingColors.text
                self.main_window['KEY-USER-INPUT'].update(value=decoded_text)
                self.update_img(decoded_text)
            elif event == 'Export':
                filename = sg.popup_get_file('Save As', save_as=True, no_window=True)
                loadsave.save(self.typingColors, filename)

        self.main_window.close()
