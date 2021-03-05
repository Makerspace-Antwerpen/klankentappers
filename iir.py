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



class IIRCombo:
    def __init__(self):
        self.filters = list()
    def addIIR(self, a_vals, b_vals):
        filter = IIR(a_vals,b_vals)
        self.filters.append(filter)
    def applyIIR(self, input):
        output = input
        for filter in self.filters:
            output = filter.applyIIR(output)
        return output
