from Data_Ploting import *
#from SoundCard import *
import sounddevice as sd
import queue as bf
from math import ceil
import numpy as np
import Signal as sg
import matplotlib.pyplot as plt

# HPChirp = exp.Data_Ploting()
#
# HPChirp.loadFromTxt('HPChirp.txt')
# HPChirp.plotTimeValues()
# HPChirp.rectangularWindowing(2750, 4750)
# HPChirp.plotTimeValues()
#
# HPChirp.computeFFT()
# HPChirp.PSD()
# HPChirp.FRF()
# HPChirp.ImpulseResponse()

HPChirp = Data_Ploting(path='HPChirp.txt')

#HPChirp.plotTimeValues()
#HPChirp.rectangularWindowing(0.02, 0.1)
#HPChirp.plotTimeValues(xlabel="Entré en V", ylabel="Sortie en Pa", color=['green','orange'],title="Signaux temporels fenêtrés")

#HPChirp.PSD()
#fig_FRF = HPChirp.FRF(1, 0)
#HPChirp.ImpulseResponse()

#fig_FRF.savefig("fig_FRF.png")

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

#SC = SoundCard()
#SC.SCChoice()
#SC.setFs(44100)
#SC.mesure(HPChirp.sig[0].x)

pass
