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
        self.compLat = False

    def setFs(self, Fs):
        self.Fs = Fs
        sd.default.samplerate = Fs
        return self

    def SCChoice(self):
        print('Choisir la carte son à utiliser :')
        print(sd.query_devices())
        sd.default.device = int(input('SC ?'))

    def mapping(self, mapIn, mapOut, lbIn=None, lbOut=None):
        if lbIn is None and lbOut is None:
            asio_out = sd.AsioSettings(channel_selectors=mapOut)
            asio_in = sd.AsioSettings(channel_selectors=mapIn)
            sd.default.extra_settings = asio_in, asio_out
            sd.default.channels = len(mapIn), len(mapOut)
        else:
            asio_out = sd.AsioSettings(channel_selectors=mapOut.append(lbOut))
            asio_in = sd.AsioSettings(channel_selectors=mapIn.append(lbIn))
            sd.default.extra_settings = asio_in, asio_out
            sd.default.channels = len(mapIn)+1, len(mapOut)+1
            self.compLat = True
        return self

    def mesure(self, out):
        return sd.playrec(out)

    def compenseLatency(self):
        T = 1
        f0 = 1e3

        t = np.arange(0, T, self.Fs)
        t_burst = T / 100
        burst = 0.5 * np.real(np.exp(-(1000 * (t - t_burst))**2 + 1j * 2 * np.pi * f0 * t))


if __name__ == "__main__":
    HPChirp = Data_Ploting(path='impulseresponse1.wav')

    blocksize = 1024

    # fifo = bf.Queue()
    # fifo_in = bf.Queue()
    #
    # for i in range(ceil(HPChirp.sig[0].N/blocksize)):
    #     data = HPChirp.sig[0].x[i*blocksize:i*blocksize+blocksize]
    #     fifo.put_nowait(data)
    #
    # def callback(indata, outdata, frames, time, status):
    #     try:
    #         data = fifo.get_nowait()
    #     except bf.Empty as e:
    #         raise sd.CallbackAbort from e
    #     if len(data) < len(outdata):
    #         outdata[:len(data)] = np.expand_dims(data, axis=1)
    #         outdata[len(data):].fill(0)
    #         raise sd.CallbackStop
    #     else:
    #         outdata[:] = np.expand_dims(data, axis=1)
    #     fifo_in.put(indata.copy())


    # sd.default.device = 10
    # asio_out = sd.AsioSettings(channel_selectors=[1])
    # asio_in = sd.AsioSettings(channel_selectors=[1])
    # sd.default.extra_settings = asio_in, asio_out
    # sd.default.samplerate = 44100
    # sd.default.channels = 1
    #
    # myrecording = sd.playrec(HPChirp.sig[0].x)

    # with sd.Stream(device=10, channels=(1,2), callback=callback, extra_settings=sd.default.extra_settings, blocksize=blocksize, samplerate=44100):
    #     print('#' * 80)
    #     print('press Return to quit')
    #     print('#' * 80)
    #     input()

    SC = SoundCard()
    SC.setFs(44100)
    SC.SCChoice()
    SC.mapping([1],[1])
    myrecording = SC.mesure(HPChirp.sig[0].x)

    sig = sg.Signal(myrecording, 44100)

    plt.figure()
    plt.plot(sig.x)
    plt.show()
    plt.tight_layout()

