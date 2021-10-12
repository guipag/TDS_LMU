import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.fftpack import fft, ifft
import re
from scipy.io import wavfile

import matplotlib as mpl
from math import ceil, log2

import Signal as sg

plt.close('all')

mpl.rc('lines', linewidth=2)
mpl.rc('font', size=14)
mpl.rc('axes', linewidth=1.5, labelsize=14)
mpl.rc('legend', fontsize=14)
mpl.rcParams['figure.figsize']=(10,7)
mpl.rcParams['text.usetex'] = True

class Data_Ploting:
    
    def __init__(self, path=None, t=None, x=None, y=None):
        self.sig = []
        if path is not None and re.match('.+\.txt$', path):
            data = np.loadtxt(path)
            t = data[:, 0]
            sh = data.shape
            for i in range(1, sh[1]):
                self.sig.append(sg.Signal(data[:, i], 1 / (t[1] - t[0])))
        elif path is not None and re.match('.+\.wav$', path):
            Fs, rawdata_wav = wavfile.read(path)
            sh = rawdata_wav.shape
            for i in range(1, sh[1]):
                self.sig.append(sg.Signal(rawdata_wav[:, i], Fs))
        elif t is not None and x is not None and y is not None:
            self.sig.append(sg.Signal(x, 1 / (t[1] - t[0])))
            self.sig.append(sg.Signal(y, 1 / (t[1] - t[0])))
        else:
            print("Erreur d'utilisation : Indiquez à la classe le chemin d'accès au fichier OU fournissez les 'array' t, x et y")
        try :
            self.N = len(self.sig[0])  #  number of points
            self.Fs = self.sig[0].Fs
        except AttributeError:
            pass
        
    def setFs(self, Fs):
        self.Fs = Fs
    
    def rectangularWindowing(self, deb, fin):
        for i in range(len(self.sig)):
            self.sig[i].rectangularWindowing(deb, fin)
        self.N = len(self.sig[0])
        return self

    def hanningWindowing(self, deb, fin):
        for i in range(len(self.sig)):
            self.sig[i].hanningWindowing(deb, fin)
        self.N = len(self.sig[0])
        return self

    @staticmethod
    def decorate(ax, title=None, xlabel=None, ylabel=None):
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid()
        ax.legend()
        plt.tight_layout()

    def plotTimeValues(self, title="Signaux temporels", xlabel='input', ylabel='ouput', color=['b','r']):
        fig, ax = plt.subplots()
        for i in range(len(self.sig)):
            ax.plot(self.sig[i].time(), self.sig[i].values(), label=xlabel)
        self.decorate(ax, title=title, xlabel='Time (s)')
        plt.show()
        return fig

    def PSD(self, voies=0):
        """
        Affichage du/des PSD
        :param voies: (int) numéro de la voie ou (array) listes des voies
        :return: fig
        """
        if len(voies) == 1:
            F, X = self.sig[voies].fft()
            fig1, ax1 = plt.figure()
            ax1.semilogx(F[1:len(F) // 2], np.abs(X[1:len(F) // 2]) ** 2, 'r', label='input')
            self.decorate(ax1, xlabel="Fréquence (Hz)")
            plt.show()
            return fig1
        else:
            for i in voies:
                F, X = self.sig[voies[i]].fft()
                fig1, ax1 = plt.subplots()
                ax1.semilogx(F[1:len(F) // 2], np.abs(X[1:len(F) // 2]) ** 2, 'r', label='input')
                self.decorate(ax1, xlabel="Fréquence (Hz)")
                plt.show()
            return fig1

    def FRF(self, sigIn=0, sigOut=1):
        F, X = self.sig[sigIn].fft()
        F, Y = self.sig[sigOut].fft()
        H = Y/X
        fig, ax = plt.subplots(2)
        ax[0].semilogx(F[1:len(F) // 2], 20 * np.log(np.abs(H[1:len(F) // 2])))
        self.decorate(ax[0], xlabel="Fréquence (Hz)",title="FRF")

        ax[1].semilogx(F[1:len(F) // 2], np.unwrap(np.angle(H[1:len(F) // 2])))
        self.decorate(ax[1], xlabel="Fréquence (Hz)", title="Phase")
        plt.show()
        return fig 

    def ImpulseResponse(self, sigIn=0, sigOut=1):
        F, X = self.sig[sigIn].fft()
        F, Y = self.sig[sigOut].fft()
        h = ifft(Y / X)
        fig, ax = plt.subplots()
        plt.stem(np.arange(200) / self.Fs * 1000, np.real(h[:200]), markerfmt=" ")
        self.decorate(ax, title="Réponse impulsionnelle", xlabel="Temps (ms)")
        plt.show()
        return fig

    def interSpectre(self, sigIn=0, sigOut=1):
        self.sig[sigIn].correlate(self.sig[sigOut])
        l = -len(self.sig[sigIn])+1+np.arange(2*len(self.sig[sigIn])-1)
        Sxy = fft(self.Rxy, len(l))
        Freq2 = np.fft.fftfreq(len(l), 1/self.Fs)
        return Freq2, Sxy

    def autoSpectre(self, voie):
        Rxx = self.sig[voie].correlate()
        l = -len(self.sig[voie]) + 1 + np.arange(2 * len(self.sig[voie]) - 1)
        Sxx = fft(Rxx, len(l))
        Freq2 = np.fft.fftfreq(len(l), 1 / self.Fs)
        return Freq2, Sxx

    def coherence(self, sigIn = 0, sigOut = 1):
        Freq2, Sxy = self.interSpectre()
        Freq2, Sxx = self.autoSpectre(sigIn)
        Freq2, Syy = self.autoSpectre(sigOut)
        gamma = np.abs(Sxy) / np.sqrt(Sxx * Syy)

        fig, ax = plt.subplots()
        plt.semilogx(Freq2, np.real(gamma))
        self.decorate(ax, title="Fonction de cohérence", xlabel="Fréquence (Hz)")
        plt.show()
        return fig
