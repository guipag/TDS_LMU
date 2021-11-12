import sounddevice as sd
from Data_Ploting import *
from signals_generator import tone_bursts, chirp
import numpy as np
from Signal import *


class SoundCard:
    def __init__(self):
        self.Fs = 44100
        self.compLat = False
        self.nbIn = 1
        self.nbOut = 1
        self.lbIn = None
        self.lbOut = None
        self.__latLag = 0

    @property
    def Fs(self):
        return self.__Fs

    @Fs.setter
    def Fs(self, Fs):
        if Fs > 0:
            self.__Fs = Fs
            sd.default.samplerate = Fs
        else:
            raise ValueError('La fréquence d\'échantillonnage doit être positive')
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
        sig = np.roll(sig, -self.__latLag, axis=1)
        #return [Signal(sig[x, :], self.Fs) for x in range(len(sig))]
        return sig

    def compenseLatency(self):
        sig = tone_bursts(1000, 0.9, 1, self.Fs)
        out = np.zeros((self.Fs*1, self.nbOut))
        out[:, -1] = sig
        mes = self.mesure(out)
        corr = np.correlate(mes[:, self.lbIn], sig)
        self.__latLag = np.argmax(corr) - len(sig) + 1
        return self


if __name__ == "__main__":
    #HPChirp = Data_Ploting(path='impulseresponse1.wav')

    SC = SoundCard()
    SC.Fs = 48000
    SC.SCChoice()
    SC.mapping([x+1 for x in range(18)], [x+1 for x in range(8)])
    out = np.zeros((96000, 8))
    out[:, 7] = chirp(20, 1000, 2, 48000).x
    myrecording = SC.mesure(out)

    sig = sg.Signal(myrecording, 48000)

    plt.figure()
    plt.plot(myrecording[:,4])
    plt.show()
    plt.tight_layout()

