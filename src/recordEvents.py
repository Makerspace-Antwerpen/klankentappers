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

#INIT all common vars
# TODO: let all vars come from config file
MIC_REF_RMS = float(micConfig['rmsRefLevel'])
MIC_REF_DBA = float(micConfig['dbRefLevel'])

TB_INTERVAL_TIME = 5
START_DBA = 55
MEASURERMENTS_PER_SEC = 8
EVENT_PADDING_TIME = 1
EVENT_TRESHOLD_DB = 10
AI_SAMPLE_DIR = "/mnt/harddisk"



# INIT all objects used to manage data
mic = micSetup()
dbaMeasure = DBAMeasure(MIC_REF_RMS, MIC_REF_DBA)
dbaMA = MovingAverage(MEASURERMENTS_PER_SEC * 1800, START_DBA)
dbaShortMA = MovingAverage(MEASURERMENTS_PER_SEC * 300, START_DBA)
dbaVeryShortMA = MovingAverage(MEASURERMENTS_PER_SEC * 5, START_DBA)
tb = TBConnection("tb.wouterpeetermans.com", 1883, cf.tb_secret)


audioQueue = queue.Queue() #holds audio for set time to drop in audio recording
dbaQueue = queue.Queue() #dba measurement fastlane
dbaHistoryQueue = queue.Queue() #holds dba measurements for set time to drop in meta file

# callbacks for use by mic

def audioRecordingCallback(indata):
    audioQueue.put(indata.copy())
    if audioQueue.qsize() > ( MEASURERMENTS_PER_SEC * EVENT_PADDING_TIME ):
        audioQueue.get()


def dbaMeasurementCallback(indata):
    dba = dbaMeasure.dbaFromInput(indata.copy())
    dbaQueue.put(dba)
    dbaHistoryQueue.put(dba)
    if dbaHistoryQueue.qsize() > ( MEASURERMENTS_PER_SEC * EVENT_PADDING_TIME ):
        dbaHistoryQueue.get()


mic.addCallback(audioRecordingCallback)
mic.addCallback(dbaMeasurementCallback)
mic.setup()
mic.start()


def upDateDBaMovingAverage(dba):
    dbaMA.addValue(dba)
    dbaShortMA.addValue(dba)
    dbaVeryShortMA.addValue(dba)
    return dba

def updateTB():
    tb.addTelemetry("longDbaMA", dbaMA.getMA())
    tb.addTelemetry("shortDbaMA", dbaShortMA.getMA())
    tb.addTelemetry("veryShortDbaMA", dbaVeryShortMA.getMA())
    tb.addTelemetry("longDbaLMA", dbaMA.getLMA())
    tb.addTelemetry("shortDbaLMA", dbaShortMA.getLMA())
    tb.addTelemetry("veryShortDbaLMA", dbaVeryShortMA.getLMA())
    tb.addTelemetry("veryShortDbaMAX", dbaVeryShortMA.getMAX())
    tb.sendTelemetry()



lastTBTime = time.time() + 10 # add extra time so sensor get's time to calibrate
dba = START_DBA
lastSoundAboveTresholdTime = time.time()
eventBusy = False
audioFile = None
metaFile = None
eventDbaList = list()

while True:
    if dbaQueue.empty() == False:
        dba = dbaQueue.get()
        upDateDBaMovingAverage(dba)
    
    if (lastTBTime + TB_INTERVAL_TIME) < time.time():
        updateTB()
        lastTBTime = time.time()

    if dba > (dbaMA.getLMA() + EVENT_TRESHOLD_DB):
        lastSoundAboveTresholdTime = time.time()
        if not eventBusy:
            fileName = AI_SAMPLE_DIR + "/" + datetime.datetime.now().astimezone().replace(microsecond=0).isoformat() + ".wav"
            audioFile = sf.SoundFile(fileName, mode='w', samplerate=48000, format="WAV", channels=1, subtype="PCM_16")
            metaFile = open(AI_SAMPLE_DIR + "/" + datetime.datetime.now().astimezone().replace(microsecond=0).isoformat() + ".meta", "wt")
            eventBusy = True

    if (lastSoundAboveTresholdTime + EVENT_PADDING_TIME) < time.time() and eventBusy:
        eventBusy = False
        audioFile.close()
        audioFile = None
        metaFile.close()
        metaFile = None

    
    if eventBusy:
        audioFile.write(audioQueue.get())
        metaFile.write(str(dbaHistoryQueue.get()) + "\n")

    


