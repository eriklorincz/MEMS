import pyaudio
import numpy as np
import os

#the code below is from the pyAudio library documentation
chunk=4096
RATE=44100

#change default audio output device to HDMI
os.system("amixer -c 0 cset numid=3 2")

p=pyaudio.PyAudio()

#input stream setup
stream=p.open(format = pyaudio.paInt16,rate=RATE,channels=1, input_device_index = 2, input=True, frames_per_buffer=chunk)

#output stream setup
player=p.open(format = pyaudio.paInt16,rate=RATE,channels=1, output=True, frames_per_buffer=chunk)
#player2=p2.open(format = pyaudio.paInt16,rate=RATE,channels=1, output=True, frames_per_buffer=chunk)

while True:            #Used to continuously stream audio
     data=np.fromstring(stream.read(chunk,exception_on_overflow = False),dtype=np.int16)
     player.write(data,chunk)
     
     
stream.stop_stream()
stream.close()
p.terminate