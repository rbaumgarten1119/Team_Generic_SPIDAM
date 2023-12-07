import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import fft
from os import path
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from pydub.playback import play
from scipy.io import wavfile
import numpy as np

sample_rate, data = wavfile.read("16bitlchan.wav")
spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))


class Audio:
    def __int__(self):
        self.filename = None
        self.sample_rate = None
        self.audio_data = None
        self.duration = None
        self.resonance_freq = None
        self.rt60_low = None
        self.rt60_mid = None
        self.rt60_high = None

    def load_audio_file(self, filename):
        self.filename = filename
        self.sample_rate, self.audio_data = wavfile.read(filename)
        self.duration = len(self.audio_data) / self.sample_rate

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
        find_target_frequency(freqs)
        # find an index of a max value
        data_in_db = frequency_check()
        index_of_max = np.argmax(data_in_db)
        value_of_max = data_in_db[index_of_max]
        sliced_array = data_in_db[index_of_max:]
        value_of_max_less_5 = value_of_max - 5
        value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
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
        print(f'The RT60 reverb time is {round(abs(rt60), 2)} seconds')


# REFERENCES TO POWERPOINTS
# # sample_rate, data = wavfile.read("16bitlchan.wav")
# # spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
#
# # prints var outputs
def debug(fstring):
    print(fstring)  # comment out for prod


#
#
# # pass
def find_target_frequency(freqs):
    for x in freqs:
        if x > 1000:
            break
    return x


#
#
def frequency_check():
    # you can choose a frequency which you want to check
    debug(f'freqs {freqs[:10]}]')
    target_frequency = find_target_frequency(freqs)
    debug(f'target_frequency {target_frequency}')
    index_of_frequency = np.where(freqs == target_frequency)[0][0]
    debug(f'index_of_frequncy {index_of_frequency}')  # find a sound data for a particular frequency
    data_for_frequency = spectrum[index_of_frequency]
    debug(f'data_for_frequency {data_for_frequency[:10]}')
    # change a digital signal for a values in decibels
    data_in_db_fun = 10 * np.log10(data_for_frequency)
    return data_in_db_fun


#
#
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
#
#
# # find a nearest value
def find_nearest_value(array, value):
    array = np.asarray(array)

    debug(f'array {array[:10]}')
    idx = (np.abs(array - value)).argmin()
    debug(f'idx {idx}')
    debug(f'array[idx] {array[idx]}')
    return array[idx]
#
#
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
#
#
# data_in_db = frequency_check()
# plt.figure(2)
# plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
# plt.xlabel('Time (s)')
# plt.ylabel('Power (dB)')
# # find an index of a max value
# index_of_max = np.argmax(data_in_db)
# value_of_max = data_in_db[index_of_max]
# plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')
# # slice our array from a max value
# sliced_array = data_in_db[index_of_max:]
# value_of_max_less_5 = value_of_max - 5
#
#
# # find a nearest value of less 5db
# def find_nearest_value(array, value):
#     array = np.asarray(array)
#     idx = (np.abs(array - value)).argmin()
#     return array[idx]
#
#
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
