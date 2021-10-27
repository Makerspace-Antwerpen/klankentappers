#!/bin/python3

from lib.Ifilter import FilterInterface
import sys


class Mic:

    def __init__(self, sd, configFile="none"):
        self.callbackList = list()
        self.filterList = list()
        self.sd = sd
        self.windowsPerSecond = 8
        self.audioSampleRate = 48000
        self.audioDevice = 1

    def addCallback(self, callBack):
        self.callbackList.append(callBack)

    def addFilter(self, filter: FilterInterface):
        self.filterList.append(filter)

    def setSamplesPerSecond(self, count: int):
        self.windowsPerSecond = count

    def setAudioSampleRate(self, sampleRate: int):
        self.audioSampleRate = sampleRate

    def setAudioDevice(self, audioDevice: int):
        self.audioDevice = audioDevice

    def callback(self, indata, frames, time, status):
        if status:
            print(status, sys.stderr)
        flatData = indata.flatten()  # input is 2d array. making 1d array from it
        filteredData = flatData.copy()
        for filter in self.filterList:
            filteredData = filter.applyFilter(filteredData)
        for cb in self.callbackList:
            cb(filteredData.copy())

    def setup(self):
        blocksize = int(self.audioSampleRate / self.windowsPerSecond)

        self.inputStream = self.sd.InputStream(device=self.audioDevice, channels=1, dtype='float32', callback=self.callback,
                                               blocksize=blocksize,
                                               samplerate=self.audioSampleRate,
                                               latency=5)

    def start(self):
        self.inputStream.start()

    def stop(self):
        self.inputStream.stop()

    def __del__(self):
        if hasattr(self, 'inputStream'):
            self.inputStream.close()
        # if self.inputStream:
        #     self.inputStream.close()
