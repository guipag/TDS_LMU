from Signal import *
import numpy as np


class ImpulseResponse(Signal):
    def __init__(self, Nh, Fs):
        x = np.zeros(Nh)
        super(ImpulseResponse, self).__init__(x, Fs)
