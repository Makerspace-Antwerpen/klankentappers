#!/bin/python3

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
from micSetup.infineon import micSetup
from lib.tbConnection import TBConnection
from lib.eventRecorder import EventRecorder
from lib.fileWriter import FileWriter
from lib.arduinoSer import ArduinoSerDBA


duino = ArduinoSerDBA(9600,'/dev/ttyACM0')



# parse configfile
config = configparser.ConfigParser()
config.read('klankConfig.ini')
micConfig = config['micConfig']
tbConfig = config['thingsBoardConfig']
eventConfig = config['eventConfig']


#INIT all common vars
MIC_REF_RMS = float(micConfig['rmsRefLevel'])
MIC_REF_DBA = float(micConfig['dbRefLevel'])
INPUT_DEV = int(micConfig['audioDevice'])
MEASURERMENTS_PER_SEC = 8


# INIT all data management objects
mic = micSetup()
mic.setAudioDevice(INPUT_DEV)
dbaMeasure = DBAMeasure(MIC_REF_RMS, MIC_REF_DBA)



def dbCompareCallback(data):
    dba = dbaMeasure.dbaFromInput(data.copy())
    duinoVal = duino.readSerDBA()
    if duinoVal > 30:
        print(str(dba) + " " + str(duinoVal))

mic.addCallback(dbCompareCallback)

try:
    mic.setup()
    mic.start()

    while True:
        response = input()
        if response in ('', 'q', 'Q'):
            mic.stop()
            break


except KeyboardInterrupt:
    mic.stop()
except Exception as e:
    mic.stop()