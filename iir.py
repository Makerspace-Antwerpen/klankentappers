#!/bin/python3

import numpy as np


class IIR(object):
    """
    Bandpass IIR Filter

    Parameters
    ----------
    a, b: list of float
      Parameters that define an IIR filter

    Attributes
    ----------
    x, y: array of float
      Local variables of IIR calculations.

    """
    def __init__(self, a, b):
        assert len(b) == len(a)
        self.b = np.array(b)
        self.a = np.array(a)
        self.N = len(a)
        self.x = np.zeros(self.N)
        self.y = np.zeros(self.N)

    def filter_sample(self, sample):
        """
        This is the standard IIR calculation.
        Parameters
        ----------
        sample: float or int
          The next element of the stream.
        """
        # Shift x and y to the right by 1
        self.x[1:] = self.x[:- 1]
        self.y[1:] = self.y[:-1]
        # Update x[0] and y[0]
        self.x[0] = sample
        self.y[0] = self.a[0] * self.x[0]
        self.y[0] += sum(self.a[1:]*self.x[1:] - self.b[1:]*self.y[1:])
        return self.y[0]