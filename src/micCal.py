#!/bin/python3

import queue
import time
import datetime
import soundfile as sf
import sounddevice as sd
import numpy as np
from iir import IIR
from mic import Mic
from dbaMeasure import DBAMeasure
from movingAverage import MovingAverage

MIC_REF_RMS = 0.008324243692980756
MIC_REF_DBA = 71.5




def micSetup():
    # vesper mic is in here for the moment. It was the one connected :)

    a_vals_flat = [1.0, -1.989554495584846, 0.989581772725467]
    b_vals_flat = [1.000576573984365, -1.981768145853667, 0.981285462311266]

    iir_l = IIR(a_vals_flat, b_vals_flat)

    a_vals_flat_h = [1.0, -4.294918477771842e-01, 4.611094235875732e-02]
    b_vals_flat_h = [-2.798094157962595e-01, -2.666742140153097e-01, -6.353734919454769e-02]

    iir_h = IIR(a_vals_flat_h, b_vals_flat_h)

    mic = Mic(sd)
    mic.addFilter(iir_l)
    mic.addFilter(iir_h)
    return mic

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
                channels=1, subtype="PCM_24") as file:
            currentTime = lastTime
            while (currentTime - 5) < lastTime:
                if dbaQueue.empty() == False:
                    if upDateDBaMovingAverage() > dbaMA.getMA() + 10:
                        lastTime = time.time()
                file.write(audioQueue.get())
                currentTime = time.time()
    

