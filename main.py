#sstv -d NASASEES.wav -o result.png'

import os
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
noiseList = []
currentNoiseLevel = 0


def sampleNoiseLevel():
    #Get Noise Level

    duration = 2 #in seconds

    def audio_callback(indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 20
        #print("|" * int(volume_norm))
        noiseList.insert(1, int(volume_norm))

    print("Ambient Noise Level Monitoring Start")

    stream = sd.InputStream(callback=audio_callback)
    with stream:
        sd.sleep(duration * 1000)

    print("Ambient Noise Level Monitoring Stop")

    #print(str(noiseList))

    noiseSum = sum(noiseList)
    noiseLen = len(noiseList)
    noiseAverage = noiseSum / noiseLen
    #print(str(noiseAverage))

    return noiseAverage

def monitorForIncrease(averageNoise):
    #Listen until a significant increase in noise level, then begin recording audio snippets.

    #currentNoiseLevel < (averageNoise + 5)

    duration = 1

    def audio_callback2(indata, frames, time, status):
        volume_norm2 = np.linalg.norm(indata) * 20
        #print("|" * int(volume_norm))
        currentNoiseLevel = volume_norm2
        print(str(currentNoiseLevel), "<", str(averageNoise))

    stream = sd.InputStream(callback=audio_callback2)

    with stream:
        sd.sleep(duration*1000)
    print("Free!")

def recordSegments():
    #36 Second Transmissions, 0.25 Second break in-between.
    #Currently: 1 SSTV Picture, 5 Color Pictures per Data Transmission.
    #Approximately a 3' 12" long transmission for current length.
    fs = 44100  # Sample rate
    seconds = (3*60) + 12 # Duration of recording
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write('RecordedAudio.wav', fs, myrecording)  # Save as WAV file 

def separateSegments():
    pass

def processSegments():
    #Convert .wav files to .png files.
    pass

#os.system('cmd /k "sstv -d NASASEES.wav -o result.png"')

ambientNoise = int(sampleNoiseLevel())
monitorForIncrease(ambientNoise)
#recordSegments()
#separateSegments()
#processSegments()