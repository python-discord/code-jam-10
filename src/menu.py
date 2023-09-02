from pathlib import Path

import PySimpleGUI as sg


def new_file(window: sg.Window):
    """Reset body and info bar, and clear filename variable

    Args:
        window (sg.Window): window instance to update
    """
    window["KEY-USER-INPUT"].update(value='')
    window["KEY-FILENAME"].update(value='> New File <')


# TODO: We need to keep the file opened !
def open_file(window: sg.Window):
    """Open file and update the filename

    Args:
        window (sg.Window): window instance to update

    Returns:
        file: path of file currently opened
    """
    filename = sg.popup_get_file('Open', no_window=True, keep_on_top=True)
    if filename:
        file = Path(filename)
        window["KEY-USER-INPUT"].update(value=file.read_text())
        window["KEY-FILENAME"].update(value=file.absolute())
        return file


def save_file(window: sg.Window, file: Path | None, content: str):
    """Save file instantly if already open; otherwise use `save-as` popup

    Args:
        window (sg.Window): window instance to update
        file (Path | None): path of file currently opened
        content (str): content to write to file
    """
    if file:
        file.write_text(content)
    else:
        save_file_as(window, content)


def save_file_as(window: sg.Window, content: str) -> Path:
    """Save new file or save existing file with another name

    Args:
        window (sg.Window): window instance to update
        content (str): content to write to file

    Returns:
        Path: path of file currently opened
    """
    filename = sg.popup_get_file('Save As', save_as=True, no_window=True)
    if filename:
        file = Path(filename)
        file.write_text(content)
        window["KEY-FILENAME"].update(value=file.absolute())
        return file
