#sstv -d NASASEES.wav -o result.png'

import os
import sounddevice as sd
from scipy.io.wavfile import write
import pydub
import numpy as np
noiseList = []
currentNoiseLevel = 0


def sampleNoiseLevel():
    #Get Noise Level

    duration = 5 #in seconds

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
    sound_file = pydub.AudioSegment.from_wav("SSTV-Complete-Transmission.wav")
    sound_file_Value = np.array(sound_file.get_array_of_samples())
    # milliseconds in the sound track
    # * 4.88
    ranges = [(0,2005600),(2005600,3825800),(3825800,5694800),(5694800,7500400),(7500400,9306000)]

    #print(str(ranges))

    for x, y in ranges:
        new_file=sound_file_Value[x : y]
        song = pydub.AudioSegment(new_file.tobytes(), frame_rate=sound_file.frame_rate,sample_width=sound_file.sample_width,channels=1)
        song.export("AMEA_Transmission_" + str(x) + "-" + str(y) +".wav", format="wav")

def processSegments():
    os.system('''cmd /k "sstv -d AMEA_Transmission_0-1805600.wav -o AMEA_Data_Result_0-1805600.png"''')

#os.system('cmd /k "sstv -d NASASEES.wav -o result.png"')

#ambientNoise = int(sampleNoiseLevel())
#monitorForIncrease(ambientNoise)
#recordSegments()
separateSegments()
processSegments()