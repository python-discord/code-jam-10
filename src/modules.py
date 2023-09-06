import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle


class ImageLabel(tk.Label):
    """A Label that displays images, and plays them if they are gifs"""

    """
    :im: A PIL Image instance or a string filename
    """

    def load(self, im: str, repeat: bool = False, after_exec=None):
        """Loads an image"""
        self.im = im
        self.after_exec = after_exec
        if isinstance(im, str):
            im = Image.open(im)
        self.og_frames = []
        try:
            for i in count(1):
                self.og_frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(self.og_frames) if repeat else iter(self.og_frames)  # If img needs to be cycled
        try:
            self.delay = im.info['duration']
        except Exception:
            self.delay = 100
        if len(self.og_frames) == 1:  # If image is not a gif
            self.config(image=next(self.frames))
        else:  # If image is gif
            self.next_frame()

    def unload(self):
        """Unloads the iamge"""
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        """Updates the image frame (if gif)"""
        if self.frames:
            try:
                self.config(image=next(self.frames))
                self.after(self.delay, self.next_frame)
            except StopIteration:
                if self.after_exec:
                    self.after_exec()
