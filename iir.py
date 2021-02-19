#!/bin/python3

import numpy as np
from scipy import signal
import math



class IIR:
    def __init__(self, a_vals, b_vals):
        self.a_vals = a_vals
        self.b_vals = b_vals
        self.zi = signal.lfilter_zi(b_vals,a_vals)

    def applyIIR(self, input):
        outdata, self.zi = signal.lfilter(self.b_vals, self.a_vals, input, -1, self.zi)
        #outdata = signal.lfilter(self.b_vals, self.a_vals, input, -1)
        return outdata
