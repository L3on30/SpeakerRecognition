# from ast import Num
import sounddevice
from scipy.io.wavfile import write
from scipy.io import wavfile
import csv
import os.path
import noisereduce as nr
import constants as c
# import numpy as np
# import wave
# from test_noisereduce import audioprocess
from pathlib import Path
# import speech_recognition as sr
# from python_speech_features import fbank

# LENGTH = 43
# NUM_FBANKS = 232
# EXT = 'wav'

def user():
    print("Vui long dien ten va ma ID: ")
    global userName, userId, num_rec
    userName = input()
    userId = input()
    #num_rec = input()

# List_Enroll_Voice = "Enroll_Voice\enroll.csv"
def recordAudio():
    fs = 44800
    seconds = 5
    print("Bat dau")
    myrecording = sounddevice.rec(int(seconds*fs),samplerate = fs, channels=1)
    sounddevice.wait()
    print("Ket thuc")
    Path("DataVoice\{}".format(userName)).mkdir(parents=True, exist_ok=True)
    # file_exists = os.path.exists("DataVoice\{}\{}".format(userName, userId))
    # if file_exists==True:
    #     Num_rec+=1
    write("DataVoice\{}\{}.wav".format(userName, userId) ,fs, myrecording)
    # else:
    #     Num_rec = 1
    #     write("DataVoice\{}\{}-1.wav".format(userName, userId, Num_rec) ,fs, myrecording)

def audioprocess():
    # file_exists = os.path.exists("DataVoice\{}\{}-{}.wav".format(userName, userId, num_rec))
    # if file_exists:
    #     Num_rec+=1
    rate, data = wavfile.read("DataVoice\{}\{}.wav".format(userName, userId))
    # print(rate, data)
    # perform noise reduction
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    dir_path = r'DataVoice\{}'.format(userName)
    count = 1
# Iterate directory
    for path in os.listdir(dir_path):
    # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
        # print('File count:', count)
    wavfile.write("DataVoice\{}\{}-{}_process.wav".format(userName, userId, count), rate, reduced_noise)
    path = r"cfg\enroll_list.csv"
    # dir_path = r'DataVoice\Test'
    # # assert os.path.isfile(path)
    # for path in os.listdir(dir_path):
    #     # check if current path is a file
    #     if os.path.isfile(os.path.join(dir_path, path)):
    #         count += 1
    text = '{}'.format(userName)
    #print(text)
    header = "DataVoice\{}\{}-{}_process.wav".format(userName, userId, count)
    #header = ["DataVoice\{}\{}-{}_process.wav".format(userName, userId, count) + ',' + str(userName)]
    #header = ["DataVoice\{}\{}-{}_process.wav,{}".format(userName, userId, count, userName)]
    print(header)
    # header = head.join(seq)
    with open(path, mode = 'a+', encoding='UTF-8') as f:
        # header = "DataVoice\{}\{}.wav_process.wav".format(userName, userId)
        #os.remove("data\{}\{}.wav".format(userName, userId))
        # 
        writer = csv.writer(f, delimiter = ',')
        writer.writerow([header,text])
        f.close()

# user()
# recordAudio()
# audioprocess()
    # audio_detection()
