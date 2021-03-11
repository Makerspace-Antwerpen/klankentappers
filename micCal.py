#!/bin/python3

import argparse
import math
import shutil
from scipy import signal

import numpy as np
import sounddevice as sd
from arduinoSer import ArduinoSerDBA
from iir import IIRCombo

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
    # infineon flat vals
    a_vals_flat = [1.0, -1.995669899865592, 0.995674587307386]
    b_vals_flat = [0.998630484460097, -1.988147138656733, 0.989537448149796]
    iirResult = IIRCombo()
    iirResult.addIIR(a_vals_flat, b_vals_flat)
    iirResult.addIIR(a_vals_dba, b_vals_dba)
    return iirResult

def CreateVesperCombo():
    global a_vals_dba
    global b_vals_dba
    # infineon flat vals
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
    # infineon flat vals
    a_vals_flat = [1.0, -1.997837005493052, 0.997838175129360]
    b_vals_flat = [0.985396588196463, -1.963665742774994, 0.978282042869039]

    a_vals_flat_h = [1.0, 6.331743873834744e-02, 6.525859922573027e-04]
    b_vals_flat_h = [0.448130111023087, 0.497537693920992, 0.137624507847601]

    iirResult = IIRCombo()
    iirResult.addIIR(a_vals_flat, b_vals_flat)
    iirResult.addIIR(a_vals_flat_h, b_vals_flat_h)
    iirResult.addIIR(a_vals_dba, b_vals_dba)
    return iirResult


# # these vallues where extracted from https://github.com/ikostoski/esp32-i2s-slm/blob/master/esp32-i2s-slm.ino#L158
# # working on calculations to create better values for IIR filter
# # infineon flat vals
# a_vals_flat = [1.0, -1.997675693595542, 0.997677044195563]
# b_vals_flat = [1.001240684967527, -1.996936108836337, 0.995703101823006]
# # vesper flat vals
# # a_vals_flat = [1.000000000000000, -0.767094031944789, 0.147079000369609]
# # b_vals_flat = [-2.596485872362707e-01, -1.485669912567066e-01, -2.124706303313597e-02]
# iirFlat = IIR(a_vals_flat, b_vals_flat)
# a_vals_dba = [1.0, -2.12979364760736134, 0.42996125885751674, 1.62132698199721426, -0.96669962900852902, 0.00121015844426781, 0.04400300696788968]
# b_vals_dba = [0.169994948147430, 0.280415310498794, -1.120574766348363, 0.131562559965936, 0.974153561246036, -0.282740857326553, -0.152810756202003]
# iirDba = IIR(a_vals_dba, b_vals_dba)

iirFilterCombo = CreateVesperCombo()


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
args = parser.parse_args(remaining)



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
    # infineon callibrate: 0.041609445060915747 at 92 db
    # vesper callibrate: 0.04619286932250245 at 92 db

    # Callibration vallues are created with the micCal.py script
    # stable noise source and callibrated db meter are required
    # inserted vallue is the average rms at a certain noise level
    # this noise level is then added to end result to get db measurement
    # dba = calcDb(rms/0.028116272750016935) + 93 # DB correction factor. Mic specific
    # dba = calcDb(rms/0.004111315776383379) + 70 # DB correction factor. Mic specific
    return rms


rmsList = [0] * 20
duinoList = [0] * 20

try:
    def callback(indata, frames, time, status):
        if status:
            text = ' ' + str(status) + ' '
            print('\x1b[34;40m', text.center(args.columns, '#'),
                  '\x1b[0m', sep='')
        if any(indata):
            flatData = indata.flatten() # input is 2d array. making 1d array from it
            dba = calcDBAfromInput(flatData)
            rmsList.append(dba)
            rmsList.pop(0)
            rmsAv = sum(rmsList)/len(rmsList)
            duinoVal = duino.readSerDBA()
            duinoList.append(duinoVal)
            duinoList.pop(0)
            duinoAv = sum(duinoList)/len(duinoList)
            #if duinoVal > 10:
            print(str(rmsAv) + " " + str(duinoAv))


            

    with sd.InputStream(device=args.device, channels=1, callback=callback,
                        blocksize=6000,
                        samplerate=48000):



        while True:
            response = input()
            if response in ('', 'q', 'Q'):
                break




except KeyboardInterrupt:
    parser.exit('Interrupted by user')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))