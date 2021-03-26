#!/bin/python3

import numpy as np
from scipy import signal
import math
from lib.Ifilter import FilterInterface



class IIR(FilterInterface):
    def __init__(self, a_vals, b_vals):
        self.a_vals = a_vals
        self.b_vals = b_vals
        self.zi = signal.lfilter_zi(b_vals,a_vals)

    def applyFilter(self, input):
        outdata, self.zi = signal.lfilter(self.b_vals, self.a_vals, input, -1, self.zi)
        #outdata = signal.lfilter(self.b_vals, self.a_vals, input, -1)
        return outdata



class IIRCombo(FilterInterface):
    def __init__(self):
        self.filters = list()
    def addIIR(self, a_vals, b_vals):
        filter = IIR(a_vals,b_vals)
        self.filters.append(filter)
    def applyFilter(self, input):
        output = input
        for filter in self.filters:
            output = filter.applyFilter(output)
        return output
