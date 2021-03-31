#!/bin/python3

import queue
import time
import datetime
import soundfile as sf
import sounddevice as sd
import numpy as np
import configparser
import config as cf
from lib.dbaMeasure import DBAMeasure
from lib.movingAverage import MovingAverage
from micSetup.adaI2S import micSetup
from lib.tbConnection import TBConnection

config = configparser.ConfigParser()
config.read('klankConfig.ini')
micConfig = config['micConfig']



MIC_REF_RMS = float(micConfig['rmsRefLevel'])
MIC_REF_DBA = float(micConfig['dbRefLevel'])




mic = micSetup()
dbaMeasure = DBAMeasure(MIC_REF_RMS, MIC_REF_DBA)
dbaMA = MovingAverage(8 * 18000, 55)
dbaShortMA = MovingAverage(8 * 300, 55)
dbaVeryShortMA = MovingAverage(8 * 5, 55)
tb = TBConnection("tb.wouterpeetermans.com", 1883, cf.tb_secret)


audioQueue = queue.Queue()
dbaQueue = queue.Queue()

def audioRecordingCallback(indata):
    audioQueue.put(indata.copy())
    # TODO move all loose values to constants
    if audioQueue.qsize() > ( 8 * 1 ): # only keep the last 5 seconds
        audioQueue.get()


def dbaMeasurementCallback(indata):
    dba = dbaMeasure.dbaFromInput(indata.copy())
    dbaQueue.put(dba)


mic.addCallback(audioRecordingCallback)
mic.addCallback(dbaMeasurementCallback)
mic.setup()
mic.start()

fileCounter = 0

lastTBtime = 0

def upDateDBaMovingAverage():
    global lastTBtime
    dba = dbaQueue.get()
    dbaMA.addValue(dba)
    dbaShortMA.addValue(dba)
    dbaVeryShortMA.addValue(dba)
    if (lastTBtime + 5) < time.time():
        updateTB()
        lastTBtime = time.time()
    return dba

def updateTB():
    tb.addTelemetry("longDbaMA", dbaMA.getMA())
    tb.addTelemetry("shortDbaMA", dbaShortMA.getMA())
    tb.addTelemetry("veryShortDbaMA", dbaVeryShortMA.getMA())
    tb.sendTelemetry()


while True:
    dba = upDateDBaMovingAverage()
    print(str(dba) + "  " + str(dbaMA.getMA()))
    if dba > dbaMA.getMA() + 10:
        print("event " + str(fileCounter) +" fired")
        lastTime = time.time()
        fileName = "/mnt/harddisk/" + datetime.datetime.now().replace(microsecond=0).isoformat() + ".wav"
        fileCounter += 1
        with sf.SoundFile(fileName, mode='w', samplerate=48000, format="WAV",
                channels=1, subtype="PCM_16") as file:
            currentTime = lastTime
            while (currentTime - 1) < lastTime:
                if dbaQueue.empty() == False:
                    if upDateDBaMovingAverage() > dbaMA.getMA() + 10:
                        lastTime = time.time()
                file.write(audioQueue.get())
                currentTime = time.time()
    


