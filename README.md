Project-Scientific Python Interactive Data Acoustic Modeling

This project is for the use of breaking down audio files to measure the reverberation and varying frequencies over time.

In this repository, there are three different classes: a Model class, a Controller class, and a View class. The Model class holds the information related to the raw audio data and its processing. This processed information is then passed through the Controller class, which handles the GUI and commands for View class. The View class then displays data and graphs for audio file being read.
The sample audio provided in both .mp3 and .wav format was used for testing the program, and it was recorded with a microphone from the Florida Polytechnic University SIM Lab. The audio file is an edited recording of a clap from a distance of 3 meters (measured with a meterstick).

The graphs were differentiated into 5 different visuals: Low RT60, Medium RT60, High RT60, Waveform, and Spectrogram. The Waveform graph was just the shape of the audio wave in terms of frequency (Hz) and amplitude (m). The RT60 variants were based on ranged frequencies from Low to High, with the center (Medium RT60) being situated at frequency 1000 Hz. The Spectrogram is made for viewing the sound wave in a more unique way.

GUI attributes of this program include a button to upload an audio file for reading, this audio file is converted to wave format automatically if it is not already. Another GUI attribute is a switch graph button which allows the user to cycle through all the different graphs to see each one individually as well as a view of all the RT60 graphs combined.