import pydub
import numpy as np
import winsound

sound_file = pydub.AudioSegment.from_wav("SSTV-Complete-Transmission.wav")
sound_file_Value = np.array(sound_file.get_array_of_samples())
# milliseconds in the sound track
# * 4.88
ranges = [(0,1805600),(1805600,3625800),(3625800,5394800),(5394800,7200400),(7200400,9006000)]

print(str(ranges))

for x, y in ranges:
    new_file=sound_file_Value[x : y]
    song = pydub.AudioSegment(new_file.tobytes(), frame_rate=sound_file.frame_rate,sample_width=sound_file.sample_width,channels=1)
    song.export("AMEA_Transmission_" + str(x) + "-" + str(y) +".wav", format="wav")