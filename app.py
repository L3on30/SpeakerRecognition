from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from xmlrpc.client import Fault
from flask import Flask, render_template, redirect
from flask import request
from flask import config
from flask import render_template_string
from flask import Flask, session
from itsdangerous import base64_decode
from Load_model import build_buckets, get_embeddings_from_list_file, loading
from recordTest import recordAudio, audioprocess
from scoring import get_id_result
from pyaudio import paInt16
import base64
from codecs import encode 
import json


app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['wav'])

def allowed_file(filename):
    	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

global model
global enroll_embs
global speakers
model, enroll_embs, speakers = loading()
# Signal processing
SAMPLE_RATE = 16000
PREEMPHASIS_ALPHA = 0.97
FRAME_LEN = 0.025
FRAME_STEP = 0.01
NUM_FFT = 512
BUCKET_STEP = 1
MAX_SEC = 10

# Model
WEIGHTS_FILE = "data/model/weights.h5"
COST_METRIC = "cosine"  # euclidean or cosine
COST_METRIC2 = "euclidean" # euclidean
INPUT_SHAPE=(NUM_FFT,None,1)
EMBED_LIST_FILE = "embed"

# IO
ENROLL_LIST_FILE = "cfg/enroll_list.csv"
TEST_LIST_FILE = "cfg/test_list.csv"
RESULT_FILE = "res/results_test.csv"


@app.route('/', methods = ['GET', 'POST'])
def index():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
    return render_template('index.html')

@app.route('/api/takeData', methods = ['GET', 'POST'])
def takeData():
    data = request.get_json()
    voice = data.get('voice', None)
    a = encode(voice, "utf-8")
    #enc = base64.b64encode(open("audio.wav", "rb").read())
    b = base64.decodebytes(a)
    # with open('original_audio.txt',mode='wb+') as f:
    #     f.write(voice)
    with open('data.wav', mode = 'wb+') as f:
        f.write(b)
    return "Nhan data thanh cong"


@app.route('/api/train', methods = ['GET'])
def trainData():
    global model, enroll_embs, speakers
    model, enroll_embs, speakers = loading()
    return "Train data thanh cong"

    


@app.route('/api/Speaker-Recognition', methods = ['POST'])
def speakerRecognition():
    try:
        data = request.get_json()
        voice = data.get("voice",None)
        a = encode(voice, "utf-8")
        b = base64.decodebytes(a)
        with open('DataVoice/check.wav', mode = 'wb+') as f:
            f.write(b)
        audioprocess()
        global model, enroll_embs, speakers
        t = get_id_result(model, enroll_embs, speakers)
        print(str(t[0]))
        return {"name": str(t[0])}, 200
    except Exception as e:
        print(e)
        return "Failed"
    
        

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)