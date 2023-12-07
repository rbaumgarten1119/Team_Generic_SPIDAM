from fastapi import FastAPI
from os import path
from pydub import AudioSegment
from pydub.playback import play
# from Model import Audio



app = FastAPI


class Controller:
    def __init__(self):

    def convert_audio(raw_audio):
        # files
        src = "pt.mp3"
        dst = "pt.wav"
        # convert wav to mp3
        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format="wav")
        raw_audio == AudioSegment.from_file("pt.wav", format="wav")
        channel_count = raw_audio.channels
        print(channel_count)
        mono_wav = raw_audio.set_channels(1)
        mono_wav.export("pt_mono.wav", format="wav")
        mono_wav_audio = AudioSegment.from_file("pt_mono.wav", format="wav")
        channel_count = mono_wav_audio.channels
        print(channel_count)



@app.get("/audio")
async def get_audio():
    return
