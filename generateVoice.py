import sounddevice
from scipy.io.wavfile import write
from scipy.io import wavfile
import csv
import os.path
import noisereduce as nr
import constants as c
from pathlib import Path
# import speech_recognition as sr
# from python_speech_features import fbank

def user():
    '''
    Get the name of the staff member and ID for new data files
    '''
    print("Vui long nhap ten va ma ID cong ty: ")
    global userName, userId
    userName = input()
    userId = input()

def recordAudio():
    '''
    This function is to set up for the audio
    By default, the recorded array has the data type 'float32'
    channels: means the number of device audio channels, 1 is kind of mono sound, 2 is kind of stereo sound
    For more details, you can search from here: https://python-sounddevice.readthedocs.io/en/0.3.7/#sounddevice.query_devices
    '''
    fs = 44100 # or 48000, record at 44100 samples per second
    seconds = 5
    print("Bat dau")
    myrecording = sounddevice.rec(int(seconds*fs),samplerate = fs, channels=1)
    sounddevice.wait()
    print("Ket thuc")
    Path("DataVoice\{}".format(userName)).mkdir(parents=True, exist_ok=True)
    write("DataVoice\{}\{}.wav".format(userName, userId) ,fs, myrecording)
    
def audioprocess():
    '''
    In this function, I access to the audio file above and use the library 'noisereduce' to reduce the noise around
    Arguments to reduce_noise: https://github.com/timsainb/noisereduce
    '''
    rate, data = wavfile.read("DataVoice\{}\{}.wav".format(userName, userId))
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    os.remove("DataVoice\{}\{}.wav".format(userName, userId))
    dir_path = r'DataVoice\{}'.format(userName)
    count = 1
    
    for path in os.listdir(dir_path):
    # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
        # print('File count:', count)
    wavfile.write("DataVoice\{}\{}-{}_process.wav".format(userName, userId, count), rate, reduced_noise)
    path = r"csv\enroll_list.csv"
    text = '{}'.format(userName)
    
    header = "DataVoice\{}\{}-{}_process.wav".format(userName, userId, count)
    
    print(header)
    with open(path, mode = 'a+', encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter = ',')
        writer.writerow([header,text])
        f.close()

# user()
# recordAudio()
# audioprocess()
    # audio_detection()
