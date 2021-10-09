import numpy as np
import sounddevice as sd
import queue as bf

fifo_out = bf.Queue()
fifo_in = bf.Queue()

def callback( indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = fifo_out.get()
    fifo_in.put(indata.copy())

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





