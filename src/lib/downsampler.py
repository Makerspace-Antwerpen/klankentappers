#!/bin/python3


# Based on the work from Bert De Coensel, 2009
# Modified for use in this program by Wouter Peetermans, 2021

class Downsampler:
  """ class for downsampling signals with an integer factor, using an 8th order Chebyshev type I filter """
  def __init__(self, factor = 2):
    if type(factor) != int:
      raise 'Downsampler only works with integer factors'
    self._factor = factor
    self._b, self._a = scipy.signal.cheby1(8, 0.05, 0.8/factor)
    self._z = numpy.zeros(max(len(self._a),len(self._b))-1) # initial delay values

  def process(self, x):
    """ downsamples the signal x """
    y, self._z = scipy.signal.lfilter(self._b, self._a, x, zi = self._z)
    return y[::self._factor]


class DownsamplerBank:
  """ cascade of downsamplers, to be used by a filterbank """
  def __init__(self, fs, n, factor = 2):
    self._fs = fs/(factor**(numpy.arange(float(n)+1.0))) # original and new sample frequencies
    self._x = {} # dict with downsampled signals
    self._d = [Downsampler(factor = factor) for i in range(n)]

  def fs(self):
    """ returns a numpy array with the original and new sample frequencies of the downsampler bank """
    return self._fs

  def __len__(self):
    """ returns the number of downsampling steps """
    return len(self.fs())

  def process(self, x):
    """ resamples the signal x (numpy array) """
    self._x[self.fs()[0]] = x.copy()
    for i in range(1, len(self)):
      self._x[self.fs()[i]] = self._d[i-1].process(self._x[self.fs()[i-1]]).copy()

  def __getitem__(self, fs):
    """ returns the signal at the given sample frequency """
    return self._x[fs]