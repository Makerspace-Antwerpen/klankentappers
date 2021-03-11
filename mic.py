#!/bin/python3

import sounddevice as sd

class Mic:

    def __init__(self):
        self.callbackList = list()
        self.windowsPerSecond = 8
        self.audioSampleRate = 48000
        self.audioDevice = 1

    def addCallback(self, callBack):
        self.callbackList.append(callBack)

    def setSamplesPerSecond(self, count):
        self.windowsPerSecond = count

    def setAudioSampleRate(self, sampleRate):
        self.audioSampleRate = sampleRate
    
    def sefAudioDevice(self, audioDevice):
        self.audioDevice = audioDevice

    def callback(self, indata, frames, time, status):
        flatData = indata.flatten() # input is 2d array. making 1d array from it

        for cb in self.callbackList:
            cb(flatData)

    def setup(self):
        blocksize = int(self.audioSampleRate / self.windowsPerSecond)

        self.inputStream = sd.InputStream(device=self.audioDevice, channels=1, callback=self.callback,
                            blocksize=blocksize,
                            samplerate=self.audioSampleRate)

    def start(self):
        self.inputStream.start()

    def stop(self):
        self.inputStream.stop()
    
    def __del__(self):
        if self.inputStream:
            self.inputStream.close()
