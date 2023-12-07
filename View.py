import tkinter as tk
from tkinter import filedialog as fd
from os import path
from Model import Audio
from Controller import Controller


class View:
    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()

        self.root.title('Project-Scientific Python Interactive Data Acoustic Modeling')
        self.root.resizable(False, False)
        self.root.geometry('300x150')

        # GUI elements
        self.load_button = tk.Button(self.root, text="Load Audio File", command=self.load_file)
        self.load_button.pack()

        self.file_label = tk.Label(self.root, text="")
        self.file_label.pack()

        self.duration_label = tk.Label(self.root, text="")
        self.duration_label.pack()

        # Add more GUI elements for other functionalities

    def load_file(self):
        file_path = fd.askopenfilename(filetypes=[("Audio files", "*.wav")])
        if file_path:
            self.controller.load_audio_file(file_path)
            self.file_label.config(text=f"File: {path.basename(file_path)}")
            self.duration_label.config(text=f"Duration: {self.controller.get_duration()} seconds")

    def run(self):
        self.root.mainloop()

