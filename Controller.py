from os import path
from pydub import AudioSegment
from pydub.playback import play
from Model import Audio
from View import View


class Controller:
    def __init__(self):
        self.model = model
        self.view = view

    def load_audio_file(self, filename):
        self.model.load_audio_file(filename)

    def get_duration(self):
        return self.model.duration


if __name__ == "__main__":
    model = Audio()
    view = View(model)
    controller = Controller(model, view)
    view.run()
