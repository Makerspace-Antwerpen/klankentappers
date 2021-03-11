#!/bin/python3

import argparse
import math
import shutil
from scipy import signal

import numpy as np
import sounddevice as sd
from arduinoSer import ArduinoSerDBA
from iir import IIRCombo
from mic import Mic

mic = Mic(sd)



duino = ArduinoSerDBA(9600,'/dev/ttyACM0')

a_vals_dba = [1.0, -2.12979364760736134, 0.42996125885751674, 1.62132698199721426, -0.96669962900852902, 0.00121015844426781, 0.04400300696788968]
b_vals_dba = [0.169994948147430, 0.280415310498794, -1.120574766348363, 0.131562559965936, 0.974153561246036, -0.282740857326553, -0.152810756202003]


def CreateInfineonCombo():
    global a_vals_dba
    global b_vals_dba
    # infineon flat vals
    a_vals_flat = [1.0, -1.997675693595542, 0.997677044195563]
    b_vals_flat = [1.001240684967527, -1.996936108836337, 0.995703101823006]
    iirResult = IIRCombo()
    iirResult.addIIR(a_vals_flat, b_vals_flat)
    iirResult.addIIR(a_vals_dba, b_vals_dba)
    return iirResult

def CreateAdaI2SCombo():
    global a_vals_dba
    global b_vals_dba
    # adaI2S flat vals
    a_vals_flat = [1.0, -1.995669899865592, 0.995674587307386]
    b_vals_flat = [0.998630484460097, -1.988147138656733, 0.989537448149796]
    iirResult = IIRCombo()
    iirResult.addIIR(a_vals_flat, b_vals_flat)
    iirResult.addIIR(a_vals_dba, b_vals_dba)
    return iirResult

def CreateVesperCombo():
    global a_vals_dba
    global b_vals_dba
    # vesper flat vals
    a_vals_flat = [1.0, -1.989554495584846, 0.989581772725467]
    b_vals_flat = [1.000576573984365, -1.981768145853667, 0.981285462311266]

    a_vals_flat_h = [1.0, -4.294918477771842e-01, 4.611094235875732e-02]
    b_vals_flat_h = [-2.798094157962595e-01, -2.666742140153097e-01, -6.353734919454769e-02]

    iirResult = IIRCombo()
    iirResult.addIIR(a_vals_flat, b_vals_flat)
    iirResult.addIIR(a_vals_flat_h, b_vals_flat_h)
    iirResult.addIIR(a_vals_dba, b_vals_dba)
    return iirResult

def CreateAdaPDMCombo():
    global a_vals_dba
    global b_vals_dba
    # adaPDM flat vals
    a_vals_flat = [1.0, -1.997837005493052, 0.997838175129360]
    b_vals_flat = [0.985396588196463, -1.963665742774994, 0.978282042869039]

    a_vals_flat_h = [1.0, 6.331743873834744e-02, 6.525859922573027e-04]
    b_vals_flat_h = [0.448130111023087, 0.497537693920992, 0.137624507847601]

    iirResult = IIRCombo()
    iirResult.addIIR(a_vals_flat, b_vals_flat)
    iirResult.addIIR(a_vals_flat_h, b_vals_flat_h)
    iirResult.addIIR(a_vals_dba, b_vals_dba)
    return iirResult


iirFilterCombo = CreateVesperCombo()



def calcDb(amp):
    if amp == 0:
        return 0
    db = 20 * math.log(amp,10)
    return db


def calcDBAfromInput(input):
    # apply IIR filtering
    weightedInput = iirFilterCombo.applyIIR(input)
    # get rid of any dc shift
    balancedInput = weightedInput - np.mean(weightedInput)
    rms = np.sqrt(np.mean(balancedInput**2))
    # Callibration vallues are created with the micCal.py script
    # stable noise source and callibrated db meter are required
    # inserted vallue is the average rms at a certain noise level
    # this noise level is then added to end result to get db measurement
    dba = calcDb(rms/0.008324243692980756) + 71.5 # DB correction factor. Mic specific
    return dba

def dbCompareCallback(data):
    dba = calcDBAfromInput(data)
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