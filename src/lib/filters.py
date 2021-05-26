#!/bin/python3

# Based on the work from Bert De Coensel, 2009
# Modified for use in this program by Wouter Peetermans, 2021

from lib.Ifilter import FilterInterface
import numpy
from numpy import pi, sin, cos, exp, sqrt
import numpy.fft
import pylab
import scipy.signal


class Filter(FilterInterface):
    """ base linear digital filter class (FIR/IIR) """

    def __init__(self, fs, b=[1], a=[1]):
        self._fs = fs
        self._b = b
        self._a = a
        self._z = numpy.zeros(max(len(a), len(b))-1)  # initial delay values
        self._pass = False
        if (len(b) == 1) and (b[0] == 1) and (len(a) == 1) and (a[0] == 1):
            self._pass = True

    def fs(self):
        """ returns the sample frequency of the filter (in Hz) """
        return self._fs

    def b(self):
        """ returns the b coefficients """
        return self._b

    def a(self):
        """ returns the a coefficients """
        return self._a

    def coefficients(self):
        """ returns the (b, a) coefficients """
        return (self.b(), self.a())

    def delays(self):
        """ returns the delay values of the filter (can be None) """
        return self._z

    def __str__(self):
        """ returns a string representation of the filter """
        return ('[Filter fs=%.1f, b=(' % self.fs()) + ', '.join(['%.4f' % x for x in self.b()]) + '), a=(' + ', '.join(['%.4f' % x for x in self.a()]) + ')]'

    def applyFilter(self, x):
        """ performs filtering on the signal x (numpy array), and remembers state """
        if self._pass == True:  # shortcut for pass-through filter
            return x
        y, self._z = scipy.signal.lfilter(self._b, self._a, x, zi=self._z)
        return y

    def freqz(self, f):
        """ returns the frequency response for the given frequencies """
        w, h = scipy.signal.freqz(self.b(), self.a(), 2.0*pi*(f/self.fs()))
        return h


class FilterFactory:
    @staticmethod
    def ExponentialAverage(fs, tau='fast'):
        """ returns a lowpass filter that performs an exponential averaging with given time constant tau (in seconds, or None/'slow'/'fast'/'impulse') """
        if tau == None:
            return Filter(fs=fs)  # pass-through filter
        if not type(tau) in (int, float):
            tau = {'slow': 1.000, 'fast': 0.125, 'impulse': 0.035}[tau]
        alpha = 1.0/(tau*fs)
        beta = 1.0 - alpha
        a = [1, -beta]
        b = [alpha]
        return Filter(fs=fs, b=b, a=a)

    @staticmethod
    def AWeightFilter(fs):
        """ returns an A-weighting filter for the given sample frequency, according to IEC/CD 1672 """
        assert fs >= 2.0e4, 'sample frequency too low for A-weighting filter design'
        f = (20.598997, 107.65265, 737.86223, 12194.217)
        z = 1.9997
        num = [(10.0**(z/20.0))*((2.0*pi*f[3])**2), 0.0, 0.0, 0.0, 0.0]
        den = numpy.convolve([1.0, 4.0*pi*f[3], (2.0*pi*f[3])**2],
                             [1.0, 4.0*pi*f[0], (2.0*pi*f[0])**2])
        den = numpy.convolve(den, [1.0, 2.0*pi*f[2]])
        den = numpy.convolve(den, [1.0, 2.0*pi*f[1]])
        b, a = scipy.signal.bilinear(num, den, fs)
        return Filter(fs=fs, b=b, a=a)

    @staticmethod
    def CWeightFilter(fs):
        """ returns an C-weighting filter for the given sample frequency, according to IEC/CD 1672 """
        assert fs >= 2.0e4, 'sample frequency too low for C-weighting filter design'
        f = (20.598997, 107.65265, 737.86223, 12194.217)
        z = 0.0619
        num = [(10.0**(z/20.0))*((2.0*pi*f[3])**2), 0.0, 0.0]
        den = numpy.convolve([1.0, 4.0*pi*f[3], (2.0*pi*f[3])**2],
                             [1.0, 4.0*pi*f[0], (2.0*pi*f[0])**2])
        b, a = scipy.signal.bilinear(num, den, fs)
        return Filter(fs=fs, b=b, a=a)

    @staticmethod
    def WeightFilter(fs, weight='L'):
        """ returns a weighting filter according to the given method """
        if weight == 'L':
            return Filter(fs=fs)  # pass-through filter
        elif weight == 'A':
            return FilterFactory.AWeightFilter(fs)
        elif weight == 'C':
            return FilterFactory.CWeightFilter(fs)
        else:
            raise 'unknown frequency weighting filter: ' + str(weight)

    @staticmethod
    def OctaveBandFilter(fs, fc, n=3):
        """ returns an octave band filter with center frequency fc, for sampling frequency fs and with order n
            for meaningful design results, the center frequency should preferably be in range fs/200 < fc < fs/5
            reference: ANSI S1.1-1986 (ASA 65-1986), Specifications for Octave-Band and Fractional-Octave-Band Analog and Digital Filters, 1993
        """
        assert fc <= 0.70 * \
            (fs/2.0), 'octave band filter design not possible for given fc and fs'
        # design Butterworth 2n'th-order octave band filter
        Qd = (pi/(2*n))/(sin(pi/(2*n)))
        alpha = (1.0 + sqrt(1.0 + 8.0*(Qd**2)))/(4.0*Qd)
        w = (2.0*(fc/fs)*sqrt(0.5)/alpha, 2.0*(fc/fs)*sqrt(2.0)*alpha)
        b, a = scipy.signal.butter(n, w, 'band')
        return Filter(fs=fs, b=b, a=a)

    @staticmethod
    def TertsBandFilter(fs, fc, n=3):
        """ returns a 1/3-octave band filter with center frequency fc, for sampling frequency fs and with order n
            for meaningful design results, the center frequency should preferably be in range fs/200 < fc < fs/5
            reference: ANSI S1.1-1986 (ASA 65-1986), Specifications for Octave-Band and Fractional-Octave-Band Analog and Digital Filters, 1993
        """
        assert fc <= 0.92 * \
            (fs/2.0), '1/3-octave band filter design not possible for given fc and fs'  # 0.92 makes fc=20kHz possible for fs=44.1kHz
        # design Butterworth 2n'th-order 1/3-octave band filter
        # min makes sure that upper cutoff is lower than nyquist frequency
        f = (fc/(2.0**(1.0/6.0)), min(fc*(2.0**(1.0/6.0)), 0.98*(fs/2.0)))
        Qr = fc/(f[1]-f[0])
        Qd = Qr*(pi/(2*n))/(sin(pi/(2*n)))
        alpha = (1.0 + sqrt(1.0 + 4.0*(Qd**2)))/(2.0*Qd)
        w = (2.0*(fc/fs)/alpha, 2.0*(fc/fs)*alpha)
        b, a = scipy.signal.butter(n, w, 'band')
        return Filter(fs=fs, b=b, a=a)

    @staticmethod
    def OuterMiddleEarFilter(fs, fr=4000.0):
        """ returns a filter that simulates the outer and middle ear transmission, with resonance frequency fr
            reference: Van Immerseel, L. M. and Martens, J.-P., Jasa 91(6):3511-3526, 1992.
        """
        wr = 2.0*pi*fr
        b, a = scipy.signal.bilinear([wr**2], [1, 0.33*wr, wr**2], fs)
        return Filter(fs=fs, b=b, a=a)
