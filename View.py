import tkinter as tk
import numpy as np
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
        self.root.geometry('800x600')

        # GUI elements
        self.load_button = tk.Button(self.root, text="Load Audio File", command=self.load_file)
        self.load_button.pack()

        self.file_label = tk.Label(self.root, text="")
        self.file_label.pack()

        self.duration_label = tk.Label(self.root, text="")
        self.duration_label.pack()

        self.resonance_label = tk.Label(self.root, text="")
        self.resonance_label.pack()

        self.rt60_diff_label = tk.Label(self.root, text="")
        self.rt60_diff_label.pack()

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
            self.duration_label.config(text=f"Duration: {'{:.2f}'.format(self.controller.get_duration())} seconds")
            self.resonance_label.config(text=f"Resonance Frequency: {'{:.2f}'.format(self.controller.get_resonance())} "
                                             f"Hz")
            self.rt60_diff_label.config(text=f"RT60 Difference: {'{:.2f}'.format(self.controller.get_rt60_diff())} "
                                             f"seconds")
            # Plot initial waveform
            self.plot_waveform()

    def switch_plot(self):
        # Switch between Low, Mid, High plots
        self.controller.switch_plot()
        self.plot_waveform()

    def plot_waveform(self):
        # Plot waveform based on the current frequency band
        if (self.controller.get_current_band() == "All"):
            #print("Here")
            self.plot_all_waveform()
            return
        elif (self.controller.get_current_band() == "Wave"):
            self.plot_wave_waveform()
            return
        elif (self.controller.get_current_band() == "Orange"):
            self.plot_orange_waveform()
            return

        time, data, color = self.controller.get_current_plot_data()
        self.ax.clear()

        #self.ax.plot(frequency_band, rt60_values, label=f"RT60 for {self.controller.get_current_band()} band")

        self.ax.plot(time, data, label=f"RT60 for {self.controller.get_current_band()} band", color=color)

        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Power (dB)")
        self.ax.legend()

        #newPlot.show()

        #self.ax = newPlot
        self.canvas.draw()

    def plot_all_waveform(self):
        data_dict, color_dict = self.controller.get_all_plot_data()
        lowTime, lowData = data_dict["Low"]
        midTime, midData = data_dict["Mid"]
        highTime, highData = data_dict["High"]

        lowColor = color_dict["Low"]
        midColor = color_dict["Mid"]
        highColor = color_dict["High"]

        self.ax.clear()

        self.ax.plot(lowTime, lowData, label=f"RT60 for Low band", color=lowColor)
        self.ax.plot(midTime, midData, label=f"RT60 for Mid band", color=midColor)
        self.ax.plot(highTime, highData, label=f"RT60 for High band", color=highColor)

        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Power (dB)")
        self.ax.legend()
        self.canvas.draw()

    def plot_wave_waveform(self):
        time, wave_data = self.controller.get_wave_plot_data()

        self.ax.clear()

        self.ax.plot(time, wave_data, label=f"Waveform of the Audio", color='purple')

        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude (metres)")
        self.ax.legend()
        self.canvas.draw()

    def plot_orange_waveform(self):
        audio_data, sample_rate, data_in_db = self.controller.get_orange_plot_data()
        data_in_db = data_in_db[1]
        self.ax.clear()

        spectrum, freqs, t, im = plt.specgram(audio_data, Fs=sample_rate, NFFT=1024,
                                              cmap=plt.get_cmap('autumn_r'))

        index_of_max = np.argmax(data_in_db)
        value_of_max = data_in_db[index_of_max]
        plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')
        # slice array from a max value
        sliced_array = data_in_db[index_of_max:]
        value_of_max_less_5 = value_of_max - 5
        value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
        plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')
        # slice array from a max -5dB
        value_of_max_less_25 = value_of_max - 25
        value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
        index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
        plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Power (dB)")

        self.canvas.draw()
    def run(self):
        self.root.mainloop()

def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

