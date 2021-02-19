import socket
import pyaudio
import time
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 40
EXPLODE_THRESH = 300
NEAR_THRESH = 23
NOISE_THRESH = 100

stream = None

def init_sound() :
    global stream
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=2)

prevsound = 0
def findexplode(dam) :
    global prevsound
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    data = np.reshape(data, (2,-1), order='F')

    ff1 = abs(np.fft.fft(data[0]) / len(data[0]))
    ff2 = abs(np.fft.fft(data[1]) / len(data[1]))

    maxf1 = ff1.argmax()
    maxf2 = ff2.argmax()
    locf1 = ff1[100:512].argmax()
    locf2 = ff2[100:512].argmax()
    if (dam>0 and\
        locf1>130 and locf1<150 and ff1[locf1+100]>NEAR_THRESH) or\
         (locf2>130 and locf2<150 and ff2[locf2+100]>NEAR_THRESH) :
        if(prevsound<max(locf1, locf2) ) :
            # print("near explode", max(locf1, locf2)) 
            return 1
        prevsound = max(locf1, locf2)+2
    else :
        prevsound = 0

    # print(ff1[maxf1],ff2[maxf2] )
    if (ff1[0]>EXPLODE_THRESH) or (ff2[0]>EXPLODE_THRESH) :
        # nowsound = round(max(ff1[0], ff2[0]),2)
        # print("far explode", nowsound)
        return 1
    elif (ff1[maxf1]>NOISE_THRESH) or (ff2[maxf2]>NOISE_THRESH) :
        return 2

    return 0
t = 0
soundv = 0
def getthresh() :
    global t, soundv
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    data = np.reshape(data, (2,-1), order='F')

    ff1 = abs(np.fft.fft(data[0]) / len(data[0]))
    ff2 = abs(np.fft.fft(data[1]) / len(data[1]))
    
    max1 = ff1.max()
    max2 = ff2.max()
    
    t+=2
    soundv += max1
    soundv += max2

def makethresh() :
    global NEAR_THRESH,EXPLODE_THRESH,NOISE_THRESH
    avg = round(soundv/t)
    EXPLODE_THRESH = avg*15
    NOISE_THRESH = avg*3
    NEAR_THRESH = avg/2
    print(EXPLODE_THRESH,NOISE_THRESH, NEAR_THRESH)

# init_sound()
# while(True) :
#     findexplode(1)
#     # time.sleep(0.1)