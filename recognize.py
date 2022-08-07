from scoring import get_id_result
from recordTest import audioprocess, recordAudio
from Load_model import loading


global model
global enroll_embs
global speakers
model, enroll_embs, speakers = loading()

recordAudio()
audioprocess()
get_id_result(model, enroll_embs, speakers)
