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

HPChirp = Data_Ploting(path='impulseresponse1.wav')

HPChirp.plotTimeValues()
#HPChirp.rectangularWindowing(0.02, 0.1)
#HPChirp.plotTimeValues(xlabel="Entré en V", ylabel="Sortie en Pa", color=['green','orange'],title="Signaux temporels fenêtrés")

#HPChirp.PSD()
#fig_FRF = HPChirp.FRF(1, 0)
#HPChirp.ImpulseResponse()

#fig_FRF.savefig("fig_FRF.png")


#SC = SoundCard()
#SC.SCChoice()
#SC.setFs(44100)
#SC.mesure(HPChirp.sig[0].x)


