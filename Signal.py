import numpy as np
from scipy import signal
from scipy.fftpack import fft, ifft
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
        return Signal(self.x + other.x, self.Fs)

    def __sub__(self, other):
        """

        :param other: Signal à soustraire
        :return: Signal étant la soustraction des deux signaux
        """
        return Signal(self.x - other.x, self.Fs)

    def __mul__(self, other):
        if len(self) == len(other):
            return Signal(self.x * other.x, self.Fs)
        else:
            raise('Les dimensions ne correspondent pas')

    def correlate(self, y=None):
        """
        Fonction de corrélation (inter si y != Null, auto sinon)
        :param y: Signal pour l'intercorrélation
        :return:
        """
        if y is not None:
            R = signal.correlate(self.x, y)
        else:
            R = signal.correlate(self.x)
        return -len(self.x)+1+np.arange(2*len(self.x)-1), 1/self.Fs * R

    def convolve(self, other):
        """
        Convolution temporelle entre deux signaux
        :param other: Signal
        :return: Signal
        """
        return Signal(np.convolve(self.x, other.x)/self.Fs, self.Fs)

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
        Y = np.zeros(Fs)
        # ifft avec zero-padding
        return Signal(ifft(Y), Fs)

    @staticmethod
    def decorate(ax, title=None, xlabel=None, ylabel=None):
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid()
        ax.legend()
        plt.tight_layout()

    def plot(self, title="Signal temporel", xlabel='Temps (s)', ylabel='ouput', color='r'):
        fig, ax = plt.figure()
        ax.plot(self.time(), self.values(), color, label=xlabel)
        self.decorate(ax, title=title, xlabel=xlabel)
        plt.show()
        return fig

