import numpy as np
import sounddevice as sd
import queue as bf
import Signal as sg
from math import ceil
import matplotlib.pyplot as plt
from Data_Ploting import *

class SoundCard:
    def __init__(self):
        self.Fs = 48000

        self.SCIn = 0
        self.SCOut = 0

    def setFs(self, Fs):
        self.Fs = Fs

    def SCChoice(self):
        print('Choisir la carte son à utiliser :')
        print(sd.query_devices())
        self.SCIn = int(input('SC entrée ?'))
        self.SCOut = int(input('SC Sortie ?'))

    def mesure(self, out):
        fifo_out.put(out)
        sd.Stream(device=(self.SCIn, self.SCOut), samplerate=self.Fs, blocksize=1024, callback=callback)
        return fifo_in.get()


if __name__ == "__main__":
    HPChirp = Data_Ploting(path='impulseresponse1.wav')

    blocksize = 1024

    fifo = bf.Queue()
    fifo_in = bf.Queue()

    for i in range(ceil(HPChirp.sig[0].N/blocksize)):
        data = HPChirp.sig[0].x[i*blocksize:i*blocksize+blocksize]
        fifo.put_nowait(data)

    def callback(indata, outdata, frames, time, status):
        try:
            data = fifo.get_nowait()
        except bf.Empty as e:
            raise sd.CallbackAbort from e
        if len(data) < len(outdata):
            outdata[:len(data)] = np.expand_dims(data, axis=1)
            outdata[len(data):].fill(0)
            raise sd.CallbackStop
        else:
            outdata[:] = np.expand_dims(data, axis=1)
        fifo_in.put(indata.copy())

    with sd.Stream(device=(1,3), channels=1, callback=callback, blocksize=blocksize, samplerate=44100):
        print('#' * 80)
        print('press Return to quit')
        print('#' * 80)
        input()

    sig = sg.Signal([fifo_in.get() for _ in range(fifo_in.qsize())], 44100)

    plt.figure()
    plt.plot(sig.x)
    plt.show()
    plt.tight_layout()

