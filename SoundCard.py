import sounddevice as sd
from Data_Ploting import *
from signals_generator import tone_bursts
import numpy as np


class SoundCard:
    def __init__(self):
        self.Fs = 48000
        self.compLat = False
        self.nbIn = 1
        self.nbOut = 1
        self.lbIn = None
        self.lbOut = None
        self.latLag = 0

    def setFs(self, Fs):
        self.Fs = Fs
        sd.default.samplerate = Fs
        return self

    def SCChoice(self):
        print('Choisir la carte son à utiliser :')
        print(sd.query_devices())
        sd.default.device = int(input('SC ?'))

    def mapping(self, mapIn, mapOut, lbIn=None, lbOut=None):
        """
        Paramétrage des I/O de la carte son
        :param mapIn: (array) liste des entrées à utiliser
        :param mapOut: (array) liste des sorties à utiliser
        :param lbIn: (int) entrée loopback
        :param lbOut: (int) sortie loopback
        :return: self
        """
        if lbIn is None and lbOut is None:
            asio_out = sd.AsioSettings(channel_selectors=mapOut)
            asio_in = sd.AsioSettings(channel_selectors=mapIn)
            sd.default.extra_settings = asio_in, asio_out
            sd.default.channels = len(mapIn), len(mapOut)
            self.nbIn = len(mapIn)
            self.nbOut = len(mapOut)
        else:
            asio_out = sd.AsioSettings(channel_selectors=mapOut.append(lbOut))
            asio_in = sd.AsioSettings(channel_selectors=mapIn.append(lbIn))
            sd.default.extra_settings = asio_in, asio_out
            sd.default.channels = len(mapIn)+1, len(mapOut)+1
            self.compLat = True
            self.nbIn = len(mapIn)+1
            self.nbOut = len(mapOut)+1
            self.lbIn = lbIn
            self.lbOut = lbOut
        return self

    def mesure(self, out):
        sig = sd.playrec(out, blocking=True)
        return np.roll(sig, -self.latLag, axis=1)

    def compenseLatency(self):
        sig = tone_bursts(1000, 0.9, 1, self.Fs)
        out = np.zeros((self.Fs*1, self.nbOut))
        out[:, -1] = sig
        mes = self.mesure(out)
        corr = np.correlate(mes[:, self.lbIn], sig)
        self.latLag = np.argmax(corr) - len(sig) + 1
        return self

if __name__ == "__main__":
    HPChirp = Data_Ploting(path='impulseresponse1.wav')

    SC = SoundCard()
    SC.setFs(44100)
    SC.SCChoice()
    SC.mapping([1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    out = np.zeros((480000, 20))
    out[:, 1] = HPChirp.sig[0].x
    myrecording = SC.mesure(out)

    sig = sg.Signal(myrecording, 44100)

    plt.figure()
    plt.plot(sig.x[:,8])
    plt.show()
    plt.tight_layout()

