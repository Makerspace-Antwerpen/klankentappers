#!/bin/python3


from lib.filters import FilterFactory
from lib.downsampler import DownsamplerBank
import numpy as np
import math

# 4 downslamplers factor 2

class TertsMeasure:
    def __init__(self, fs, rmsReference: float, dbaReference: float):
        self.fs = fs
        self.rmsReference = rmsReference
        self.dbaReference = dbaReference
        self.downsamplerBank = DownsamplerBank(fs, 4, 2)
        self.centerFreqs = [16, 20, 25, 32.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000]
        self.buildFilters()


    def buildFilters(self):
        self.filterList = list()
        for freq in self.centerFreqs:
            if freq < (self.fs/(5 * 16)):
                self.filterList.append(FilterFactory.TertsBandFilter(self.fs/16, freq))
            elif freq < (self.fs/(5 * 8)):
                self.filterList.append(FilterFactory.TertsBandFilter(self.fs/8, freq))
            elif freq < (self.fs/(5 * 4)):
                self.filterList.append(FilterFactory.TertsBandFilter(self.fs/4, freq))
            elif freq < (self.fs/(5 * 2)):
                self.filterList.append(FilterFactory.TertsBandFilter(self.fs/2, freq))
            else:
                self.filterList.append(FilterFactory.TertsBandFilter(self.fs, freq))


    def calcTertsBands(self, input):
        self.downsamplerBank.process(input)
        outList = list()
        for filter in self.filterList:
            # outData = filter.applyFilter(downSampleSet[dataToUse])
            outData = filter.applyFilter(self.downsamplerBank.__getitem__(filter.fs()))
            balancedInput = outData - np.mean(outData)
            rms = np.sqrt(np.mean(balancedInput**2))
            db = 20 * math.log(rms/self.rmsReference,10) + self.dbaReference
            outList.append(db)
        return outList