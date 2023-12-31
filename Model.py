from matplotlib import pyplot as plt
from scipy import fft
from os import path
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from scipy.io import wavfile
import numpy as np


class Audio:
    def __init__(self):
        self.filename = None
        self.sample_rate = None
        self.audio_data = None
        self.duration = None
        self.resonance_freq = None
        self.rt60_low = None
        self.rt60_mid = None
        self.rt60_high = None
        self.rt60_low_val = None
        self.rt60_mid_val = None
        self.rt60_high_val = None
        self.audioLength = None

    def load_audio_file(self, filename):
        self.convert_to_wav(filename)
        self.duration = len(self.audio_data) / self.sample_rate
        self.calculate_rt60()
        self.getEntireFrequency()
        self.getLengthArray()

    def convert_to_wav(self, filename):
        if filename.lower().endswith(".wav"):
            # Already a WAV file, no need to convert
            self.filename = filename
            self.sample_rate, self.audio_data = wavfile.read(filename)
            return

        try:
            audio = AudioSegment.from_file(filename)
            # Convert to WAV format
            wav_filename = path.splitext(filename)[0] + ".wav"
            audio.export(wav_filename, format="wav")
            self.filename = wav_filename
            self.sample_rate, self.audio_data = wavfile.read(wav_filename)
        except CouldntDecodeError as e:
            print(f"Error converting to WAV: {e}")

    def remove_meta_multichannel(self):  # handle meta data or multi-channel
        # Check if the audio has metadata
        if len(self.audio_data.shape) > 1 and self.audio_data.shape[1] > 1:
            # If multichannel, take the mean across channels to convert to mono
            self.audio_data = np.mean(self.audio_data, axis=1)

    def calculate_resonance_freq(self):  # compute and set the resonance frequency
        # find dominant frequency
        fft_result = fft.fft(self.audio_data)
        frequencies = fft.fftfreq(len(fft_result), 1.0 / self.sample_rate)

        # prevent negative frequencies
        positive_frequencies = frequencies[frequencies >= 0]
        positive_fft = fft_result[:len(positive_frequencies)]

        # locate index of maximum amplitude
        max_amplitude_index = np.argmax(np.abs(positive_fft))

        # define index as corresponding frequency
        self.resonance_freq = positive_frequencies[max_amplitude_index]

        return self.resonance_freq

    def calculate_rt60(self):  # compute RT60 for low, mid, and high frequencies
        # Split the frequency range into low, mid, and high ranges (adjust as needed)
        low_cutoff = 250  # Adjust as needed
        high_cutoff = 5000  # Adjust as needed

        # Find the indices corresponding to the frequency ranges
        low_band_index = [60000, 250000]
        mid_band_index = [0, 1000]
        high_band_index = [5000, 10000]

        # Calculate RT60 for each frequency range
        self.rt60_low = self._calculate_rt60_for_range(low_band_index)
        self.rt60_mid = self._calculate_rt60_for_range(mid_band_index)
        self.rt60_high = self._calculate_rt60_for_range(high_band_index)

    def _calculate_rt60_for_range(self, frequency_index):
        spectrum, freqs, t, im = plt.specgram(self.audio_data, Fs=self.sample_rate, NFFT=1024,
                                              cmap=plt.get_cmap('autumn_r'))

        data_in_db = frequency_check(freqs, spectrum, frequency_index)

        # plot reverb time on grid
        plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (dB)')

        # find a index of a max value
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
        rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
        # extrapolate rt20 to rt60
        rt60 = 3 * rt20

        # if (frequency_index[0] == 60000):
        #     plt.savefig('currentLowFreqPlot.png')
        # elif (frequency_index[0]== 0):
        #     plt.savefig('currentMidFreqPlot.png')
        # elif (frequency_index[0] == 5000):
        #     plt.savefig('currentHighFreqPlot.png')

        # optional set limits on plot
        # plt.xlim(0, ((round(abs(rt60), 2)) * 1.5))

        print(f'The RT60 reverb time at freq {int(target_frequency)}Hz is {round(abs(int(rt60)), 2)} seconds')

        if frequency_index == [60000, 250000]:
            self.rt60_low_val = rt60
        if frequency_index == [0, 1000]:
            self.rt60_mid_val = rt60
        if frequency_index == [5000, 10000]:
            self.rt60_high_val = rt60

        return t, data_in_db

    def rt60_difference(self):
        rt60_avg = (self.rt60_low_val + self.rt60_mid_val + self.rt60_high_val) / 3
        rt60_diff = abs(0.5 - rt60_avg)
        return rt60_diff

    def getEntireFrequency(self):
        fft_result = fft.fft(self.audio_data)
        frequencies = fft.fftfreq(len(fft_result), 1.0 / self.sample_rate)

        self.frequency_low_values = frequencies

    def getLengthArray(self):
        self.audioLength = list(range(0, len(self.audio_data)))

    # def __del__(self):
    #     os.remove('currentLowFreqPlot.png')
    #     os.remove('currentMidFreqPlot.png')
    #     os.remove('currentHighFreqPlot.png')


# REFERENCES TO POWERPOINTS
# spectrum, freqs, t, im = plt.specgram(audio_data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))

def find_target_frequency(freqs, target):
    global x
    for x in freqs:
        if (x > target[0]) and (x < target[1]):
            break
    return x


def frequency_check(freqs, spectrum, target_frequency_type):
    # you can choose a frequency which you want to check
    f'freqs {freqs[:10]}]'
    global target_frequency
    target_frequency = find_target_frequency(freqs, target_frequency_type)
    f'target_frequency {target_frequency}'
    index_of_frequency = np.where(freqs == target_frequency)[0][0]
    f'index_of_frequncy {index_of_frequency}'  # find a sound data for a particular frequency
    data_for_frequency = spectrum[index_of_frequency]
    f'data_for_frequency {data_for_frequency[:10]}'
    # change a digital signal for a values in decibels
    data_in_db_fun = 10 * np.log10(data_for_frequency)
    return data_in_db_fun


# find nearest value of less 5db
def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]
