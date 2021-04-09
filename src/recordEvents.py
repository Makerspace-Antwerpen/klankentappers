#!/bin/python3

import queue
import rx
from rx import operators as ops
import time
import datetime
import soundfile as sf
import sounddevice as sd
import numpy as np
import configparser
from lib.dbaMeasure import DBAMeasure
from lib.movingAverage import MovingAverage
from micSetup.adaI2S import micSetup
from lib.tbConnection import TBConnection
from lib.eventRecorder import EventRecorder
from lib.fileWriter import FileWriter

# parse configfile
config = configparser.ConfigParser()
config.read('klankConfig.ini')
micConfig = config['micConfig']
tbConfig = config['thingsBoardConfig']
eventConfig = config['eventConfig']


#INIT all common vars
# TODO: let all vars come from config file
MIC_REF_RMS = float(micConfig['rmsRefLevel'])
MIC_REF_DBA = float(micConfig['dbRefLevel'])

TB_INTERVAL_TIME = int(tbConfig['intervalTime'])
MEASURERMENTS_PER_SEC = 8
EVENT_PADDING_TIME = int(eventConfig['padding'])
EVENT_START_THRESHOLD_DB = int(eventConfig['startDB'])
EVENT_END_THRESHOLD = int(eventConfig['endDB'])
AI_SAMPLE_DIR = eventConfig['sampleDir']



# INIT all objects used to manage data
mic = micSetup()
dbaMeasure = DBAMeasure(MIC_REF_RMS, MIC_REF_DBA)
dbaMA = MovingAverage(MEASURERMENTS_PER_SEC * 1800)
dbaShortMA = MovingAverage(MEASURERMENTS_PER_SEC * 300)
dbaVeryShortMA = MovingAverage(MEASURERMENTS_PER_SEC * 5)
tb = TBConnection(TB_INTERVAL_TIME, "tb.wouterpeetermans.com", 1883, tbConfig['secret'])

# set up dataSubject and schedulers
defaultScheduler = rx.scheduler.EventLoopScheduler()
detectionScheduler = rx.scheduler.EventLoopScheduler()
recordingScheduler = rx.scheduler.EventLoopScheduler()
audioDataSubject = rx.subject.ReplaySubject(buffer_size = 8 * EVENT_PADDING_TIME , scheduler=defaultScheduler)




# callbacks for use by mic
def dataCallback(indata):
    dba = dbaMeasure.dbaFromInput(indata.copy())
    audioDataSubject.on_next(tuple((dba, indata.copy(), time.time())))
    


mic.addCallback(dataCallback)
mic.setup()
mic.start()


def updateTB(Any):
    tb.addTelemetry("longDbaMA", dbaMA.getMA())
    tb.addTelemetry("shortDbaMA", dbaShortMA.getMA())
    tb.addTelemetry("veryShortDbaMA", dbaVeryShortMA.getMA())
    tb.addTelemetry("longDbaLMA", dbaMA.getLMA())
    tb.addTelemetry("shortDbaLMA", dbaShortMA.getLMA())
    tb.addTelemetry("veryShortDbaLMA", dbaVeryShortMA.getLMA())
    tb.addTelemetry("veryShortDbaMAX", dbaVeryShortMA.getMAX())

def createFileWriter():
    return FileWriter(AI_SAMPLE_DIR, datetime, 4800, audioDataSubject, recordingScheduler)

def eventDetector(val, eventBusy):
    if val[0] > dbaMA.getLMA() + EVENT_START_THRESHOLD_DB:
        return True
    elif eventBusy and val[0] > dbaMA.getLMA() + EVENT_END_THRESHOLD:
        return True
    else:
        return False

eventRecorder = EventRecorder(eventDetector,EVENT_PADDING_TIME , createFileWriter)

# TODO get MA's somewhere in stream instead of sideefects
audioDataSubject.subscribe(dbaMA)
audioDataSubject.subscribe(dbaVeryShortMA)
audioDataSubject.subscribe(dbaShortMA)
audioDataSubject.subscribe(eventRecorder, scheduler=detectionScheduler)
audioDataSubject.subscribe(
    on_next=updateTB
)

tb.startTelemetry()



while True:
    time.sleep(1)
    continue


