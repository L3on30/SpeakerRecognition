# SpeakerRecognition

## Project for AI Voice Recognition
Imagine you have a secret room with a smart door, smart door has a microphone for user to speak to. The record will be processed and if you are permiited to access this secret room, the door will be opened. This project need your data before being trained. You can say a sentence as a input data. After being trained, when you test the system you can say even another sentence with different content. Bammn it still can recognize you as a valid speaker.
## vggvox

* Python adaptation of VGGVox speaker identification model, based on Nagrani et al 2017, "[VoxCeleb: a large-scale speaker identification dataset](https://arxiv.org/pdf/1706.08612.pdf)"
* Evaluation code only, based on the author's [Matlab code](https://github.com/a-nagrani/VGGVox/)
and [pretrained model](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system. You also can run on Flask API to set up it on server

### Prerequisites

```
Flask==2.1.2
Keras==2.4.3
Keras-Preprocessing==1.1.2
keras-layer-normalization==0.16.0
pandas==1.3.5
sounddevice==0.4.4
scipy==1.7.3
numpy==1.19.5
librosa

```
### Installing

#### Install NVIDA CUDA Toolkit for tensorflow
```
https://developer.nvidia.com/cuda-downloads
```

## Usage for API
### Enroll new data
```
python EnrollVoice.py 
```
Or
```
You can call API '/', it will return a website for recording new data with you username and ID is necessary. Then you download it and write 
its address in "csv\enroll_list.csv" with form "address,username"
```
### Recognize 
```
API '/api/Speaker-Recognition'
#### Input
This API requires json input with the parameter name is "voice", paremeter value is a base64 encoded .wav, we can use POSTMAN to test
For example:
{
    "voice": "abcsadfadfadsfsadfqwerqe"
}
#### Output
{
    "name": "alkdjflkajsdlfkajs"
}
```
### 

## Authors

* **Nghia Tran** - *Initial work* - [L3on30](https://github.com/L3on30)
## Contributors
* **Nghia Tran** - *Initial work* - [L3on30](https://github.com/L3on30)
* **Dat Ngo** - *Initial work* - [kaitoud906](https://github.com/kaitoud906)
