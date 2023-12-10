import tkinter as tk
from tkinter import filedialog as fd
from os import path
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class View:
    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()

        self.root.title('Project-Scientific Python Interactive Data Acoustic Modeling')
        self.root.resizable(False, False)
        self.root.geometry('500x500')

        # GUI elements
        self.load_button = tk.Button(self.root, text="Load Audio File", command=self.load_file)
        self.load_button.pack()

        self.file_label = tk.Label(self.root, text="")
        self.file_label.pack()

        self.duration_label = tk.Label(self.root, text="")
        self.duration_label.pack()

        # Button to switch between Low, Mid, High plots
        self.switch_button = tk.Button(self.root, text="Switch Plot", command=self.switch_plot)
        self.switch_button.pack()

        # Matplotlib Figure and Canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack()

    def load_file(self):
        file_path = fd.askopenfilename(filetypes=[("Audio files", "")])
        if file_path:
            print(file_path)
            self.controller.load_audio_file(file_path)
            self.file_label.config(text=f"File: {path.basename(file_path)}")
            self.duration_label.config(text=f"Duration: {self.controller.get_duration()} seconds")
            # Plot initial waveform
            self.plot_waveform()

    def switch_plot(self):
        # Switch between Low, Mid, High plots
        self.controller.switch_plot()
        self.plot_waveform()

    def plot_waveform(self):
        # Plot waveform based on the current frequency band
        frequency_band, rt60_values = self.controller.get_current_plot_data()
        self.ax.clear()
        self.ax.plot(frequency_band, rt60_values, label=f"RT60 for {self.controller.get_current_band()} band")
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Amplitude(dB) ?")
        self.ax.legend()
        self.canvas.draw()

    def run(self):
        self.root.mainloop()

