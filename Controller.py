# from os import path
# from pydub import AudioSegment
# from pydub.playback import play
from Model import Audio
from View import View


class Controller:
    def __init__(self, model):
        self.model = model
        # Track the current frequency ranges (initially set to Low)
        self.current_range = "Low"
        self.frequency_ranges = {"Low": self.model.rt60_low, "Mid": self.model.rt60_mid, "High": self.model.rt60_high}

    def load_audio_file(self, filename):
        self.model.load_audio_file(filename)

    def get_duration(self):
        return self.model.duration

    def switch_plot(self):
        # Switch between Low, Mid, High plots
        if self.current_range == "Low":
            self.current_range = "Mid"
        elif self.current_range == "Mid":
            self.current_range = "High"
        else:
            self.current_range = "Low"

    def get_current_band(self):
        return self.current_range

    def get_current_plot_data(self):
        self.frequency_ranges = {"Low": self.model.rt60_low, "Mid": self.model.rt60_mid, "High": self.model.rt60_high}

        # print(self.model.audio_data)
        # print(self.frequency_ranges[self.current_range])

        # return self.model.audio_data, self.frequency_ranges[self.current_range]

        return self.model.frequency_low_values, self.model.audio_data

if __name__ == "__main__":
    model = Audio()
    controller = Controller(model)
    view = View(controller)
    view.run()
