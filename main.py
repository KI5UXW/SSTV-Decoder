#sstv -d NASASEES.wav -o result.png'

import os
import sounddevice as sd
from scipy.io.wavfile import write

def sampleNoiseLevel():
    #Get Noise Level
    pass

def monitorForIncrease():
    #Listen until a significant increase in noise level, then begin recording audio snippets.
    pass

def recordSegments():
    #36 Second Transmissions, 0.25 Second break in-between.
    #Currently: 1 SSTV Picture, 5 Color Pictures per Data Transmission.
    #Approximately a 3' 12" long transmission for current length.
    fs = 44100  # Sample rate
    seconds = (3*60) + 12 # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write('RecordedAudio.wav', fs, myrecording)  # Save as WAV file 

def separateSegments()

def processSegments():
    #Convert .wav files to .png files.
    pass

#os.system('cmd /k "sstv -d NASASEES.wav -o result.png"')

sampleNoiseLevel()
monitorForIncrease()
recordSegments()
separateSegments()
processSegments()