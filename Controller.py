import numpy as np
from Model import Audio
from View import View


class Controller:
    def __init__(self, model):
        self.model = model
        # Track the current frequency ranges (initially set to Low)
        self.current_range = "Low"
        self.frequency_ranges = {"Low": self.model.rt60_low, "Mid": self.model.rt60_mid, "High": self.model.rt60_high}
        self.color_dict = {"Low": 'green', "Mid": 'blue', "High": 'red'}

    def load_audio_file(self, filename):
        self.model.load_audio_file(filename)

    def get_duration(self):
        return self.model.duration

    def get_resonance(self):
        return self.model.calculate_resonance_freq()

    def get_rt60_diff(self):
        return self.model.rt60_difference()

    def switch_plot(self):
        # Switch between Low, Mid, High plots
        if self.current_range == "Low":
            self.current_range = "Mid"
        elif self.current_range == "Mid":
            self.current_range = "High"
        elif self.current_range == "High":
            self.current_range = "All"
        elif self.current_range == "All":
            self.current_range = "Wave"
        elif self.current_range == "Wave":
            self.current_range = "Orange"
        else:
            self.current_range = "Low"

    def get_current_band(self):
        return self.current_range

    def get_current_plot_data(self):
        self.frequency_ranges = {"Low": self.model.rt60_low, "Mid": self.model.rt60_mid, "High": self.model.rt60_high}
        # print(self.model.audio_data)
        # print(self.frequency_ranges[self.current_range])

        # return self.model.audio_data, self.frequency_ranges[self.current_range]

        if (self.current_range == "Orange"):
            return self.frequency_ranges["Mid"]

        time, data = self.frequency_ranges[self.current_range]
        return time, data, self.color_dict[self.current_range]

    def get_all_plot_data(self):
        self.frequency_ranges = {"Low": self.model.rt60_low, "Mid": self.model.rt60_mid, "High": self.model.rt60_high}
        return self.frequency_ranges, self.color_dict

    def get_wave_plot_data(self):
        time = np.linspace(0, self.model.duration, self.model.audio_data.shape[0])
        return time, self.model.audio_data

    def get_orange_plot_data(self):
        data_in_db = self.get_current_plot_data()
        return self.model.audio_data, self.model.sample_rate, data_in_db


if __name__ == "__main__":
    model = Audio()
    controller = Controller(model)
    view = View(controller)
    view.run()
