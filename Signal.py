import numpy as np
from scipy import signal
from scipy.fftpack import fft
from math import ceil, log2

class Signal:
    def __init__(self, x, Fs):
        self.x = x
        self.Fs = Fs
        self.N = len(x)

    def __len__(self):
        return self.N

    def __add__(self, other):
        return Signal(self.x + other.x, self.Fs)

    def __sub__(self):
        return Signal(self.x - other.x, self.Fs)

    def __mul__(self, other):
        if len(self) == len(other):
            return Signal(self.x * self.y, self.Fs)
        else:
            raise('Les dimensions ne correspondent pas')

    def correlate(self, y=None):
        if y is not None:
            R = signal.correlate(self.x, y)
        else:
            R = signal.correlate(self.x)
        return -len(self.x)+1+np.arange(2*len(self.x)-1), 1/self.Fs * R

    def fft(self, Ntfd=None):
        if Ntfd is not None:
            return np.fft.fftfreq(Ntfd, 1 / self.Fs), fft(self.x, Ntfd)
        else:
            return np.fft.fftfreq(self.next_power_of_2(self.N), 1 / self.Fs), fft(self.x, self.next_power_of_2(self.N))

    def values(self):
        return self.x

    def time(self):
        return np.arange(self.N)/self.Fs

    @staticmethod
    def next_power_of_2(x):
        return 1 if x == 0 else 2 ** ceil(log2(x))

    @staticmethod
    def _rectangular(t1, t2, data, rate):
        return data[int(t1 * len(data) / (len(data) / rate)):int(t2 * len(data) / (len(data) / rate)):]

    def rectangularWindowing(self, deb, fin):
        self.x = self._rectangular(deb, fin, self.x, self.Fs)
        self.N = len(self.x)
        return self

    def hanningWindowing(self, deb, fin):
        self.rectangularWindowing(deb, fin)
        self.x = self.x * (0.5 * (1 - np.cos(2 * np.pi * np.arange(len(self.x)) / len(self.x))))
        self.N = len(self.x)
        return self
