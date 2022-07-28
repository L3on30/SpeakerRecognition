from generateVoice import user, recordAudio, audioprocess
import numpy as np
import constants as c
import pandas as pd
# import os.path
from model import vggvox_model
from wav_reader import get_fft_spectrum


def build_buckets(max_sec, step_sec, frame_step):
    buckets = {}
    frames_per_sec = int(1/frame_step)
    end_frame = int(max_sec*frames_per_sec)
    step_frame = int(step_sec*frames_per_sec)
    for i in range(0, end_frame+1, step_frame):
        s = i
        s = np.floor((s-7+2)/2) + 1  # conv1
        s = np.floor((s-3)/2) + 1  # mpool1
        s = np.floor((s-5+2)/2) + 1  # conv2
        s = np.floor((s-3)/2) + 1  # mpool2
        s = np.floor((s-3+2)/1) + 1  # conv3
        s = np.floor((s-3+2)/1) + 1  # conv4
        s = np.floor((s-3+2)/1) + 1  # conv5
        s = np.floor((s-3)/2) + 1  # mpool5
        s = np.floor((s-1)/1) + 1  # fc6
        if s > 0:
            buckets[i] = int(s)
    return buckets

def get_embeddings_from_list_file(model, list_file, max_sec):
    buckets = build_buckets(max_sec, c.BUCKET_STEP, c.FRAME_STEP)
    result = pd.read_csv(list_file, delimiter=",")
    result['features'] = result['filename'].apply(
        lambda x: get_fft_spectrum(x, buckets))
    result['embedding'] = result['features'].apply(
        lambda x: np.squeeze(model.predict(x.reshape(1, *x.shape, 1))))
    return result[['filename', 'speaker', 'embedding']]

def loading():
    print("Loading model weights from [{}]....".format(c.WEIGHTS_FILE))
    model = vggvox_model()
    model.load_weights(c.WEIGHTS_FILE)
    # model.summary()
    print("Processing enroll samples....")
    enroll_result = get_embeddings_from_list_file(
        model, c.ENROLL_LIST_FILE, c.MAX_SEC)
    enroll_embs = np.array([emb.tolist() for emb in enroll_result['embedding']])
    speakers = enroll_result['speaker']
    # for i in range(len(speakers)):
    #     np.save(os.path.join(c.EMBED_LIST_FILE,str(speakers[i]) +".npy"), enroll_embs[i])
    #     print("Succesfully enrolled the user")
    # print(enroll_embs)
    # print(speakers)
    return model, enroll_embs, speakers


if __name__ == '__main__':
    user()
    recordAudio()
    audioprocess()
    loading()
