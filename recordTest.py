# from ast import Num
import sounddevice
from scipy.io.wavfile import write
from scipy.io import wavfile
import csv
import os.path
import noisereduce as nr
from pathlib import Path
# import speech_recognition as sr
# from python_speech_features import fbank

def recordAudio():
    fs = 44100
    seconds = 5
    print("Bat dau")
    myrecording = sounddevice.rec(int(seconds*fs),samplerate = fs, channels=1)
    sounddevice.wait()
    print("Ket thuc")
    Path("DataVoice\Test").mkdir(parents=True, exist_ok=True)
    write("DataVoice\check.wav", fs, myrecording)

def audioprocess():
    rate, data = wavfile.read("DataVoice\check.wav")
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wavfile.write("DataVoice\Test\check_process.wav", rate, reduced_noise)
    path = r"csv\test_list.csv"
    header = ["DataVoice\Test\check_process.wav"]
    fn = "filename"
    sk = "speaker"                  
    print(header)
    with open(path, mode = 'w+', newline='', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow([fn,sk])
        writer.writerow(header)
        f.close()

    # audio_detection()
