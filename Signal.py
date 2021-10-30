import numpy as np
from scipy import signal
from scipy.fftpack import fft, ifft, rfft, irfft
from math import ceil, log2
import matplotlib.pyplot as plt

import matplotlib as mpl

plt.close('all')

mpl.rc('lines', linewidth=2)
mpl.rc('font', size=14)
mpl.rc('axes', linewidth=1.5, labelsize=14)
mpl.rc('legend', fontsize=14)
mpl.rcParams['figure.figsize']=(10,7)
mpl.rcParams['text.usetex'] = True


class Signal:
    """
    Classe représentant un signal à temps discret
    """
    def __init__(self, x, Fs):
        """
        Initalisation du signal
        :param x: array représentant le signal discret
        :param Fs: Fréquence d'échantillonnage
        """
        self.x = x
        self.Fs = Fs
        self.N = len(x)

    def __len__(self):
        """

        :return: taille du signal (int)
        """
        return self.N

    def __add__(self, other):
        """

        :param other: Signal à ajouter
        :return: Signal étant la somme des signaux
        """
        if len(self) != len(other):
            raise('Les dimensions ne correspondent pas')
        if self.Fs != other.Fs:
            return Signal(self.x + other.resample(self.Fs).x, self.Fs)
        else:
            return Signal(self.x + other.x, self.Fs)

    def __sub__(self, other):
        """

        :param other: Signal à soustraire
        :return: Signal étant la soustraction des deux signaux
        """
        if len(self) != len(other):
            raise('Les dimensions ne correspondent pas')
        if self.Fs != other.Fs:
            return Signal(self.x - other.resample(self.Fs).x, self.Fs)
        else:
            return Signal(self.x - other.x, self.Fs)

    def __mul__(self, other):
        if len(self) != len(other):
            raise('Les dimensions ne correspondent pas')
        if self.Fs != other.Fs:
            return Signal(self.x * other.resample(self.Fs).x, self.Fs)
        else:
            return Signal(self.x * other.x, self.Fs)

    def correlate(self, other=None):
        """
        Fonction de corrélation (inter si y != Null, auto sinon)
        :param y: Signal pour l'intercorrélation
        :return:
        """
        if other is not None:
            if self.Fs != other.Fs:
                R = signal.correlate(self.x, other.resample(self.Fs).x)
            else:
                R = signal.correlate(self.x, other.x)
            return -len(self.x) + 1 + np.arange(2 * len(self.x) - 1), 1 / self.Fs * R
        else:
            R = signal.correlate(self.x)
            return -len(self.x)+1+np.arange(2*len(self.x)-1), 1/self.Fs * R

    def convolve(self, other):
        """
        Convolution temporelle entre deux signaux
        :param other: Signal
        :return: Signal
        """
        if self.Fs != other.Fs:
            return Signal(np.convolve(self.x, other.resample(self.Fs).x)/self.Fs, self.Fs)
        else:
            return Signal(np.convolve(self.x, other.x) / self.Fs, self.Fs)

    def fft(self, Ntfd=None):
        """
        Transformée de Fourier du signal
        :param Ntfd: Nombre de raies spectrales
        :return: Axe fréquentiel, spectre
        """
        if Ntfd is not None:
            return np.fft.fftfreq(Ntfd, 1 / self.Fs), fft(self.x, Ntfd)
        else:
            return np.fft.fftfreq(self.next_power_of_2(self.N), 1 / self.Fs), fft(self.x, self.next_power_of_2(self.N))

    def values(self):
        """
        Getter des valeurs du signal
        :return: array
        """
        return self.x

    def time(self):
        return np.arange(self.N)/self.Fs

    @staticmethod
    def next_power_of_2(x):
        return 1 if x == 0 else 2 ** ceil(log2(x))

    @staticmethod
    def _rectangular(t1, t2, data, rate):
        """
        Fenêtrage rectangulaire à partir des temps en seconde
        :param t1: temps (s) de début
        :param t2: temps (s) de fin
        :param data: array représentant le signal
        :param rate: fréquence d'échantillonnage
        :return: array du signal fenêtré
        """
        return data[int(t1 * len(data) / (len(data) / rate)):int(t2 * len(data) / (len(data) / rate)):]

    def rectangularWindowing(self, deb, fin):
        """
        Fenêtrage rectangulaire
        :param deb:
        :param fin:
        :return: self (fluent)
        """
        self.x = self._rectangular(deb, fin, self.x, self.Fs)
        self.N = len(self.x)
        return self

    def hanningWindowing(self, deb, fin):
        """
        Fenêtrage avec Hanning
        :param deb: temps (s) de début du fenêtrage
        :param fin: temps (s) de fin du fenêtrage
        :return: self (fluent)
        """
        self.rectangularWindowing(deb, fin)
        self.x = self.x * (0.5 * (1 - np.cos(2 * np.pi * np.arange(len(self.x)) / len(self.x))))
        self.N = len(self.x)
        return self

    def resample(self, Fs):
        """
        Pour les opérations mathématiques, modification de Fs
        :param Fs: Nouvelle fréquence d'échantillonnage
        :return: Signal à la nouvelle fréquence d'échantillonnage
        """
        Nx = self.x.shape[0]
        X = rfft(self.x)
        newshape = list(self.x.shape)
        newshape[0] = Fs // 2 + 1
        Y = np.zeros(Fs, X.dtype)

        N = min(Fs, Nx)
        nyq = N // 2 + 1  # Slice index that includes Nyquist if present
        sl = [slice(None)] * self.x.ndim
        sl[0] = slice(0, nyq)
        Y[tuple(sl)] = X[tuple(sl)]

        if Fs < self.Fs:
            sl[0] = slice(N // 2, N // 2 + 1)
            Y[tuple(sl)] *= 2.
        else:
            sl[0] = slice(N // 2, N // 2 + 1)
            Y[tuple(sl)] *= 0.5

        y = irfft(Y)
        y *= (float(Fs) / float(Nx))

        return Signal(y, Fs)

    @staticmethod
    def decorate(ax, title=None, xlabel=None, ylabel=None):
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid()
        ax.legend()
        plt.tight_layout()

    def plot(self, title="Signal temporel", xlabel='Temps (s)', ylabel='ouput', color='r'):
        plt.figure()
        plt.stem(self.time(), self.values(), color, label=xlabel)
        #self.decorate(fig, title=title, xlabel=xlabel)
        plt.show()
        #return fig


if __name__ == "__main__":
    n = np.arange(1024)
    x = 0.9*np.sin(2*np.pi*10*n/1000)
    sig = Signal(x, 1000)
    sig.plot()

    sig2 = sig.resample(500)
    sig2.plot()