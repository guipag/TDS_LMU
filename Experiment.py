import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, ifft

import matplotlib as mpl
from math import ceil, log2

mpl.rc('lines', linewidth=2)
mpl.rc('font', size=14)
mpl.rc('axes', linewidth=1.5, labelsize=14)
mpl.rc('legend', fontsize=14)

class Experiment:
    def loadFromTxt(self, path):
        data = np.loadtxt(path)

        self.N = len(data)  #  number of points

        self.t = data[:, 0]  #  time axis
        self.x = data[:, 1]  #  input (generator output) [V]
        self.y = data[:, 2]  #  output (microphone) [Pa]

        self.Fs = 1 / (self.t[1] - self.t[0])

    def setFs(self,Fs):
        self.Fs = Fs

    def plotTimeValues(self):
        plt.figure()
        plt.plot(self.t, self.y, 'r', label='ouput')
        plt.plot(self.t, self.x, 'b', label='input')
        plt.title("Signaux temporels bruts")
        plt.grid()
        plt.xlabel('Time (s)')
        plt.show()

    def computeFFT(self):
        NTFD = self.next_power_of_2(len(self.t))

        self.N = NTFD  # total number of points
        self.n = np.arange(self.N)

        self.Freq = np.fft.fftfreq(NTFD, 1 / self.Fs)

        self.X = fft(self.x, NTFD)
        self.Y = fft(self.y, NTFD)
        self.H = np.zeros(self.N, dtype=complex)

        self.H = self.Y / self.X
        self.h = ifft(self.H)

    def PSD(self):
        plt.figure()
        plt.semilogx(self.Freq[1:self.N // 2], np.abs(self.X[1:self.N // 2]) ** 2, 'r', label='input')
        plt.grid()
        plt.xlabel("Fréquence (Hz)")
        plt.show()

        plt.figure()
        plt.semilogx(self.Freq[:self.N // 2], np.abs(self.Y[:self.N // 2]) ** 2, 'b', label='ouput')
        plt.grid()
        plt.xlabel("Fréquence (Hz)")
        plt.show()

    def next_power_of_2(self,x):
        return 1 if x == 0 else 2 ** ceil(log2(x))

    def FRF(self):
        plt.figure()
        ax1 = plt.subplot(211)
        ax1.set_title("FRF")
        plt.semilogx(self.Freq[1:self.N // 2], 20 * np.log(np.abs(self.H[1:self.N // 2])))
        plt.xlabel("Fréquence (Hz)")
        plt.grid()
        ax2 = plt.subplot(212)
        ax2.set_title("Phase")
        plt.semilogx(self.Freq[1:self.N // 2], np.unwrap(np.angle(self.H[1:self.N // 2])))
        plt.xlabel("Fréquence (Hz)")
        plt.grid()
        plt.tight_layout()
        plt.show()

    def ImpulseResponse(self):

        plt.figure()
        plt.title("Réponse impulsionnelle")
        plt.stem(self.n[:200] / self.Fs * 1000, np.real(self.h[:200]), markerfmt=" ")
        plt.xlabel("Temps (ms)")
        plt.grid()
        plt.tight_layout()
        plt.show()

    def rectangularWindowing(self, deb, fin):
        self.t = self.t[deb:fin]
        self.x = self.x[deb:fin]
        self.y = self.y[deb:fin]
