#!/bin/python3

import queue
import time
import datetime
import soundfile as sf
import sounddevice as sd
import numpy as np
from lib.dbaMeasure import DBAMeasure
from lib.movingAverage import MovingAverage
from micSetup.adaI2S import micSetup

MIC_REF_RMS = 0.008324243692980756
MIC_REF_DBA = 71.5


mic = micSetup()
dbaMeasure = DBAMeasure(MIC_REF_RMS, MIC_REF_DBA)
dbaMA = MovingAverage(8 * 18000, 40)

audioQueue = queue.Queue()
dbaQueue = queue.Queue()

def audioRecordingCallback(indata):
    audioQueue.put(indata.copy())
    # TODO move all loose values to constants
    if audioQueue.qsize() > ( 8 * 5 ): # only keep the last 5 seconds
        audioQueue.get()


def dbaMeasurementCallback(indata):
    dba = dbaMeasure.dbaFromInput(indata.copy())
    dbaQueue.put(dba)


mic.addCallback(audioRecordingCallback)
mic.addCallback(dbaMeasurementCallback)
mic.setup()
mic.start()

fileCounter = 0


def upDateDBaMovingAverage():
    dba = dbaQueue.get()
    dbaMA.addValue(dba)
    return dba


while True:
    dba = upDateDBaMovingAverage()
    #print(str(dba) + "  " + str(dbaMA.getMA()))
    if dba > dbaMA.getMA() + 10:
        print("event " + str(fileCounter) +" fired")
        lastTime = time.time()
        fileName = datetime.datetime.now().replace(microsecond=0).isoformat() + ".wav"
        fileCounter += 1
        with sf.SoundFile(fileName, mode='w', samplerate=48000, format="WAV",
                channels=1, subtype="PCM_16") as file:
            currentTime = lastTime
            while (currentTime - 5) < lastTime:
                if dbaQueue.empty() == False:
                    if upDateDBaMovingAverage() > dbaMA.getMA() + 10:
                        lastTime = time.time()
                file.write(audioQueue.get())
                currentTime = time.time()
    


