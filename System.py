import numpy as np
import SoundCard as sc
from signals_generator import chirp
import ImpulseResponse as ri
from scipy.fftpack import fft, ifft


class System:
    def __init__(self, nbIn, nbOut):
        self.nbIn = nbIn
        self.nbOut = nbOut
        self.H = np.array((nbIn, nbOut))
        self.__Fs = 44100
        self.__Fmin = 10
        self.__Fmax = 100
        self.SC = sc.SoundCard()

    @property
    def Fs(self):
        return self.__Fs

    @property
    def Fmin(self):
        return self.__Fmin

    @property
    def Fmax(self):
        return self.__Fmax

    @Fs.setter
    def Fs(self, Fs):
        if Fs > 0:
            self.__Fs = Fs
        else:
            raise ValueError('La fréquence d\'échantillonnage doit être positive')

    @Fmin.setter
    def Fmin(self, Fmin):
        if Fmin < self.__Fmax:
            self.__Fmin = Fmin
        else:
            raise ValueError('Fmin doit être plus petit que Fmax')

    @Fmax.setter
    def Fmax(self, Fmax):
        if Fmax > self.__Fs//2:
            raise ValueError('Fmax ne peut pas être plus grand que Fs/2')
        elif Fmax < self.__Fmin:
            raise ValueError('Fmax doit être plus grand que Fmin')
        else:
            self.__Fmax = Fmax

    def Frange(self, Fmin, Fmax):
        if Fmin < Fmax < self.__Fs//2:
            self.__Fmin = Fmin
            self.__Fmax = Fmax
        else:
            raise ValueError('Fmin doit être plus petit que Fmax et Fmax doit être plus petit que Fs/2')

    def routing(self, inp, out):
        self.SC.Fs = self.__Fs
        self.SC.mapping(inp, out)
        return self

    def mesure(self):
        for noOut in range(self.nbOut):
            for noIn in range(self.nbIn):
                out = np.zeros((self.__Fs*2, self.nbOut))
                out[:, noOut] = chirp(self.__Fmin, self.__Fmax, 2, self.__Fs).x
                rec = self.SC.mesure(out)
                F, X = out[noOut].fft()
                F, Y = rec[noIn].fft()
                h = ifft(Y / X)
                self.H[noIn][noOut] = ri.ImpulseResponse(h, len(h), self.Fs)

if __name__ == "__main__":
    sys = System(12, 1)
    sys.Fs = 44100
    sys.Frange(100, 10000)

    sys.routing([x+1 for x in range(12)], [9])
    sys.mesure()