from pyaudio import paInt16

# Signal processing
SAMPLE_RATE = 16000
PREEMPHASIS_ALPHA = 0.97
FRAME_LEN = 0.025
FRAME_STEP = 0.01
NUM_FFT = 512
BUCKET_STEP = 1
MAX_SEC = 10

# Model
WEIGHTS_FILE = "Model/weights.h5"
COST_METRIC = "cosine"  # euclidean or cosine
COST_METRIC2 = "euclidean" # euclidean
INPUT_SHAPE=(NUM_FFT,None,1)
EMBED_LIST_FILE = "embed"

# IO
ENROLL_LIST_FILE = "csv/enroll_list.csv"
TEST_LIST_FILE = "csv/test_list.csv"
RESULT_FILE = "res/results_test.csv"
#RESULT_FILE = "res/results.csv"
