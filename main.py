#sstv -d NASASEES.wav -o result.png'

import os
import sounddevice as sd
from scipy.io.wavfile import write
import pydub
import numpy as np
import time
from pydub import AudioSegment
from pydub.silence import split_on_silence
import datetime
from datetime import date
from datetime import datetime
noiseList = []
currentNoiseLevel = 0
today = date.today()
now = datetime.now()
now = now.hour


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
    pass

def recordSegments():
    #36 Second Transmissions, 0.25 Second break in-between.
    #Currently: 1 SSTV Picture, 5 Color Pictures per Data Transmission.
    #Approximately a 3' 12" long transmission for current length.
    fs = 44100  # Sample rate
    seconds = (4*60)
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write('DataDemo3.wav', fs, myrecording)  # Save as WAV file 

def separateSegments():
    song = AudioSegment.from_mp3("DataDemo3.wav")

    # Split track where the silence is 2 seconds or more and get chunks using 
    # the imported function.
    chunks = split_on_silence (
    # Use the loaded audio.
    song, 
    # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
    min_silence_len = 250,
    # Consider a chunk silent if it's quieter than -16 dBFS.
    # (You may want to adjust this parameter.)
    silence_thresh = -50
    )

    # Process each chunk with your parameters
    for i, chunk in enumerate(chunks):
        # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
        silence_chunk = AudioSegment.silent(duration=500)

        # Add the padding chunk to beginning and end of the entire chunk.
        audio_chunk = chunk

        # Normalize the entire chunk.
        #normalized_chunk = match_target_amplitude(audio_chunk, -10.0)

        # Export the audio chunk with new bitrate.
        print("Exporting AMEA_Transmission{0}.wav.".format(i))
        audio_chunk.export(
        ".//AMEA_Transmission_{0}.wav".format(i),
        bitrate = "192k",
        format = "wav"
        ) 


def processSegments():
    os.system("sstv -d AMEA_Transmission_0.wav -o AMEA_Data_Result_SSTV_Picture_"+str(today)+"_Hour-"+str(now)+".png")
    os.system("sstv -d AMEA_Transmission_1.wav -o AMEA_Data_1_Digit_1_"+str(today)+"_Hour-"+str(now)+".png")
    os.system("sstv -d AMEA_Transmission_2.wav -o AMEA_Data_1_Digit_2_"+str(today)+"_Hour-"+str(now)+".png")
    os.system("sstv -d AMEA_Transmission_3.wav -o AMEA_Data_1_Digit_3_"+str(today)+"_Hour-"+str(now)+".png")
    os.system("sstv -d AMEA_Transmission_4.wav -o AMEA_Data_1_Digit_4_"+str(today)+"_Hour-"+str(now)+".png")
    os.system("sstv -d AMEA_Transmission_5.wav -o AMEA_Data_1_Digit_5_"+str(today)+"_Hour-"+str(now)+".png")

#ambientNoise = int(sampleNoiseLevel())
#monitorForIncrease(ambientNoise)
#recordSegments()
separateSegments()
processSegments()