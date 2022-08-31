import json
from pathlib import Path

from tkinter import Tk, Y, RIGHT, LEFT
from tkinter.ttk import Frame, Label, Button, Scrollbar
from tkinter.filedialog import askopenfile
from PIL.ImageTk import PhotoImage
from PIL import Image, ImageOps


DEFAULT_FRAME_PADDING = 5


class Card:
    CARD_SIZE = (168, 234)

    def __init__(self, parent, path):
        self._image = Image.open(path, 'r')
        self._thumbnail = ImageOps.contain(self._image, self.CARD_SIZE)
        self._image_adapter = PhotoImage(self._thumbnail)
        self._elem = Label(parent, image=self._image_adapter)


class CardsContainer:
    def __init__(self, parent, files):
        self._outer_frame = parent
        self._inner_frame = Frame(self._outer_frame)
        self._inner_frame.pack(side=LEFT, fill=Y)

        Card(self._inner_frame, files[0]['path'])

        self._scrollbar = Scrollbar(self._outer_frame, orient='horizontal')
        self._scrollbar.pack(side=RIGHT, fill=Y)


if __name__ == '__main__':
    root = Tk()

    frame = Frame(root, padding=DEFAULT_FRAME_PADDING)
    frame.grid()

    settings = None

    def handle_open_settings():
        global settings

        with askopenfile() as file:
            settings = json.load(file)

        for card in settings['files']:
            card['path'] = Path(settings['dir']) / card['file_name']

        # CardsContainer(bottom_panel, settings['files'])
        Card(bottom_panel, settings['files'][0]['path'])


    button_panel = Frame(frame, padding=DEFAULT_FRAME_PADDING)
    button_panel.grid(column=1, row=0)
    display_panel = Frame(frame, padding=DEFAULT_FRAME_PADDING, width=800, height=600)
    display_panel.grid(column=0, row=0)
    bottom_panel = Frame(frame, padding=DEFAULT_FRAME_PADDING)


    Button(button_panel, text="Open Settings", command=handle_open_settings).grid(column=0, row=1)

    root.mainloop()
