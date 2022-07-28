from Load_model import get_embeddings_from_list_file, loading
from recordTest import audioprocess, recordAudio
import os
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist, euclidean, cosine
# from glob import glob
from model import vggvox_model
# from wav_reader import get_fft_spectrum
import constants as c


def get_id_result(model, enroll_embs, speakers):
    # if os.path.exists(c.EMBED_LIST_FILE):
    #     embeds = os.listdir(c.EMBED_LIST_FILE)
    # if len(embeds) is 0:
    #     print("No enrolled users found")
    #     exit()
    # print("Loading model weights from [{}]....".format(c.WEIGHTS_FILE))
    # model = vggvox_model()
    # model.load_weights(c.WEIGHTS_FILE)
    # model.summary()

    # print("Processing enroll samples....")
    # enroll_result = get_embeddings_from_list_file(
    #     model, c.ENROLL_LIST_FILE, c.MAX_SEC)
    # enroll_embs = np.array([emb.tolist()
    #                        for emb in enroll_result['embedding']])
    # speakers = enroll_result['speaker']
    # model, enroll_embs, speakers = loading()
    print("Processing test samples....")
    test_result = get_embeddings_from_list_file(model, c.TEST_LIST_FILE, c.MAX_SEC)
    test_embs = np.array([emb.tolist() for emb in test_result['embedding']])

    print("Comparing test samples against enroll samples....")
    distances = pd.DataFrame(
        cdist(test_embs, enroll_embs, metric=c.COST_METRIC), columns=speakers) # cosine metric
    #distances2 = pd.DataFrame(
    #     cdist(test_embs, enroll_embs, metric=c.COST_METRIC2), columns=speakers) # Euclidean metric
    scores = pd.read_csv(c.TEST_LIST_FILE, delimiter=",", header=1, names=['test_file', 'test_speaker'])
    # scores2 = pd.read_csv(c.TEST_LIST_FILE, delimiter=",", header=0, names=['test_file', 'test_speaker'])
    scores = pd.concat([scores, distances], axis=1)
    # scores2 = pd.concat([scores, distances2], axis=1)
    scores['result'] = scores[speakers].idxmin(axis=1)
    # scores2['result'] = scores2[speakers].idxmin(axis=1)
    # if scores['result'] == scores2['result']:
    scores['correct'] = (scores['result'] == scores['test_speaker'])*1.  # bool to int

    print("Writing outputs to [{}]....".format(c.RESULT_FILE))
    print(scores['result'])
    # else:
    #     print("Please say again")
    #     exit()
    result_dir = os.path.dirname(c.RESULT_FILE)
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    with open(c.RESULT_FILE, 'w') as f:
        scores['result'].to_csv(f, index=False)
    return scores['result']


if __name__ == '__main__':
    recordAudio()
    audioprocess()
    get_id_result()
