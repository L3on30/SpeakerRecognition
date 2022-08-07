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
    '''
    Get embedding result for test audio, then compare with the enroll_embs
    COS_METRIC is cosine
    The score which has smallest deviation with the test_embs is the speaker
    '''
    # model, enroll_embs, speakers = loading()
    print("Processing test samples....")
    test_result = get_embeddings_from_list_file(model, c.TEST_LIST_FILE, c.MAX_SEC)
    test_embs = np.array([emb.tolist() for emb in test_result['embedding']])

    print("Comparing test samples against enroll samples....")
    distances = pd.DataFrame(
        cdist(test_embs, enroll_embs, metric=c.COST_METRIC), columns=speakers) # cosine metric
    #distances2 = pd.DataFrame(
    #     cdist(test_embs, enroll_embs, metric=c.COST_METRIC2), columns=speakers) # Euclidean metric
    scores = pd.read_csv(c.TEST_LIST_FILE, delimiter=",", header=1, names=['filename', 'speakers'])
    # scores2 = pd.read_csv(c.TEST_LIST_FILE, delimiter=",", header=0, names=['test_file', 'test_speaker'])
    scores = pd.concat([scores, distances], axis=1)
    # scores2 = pd.concat([scores, distances2], axis=1)
    scores['result'] = scores[speakers].idxmin(axis=1)
    # scores2['result'] = scores2[speakers].idxmin(axis=1)
    # if scores['result'] == scores2['result']:
    scores['correct'] = (scores['result'] == scores['speakers'])*1.  # bool to int

    print("Writing outputs to [{}]....".format(c.RESULT_FILE))
    
    result_dir = os.path.dirname(c.RESULT_FILE)
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    with open(c.RESULT_FILE, 'w') as f:
        scores['result'].to_csv(f, index=False)
   
    return scores['result']


# if __name__ == '__main__':
#     # recordAudio()
#     audioprocess()
#     get_id_result()
