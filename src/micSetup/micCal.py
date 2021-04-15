#!/bin/python3

import queue
import time
import datetime
import sounddevice as sd
import numpy as np
from lib.dbaMeasure import DBAMeasure
from lib.movingAverage import MovingAverage
from micSetup.adaI2S import micSetup

mic = micSetup()

rmsMA = MovingAverage(160)

dbaMeasure = DBAMeasure(0,0)

rmsQueue = queue.Queue()


def dbaMeasurementCallback(indata):
    rms = dbaMeasure.AWeightedRMS(indata.copy())
    rmsQueue.put(rms)


mic.addCallback(dbaMeasurementCallback)
fileCounter = 0


def upDateRMSMovingAverage():
    rms = rmsQueue.get()
    rmsMA.addValue(rms)
    return rms


def micCal(device):
    mic.setAudioDevice(device)
    mic.setup()
    mic.start()


    startTime = time.time()
    rms = 0
    while True:
        rms = upDateRMSMovingAverage()
        if time.time() > (startTime + 30):
            break
    
    return rms




    
    


