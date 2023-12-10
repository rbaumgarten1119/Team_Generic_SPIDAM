from matplotlib import pyplot as plt
from scipy import fft
from os import path
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from scipy.io import wavfile
import numpy as np
# from scipy import signal
# from scipy.signal import find_peaks


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
        self.frequency_low_values = None
        self.frequency_mid_values = None
        self.frequency_high_values = None
        self.audioLength = None

    def load_audio_file(self, filename):
        self.filename = filename
        self.sample_rate, self.audio_data = wavfile.read(filename)
        self.duration = len(self.audio_data) / self.sample_rate
        self.calculate_rt60()
        self.getEntireFrequency()
        self.getLengthArray()

    def convert_to_wav(self):
        if self.filename.lower().endswith(".wav"):
            # Already a WAV file, no need to convert
            return

        try:
            audio = AudioSegment.from_file(self.filename)
            # Convert to WAV format
            wav_filename = path.splitext(self.filename)[0] + ".wav"
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

    def calculate_rt60(self):  # compute RT60 for low, mid, and high frequencies
        # Split the frequency range into low, mid, and high ranges (adjust as needed)
        low_cutoff = 250  # Adjust as needed
        high_cutoff = 5000  # Adjust as needed

        # Find the indices corresponding to the frequency ranges
        low_band_index = np.where((self.audio_data >= 0) & (self.audio_data < low_cutoff))[0]
        mid_band_index = np.where((self.audio_data >= low_cutoff) & (self.audio_data < high_cutoff))[0]
        high_band_index = np.where(self.audio_data >= high_cutoff)[0]

        # Calculate RT60 for each frequency range
        self.rt60_low = self._calculate_rt60_for_range(low_band_index)
        self.rt60_mid = self._calculate_rt60_for_range(mid_band_index)
        self.rt60_high = self._calculate_rt60_for_range(high_band_index)

    def _calculate_rt60_for_range(self, frequency_index):
        # DIFFERENT FROM POWERPOINT
        # # Calculate the energy envelope
        # energy_envelope = np.abs(np.imag(signal.hilbert(self.audio_data)))
        #
        # # Extract the energy envelope for the specified frequency range
        # fRange = energy_envelope[frequency_index]
        #
        # # Find the peaks in the envelope
        # peaks, _ = find_peaks(fRange)
        #
        # # Measure the time between the first and last peaks where the envelope exceeds a threshold (e.g., -60 dB)
        # threshold_db = -60
        # threshold_amplitude = 10 ** (threshold_db / 20)
        # envelope_thresholded = fRange > threshold_amplitude
        #
        # # Find the first and last indices where the envelope exceeds the threshold
        # first_peak = np.argmax(envelope_thresholded)
        # last_peak = len(envelope_thresholded) - np.argmax(envelope_thresholded[::-1])
        #
        # # Calculate the time between the first and last peaks
        # rt60 = (last_peak - first_peak) / self.sample_rate

        spectrum, freqs, t, im = plt.specgram(self.audio_data, Fs=self.sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))

        data_in_db = frequency_check()
        plt.figure()
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
        # optional set limits on plot
        # plt.xlim(0, ((round(abs(rt60), 2)) * 1.5))
        plt.grid()  # show grid
        plt.show()  # show plots
        print(f'The RT60 reverb time at freq {int(target_frequency)}Hz is {round(abs(rt60), 2)} seconds')

        return rt60


    # These two functions were to mainly test things, I imagine the "calculate_resonance_freq" function will have much more use than these.

    def getEntireFrequency(self):
        fft_result = fft.fft(self.audio_data)
        frequencies = fft.fftfreq(len(fft_result), 1.0 / self.sample_rate)

        self.frequency_low_values = frequencies

    def getLengthArray(self):
        self.audioLength = list(range(0, len(self.audio_data)))



# REFERENCES TO POWERPOINTS
# sample_rate, data = wavfile.read("16bitlchan.wav")
# spectrum, freqs, t, im = plt.specgram(audio_data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))

# pass
def find_target_frequency(freqs):
    for x in freqs:
        if x > 1000:
            break
    return x

def frequency_check(freqs, spectrum):
# you can choose a frequency which you want to check
    f'freqs {freqs[:10]}]'
    global target_frequency
    target_frequency = find_target_frequency(freqs)
    f'target_frequency {target_frequency}'
    index_of_frequency = np.where(freqs == target_frequency)[0][0]
    f'index_of_frequncy {index_of_frequency}'  # find a sound data for a particular frequency
    data_for_frequency = spectrum[index_of_frequency]
    f'data_for_frequency {data_for_frequency[:10]}'
    # change a digital signal for a values in decibels
    data_in_db_fun = 10 * np.log10(data_for_frequency)
    return data_in_db_fun

# data_in_db = frequency_check()
# plt.figure()
# # plot reverb time on grid
# plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
# plt.xlabel('Time (s)')
# plt.ylabel('Power (dB)')
# # find a index of a max value
# index_of_max = np.argmax(data_in_db)
# value_of_max = data_in_db[index_of_max]
# plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')
# # slice array from a max value
# sliced_array = data_in_db[index_of_max:]
# value_of_max_less_5 = value_of_max - 5

# value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
# index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
# plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')
# # slice array from a max -5dB
# value_of_max_less_25 = value_of_max - 25
# value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
# index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
# plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')
# rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
# # extrapolate rt20 to rt60
# rt60 = 3 * rt20
# # optional set limits on plot
# # plt.xlim(0, ((round(abs(rt60), 2)) * 1.5))
# plt.grid()  # show grid
# plt.show()  # show plots
# print(f'The RT60 reverb time is {round(abs(rt60), 2)} seconds')

data_in_db = frequency_check()
plt.figure(2)

# find nearest value of less 5db
def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

# value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
# index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
# plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')
# # slice array from a max-5dB
# value_of_max_less_25 = value_of_max - 25
# value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
# index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
# plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')
# rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
# # print (f'rt20= {rt20}')
# rt60 = 3 * rt20
# # plt.xlim(0, ((round(abs(rt60), 2)) * 1.5))
# plt.grid()
# plt.show()
# print(f'The RT60 reverb time at freq {int(target_frequency)}Hz is {round(abs(rt60), 2)} seconds')
