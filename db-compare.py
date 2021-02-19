#!/bin/python3

import argparse
import math
import shutil
from scipy import signal

import numpy as np
import sounddevice as sd
from arduinoSer import ArduinoSerDBA
from iir import IIR

duino = ArduinoSerDBA(9600,'/dev/ttyACM0')

# these vallues where extracted from https://github.com/ikostoski/esp32-i2s-slm/blob/master/esp32-i2s-slm.ino#L158
# working on calculations to create better values for IIR filter
a_vals = [1.0, -1.997675693595542, 0.997677044195563]
b_vals = [1.001240684967527, -1.996936108836337, 0.995703101823006]
iir = IIR(a_vals, b_vals)


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
    # apply flattening
    weightedInput = iir.applyIIR(input)
    # get rid of any dc shift
    balancedInput = weightedInput - np.mean(weightedInput)
    rms = np.sqrt(np.mean(balancedInput**2))
    # infineon callibrate: 0.041609445060915747 at 92 db
    # vesper callibrate: 0.04619286932250245 at 92 db

    # Callibration vallues are created with the micCal.py script
    # stable noise source and callibrated db meter are required
    # inserted vallue is the average rms at a certain noise level
    # this noise level is then added to end result to get db measurement
    dba = calcDb(rms/0.041609445060915747) + 92 # DB correction factor. Mic specific
    return dba


try:
    def callback(indata, frames, time, status):
        if status:
            text = ' ' + str(status) + ' '
            print('\x1b[34;40m', text.center(args.columns, '#'),
                  '\x1b[0m', sep='')
        if any(indata):
            flatData = indata.flatten() # input is 2d array. making 1d array from it
            dba = calcDBAfromInput(flatData)
            duinoVal = duino.readSerDBA()
            print(str(dba) + " " + str(duinoVal+2))


            

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