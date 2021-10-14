import numpy as np
from scipy import signal
import Signal as sg

def sinus(freq, amplitude, RSB, Fs, duration=1):

    time = np.arange(0, duration, 1/(Fs))

    function = amplitude * np.sin(2 * np.pi * freq * time + i)

    noise = np.mean(function ** 2) / (10 ** (RSB / 10))
    function += np.sqrt(noise) * np.random.randn(len(time))
    function+= noise

    return sg.Signal(function,Fs)

def multiple_sinus(freq, amplitude,  RSB, Fs, duration=1):
    """
    Replace by multisine signal

    :param freq:
    :param amplitude:
    :param RSB:
    :param Fs:
    :param duration:
    :return:
    """
    time = np.arange(0, duration, 1/(Fs))

    function_1 = amplitude * np.sin(2 * np.pi * freq * time)
    function_2 = amplitude * np.sin(2 * np.pi * (freq*6/5) * time)
    function_3 = amplitude * np.sin(2 * np.pi * (freq * 3 / 2) * time)
    function_4 = amplitude * np.sin(2 * np.pi * (freq * 2) * time)

    function_final = function_1 + function_2 + function_3 + function_4

    noise = np.mean(function_final ** 2) / (10 ** (RSB / 10))
    function_final += np.sqrt(noise) * np.random.randn(len(time))
    function_final += noise

    return sg.Signal(function_final,Fs)


def chirp(Fmin, Fmax, duration, Fs):

    time = np.arange(0, duration, 1 / Fs)
    function = signal.chirp(time, f0=Fmin, f1=Fmax, t1=duration, method='linear')

    return sg.Signal(function,Fs)


def tone_bursts(F0,A0,duration, Fs):

    time = np.arange(0, duration, 1/Fs)
    phi0 = 2*np.pi*np.random.rand(1)
    sigma_t = 0.05/6
    tc = 3*sigma_t
    x = A0*np.cos(2*np.pi*F0*time+phi0)
    w = np.exp(-(time-tc)**2/(2*sigma_t**2))
    x = np.tile(x, 3)
    w = np.tile(w, 3)
    function = x*w

    return sg.Signal(function,Fs)


# def sawtooth(freq,  amplitude, RSB, i, duration = 1):
#
#         time = np.arange(0, duration, 1/Fs)
#         function = amplitude * signal.sawtooth(2 * np.pi * freq * time + i)
#         noise = np.mean(function ** 2) / (10 ** (RSB / 10))
#         function += np.sqrt(noise) * np.random.randn(len(time))
#         function += noise
#         return time, function
#
#
# def multiple_sawtooth(freq, amplitude, RSB, i, duration=1):
#
#     time = np.arange(0, duration, 1 / Fs)
#     function_1 = amplitude*signal.sawtooth(2 * np.pi * freq * time + i)
#     function_2 = amplitude*signal.sawtooth(2 * np.pi * (freq*6/5)* time + i)
#     function_3 = amplitude*signal.sawtooth(2 * np.pi * (freq*3/2) * time+ i)
#     function_4 = amplitude*signal.sawtooth(2 * np.pi * freq *2* time + i)
#
#     function_final = function_1 + function_2 + function_3 + function_4
#
#     noise = np.mean(function_final ** 2) / (10 ** (RSB / 10))
#     function_final += np.sqrt(noise) * np.random.randn(len(time))
#     function_final += noise
#
#     return time, function_final

def triangle(freq, amplitude, RSB, Fs, duration=1):

    time = np.arange(0, duration, 1 / Fs)
    function = amplitude*signal.sawtooth(2 * np.pi * freq * time , 0.5)

    noise = np.mean(function ** 2) / (10 ** (RSB / 10))
    function += np.sqrt(noise) * np.random.randn(len(time))
    function += noise

    return sg.Signal(function,Fs)


# def multiple_triangle(freq, amplitude, RSB, i, duration=1):
#
#     time = np.arange(0, duration, 1 / Fs)
#
#     function_1 = amplitude*signal.sawtooth(2 * np.pi * freq * time + i , 0.5)
#     function_2 = amplitude*signal.sawtooth(2 * np.pi * (freq*6/5) * time + i, 0.5)
#     function_3 = amplitude*signal.sawtooth(2 * np.pi * (freq*3/2) * time + i, 0.5)
#     function_4 = amplitude*signal.sawtooth(2 * np.pi * (freq *2) * time + i, 0.5)
#
#     function_final = function_1 + function_2 + function_3 + function_4
#
#     noise = np.mean(function_final ** 2) / (10 ** (RSB / 10))
#     function_final += np.sqrt(noise) * np.random.randn(len(time))
#     function_final += noise
#
#     return time, function_final
#


def square(freq, amplitude, RSB, Fs, duration=1):

    time = np.arange(0, duration, 1/Fs)

    function = amplitude*signal.square(2 * np.pi * freq * time)

    noise = np.mean(function ** 2) / (10 ** (RSB / 10))
    function += np.sqrt(noise) * np.random.randn(len(time))
    function += noise

    return sg.Signal(function,Fs)

# def Gibbs(freq, RSB, number_of_sin, i, duration = 1):
#
#     time = np.arange(0, duration, 1/Fs)
#
#     function = 0
#
#     for k in range(1, number_of_sin):
#
#         function = function + ((np.sin(2*np.pi*((2*k)-1)*freq*time+i))/((2*k)-1))
#         function = (4/np.pi) * function
#
#     noise = np.mean(function ** 2) / (10 ** (RSB / 10))
#     function += np.sqrt(noise) * np.random.randn(len(time))
#     function += noise
#
#     return time, function

#
# def multiple_square(freq, amplitude, RSB, Fs, duration=1):
#
#     time = np.arange(0, duration, 1/Fs)
#
#     function_1 = amplitude* signal.square(2 * np.pi * freq * time  + i)
#     function_2 = amplitude * signal.square(2 * np.pi * (freq*6/5) * time + i )
#     function_3 = amplitude * signal.square(2 * np.pi * (freq*3/2) * time + i)
#     function_4 = amplitude * signal.square(2 * np.pi * freq * 2* time + i)
#
#     function_final = function_1 + function_2 + function_3 + function_4
#
#     noise = np.mean(function_final ** 2) / (10 ** (RSB / 10))
#     function_final += np.sqrt(noise) * np.random.randn(len(time))
#     function_final += noise
#
#     return time, function_final


def white_noise(N,Fs):
    function = np.random.randn(N)
    return sg.Signal(function,Fs)
