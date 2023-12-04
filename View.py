from tkinter import Tk, Label, Button
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from Model import Audio
from os import path
from pydub import AudioSegment
from pydub.playback import play


gfile = ''
root = Tk()

root.title('Project-Scientific Python Interactive Data Acoustic Modeling')
root.resizable(False, False)
root.geometry('300x150')
def select_file():
    filetypes = (
        ('wave files', '*.wav'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    gfile = filename

    # tkinter.messagebox — Tkinter message prompts
    showinfo(
        title='Selected File',
        message=filename
    )

    gfile_label = ttk.Label(root, text=gfile)
    gfile_label.pack(side="bottom")


# open button
open_button = ttk.Button(
    root,
    text='Load audio file',
    command=select_file
)

open_button.pack(expand=True)


# run the application
root.mainloop()
