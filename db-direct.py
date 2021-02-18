#!/bin/python3

"""Show a text-mode spectrogram using live microphone data."""
import argparse
import math
import shutil
from scipy import signal

import numpy as np
import sounddevice as sd

import serial

ser = serial.Serial(
        port='/dev/ttyACM0', \
        baudrate=9600, \
        parity=serial.PARITY_NONE, \
        stopbits=serial.STOPBITS_ONE, \
        bytesize=serial.EIGHTBITS,\
        timeout=0)


usage_line = ' press <enter> to quit, +<enter> or -<enter> to change scaling '


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


try:
    columns, _ = shutil.get_terminal_size()
except AttributeError:
    columns = 10

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__ + '\n\nSupported keys:' + usage_line,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-b', '--block-duration', type=float, metavar='DURATION', default=50,
    help='block size (default %(default)s milliseconds)')
parser.add_argument(
    '-c', '--columns', type=int, default=columns,
    help='width of spectrogram')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-g', '--gain', type=float, default=10,
    help='initial gain factor (default %(default)s)')
parser.add_argument(
    '-r', '--range', type=float, nargs=2,
    metavar=('LOW', 'HIGH'), default=[100, 2000],
    help='frequency range (default %(default)s Hz)')
args = parser.parse_args(remaining)
low, high = args.range
if high <= low:
    parser.error('HIGH must be greater than LOW')

# Create a nice output gradient using ANSI escape sequences.
# Stolen from https://gist.github.com/maurisvh/df919538bcef391bc89f
colors = 30, 34, 35, 91, 93, 97
chars = ' :%#\t#%:'
gradient = []
for bg, fg in zip(colors, colors[1:]):
    for char in chars:
        if char == '\t':
            bg, fg = fg, bg
        else:
            gradient.append('\x1b[{};{}m{}'.format(fg, bg + 10, char))


def calcDb(amp):
    if amp == 0:
        return 0
    db = 20 * math.log(amp/0.00002,10)
    return db


try:
    samplerate = sd.query_devices(args.device, 'input')['default_samplerate']

    delta_f = (high - low) / (args.columns - 1)
    fftsize = math.ceil(samplerate / delta_f)
    low_bin = math.floor(low / delta_f)

    a_vals = [1.0, -1.997675693595542, 0.997677044195563]
    b_vals = [1.001240684967527, -1.996936108836337, 0.995703101823006]

    zi = signal.lfilter_zi(b_vals,a_vals) # still doing something wrong. This should be passed in

    def callback(indata, frames, time, status):


        if status:
            text = ' ' + str(status) + ' '
            print('\x1b[34;40m', text.center(args.columns, '#'),
                  '\x1b[0m', sep='')
        if any(indata):
            outdata = signal.lfilter(b_vals, a_vals, indata)
            rms = np.sqrt(np.mean(outdata**2))
            db = calcDb(rms) + 25
            ser.write(1)
            rawDuino = str(ser.readline())
            split1 = rawDuino.split("'")
            duinoVal = split1[1].split("\\")[0]
            print(str(db) + " " + str(duinoVal) )

        #     magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
        #     magnitude *= args.gain / fftsize
        #     line = (gradient[int(np.clip(x, 0, 1) * (len(gradient) - 1))]
        #             for x in magnitude[low_bin:low_bin + args.columns])
        #     print(*line, sep='', end='\x1b[0m\n')
        # else:
        #     print('no input')

    with sd.InputStream(device=args.device, channels=1, callback=callback,
                        blocksize=6000,
                        samplerate=48000):
        while True:
            response = input()
            if response in ('', 'q', 'Q'):
                break
            for ch in response:
                if ch == '+':
                    args.gain *= 2
                elif ch == '-':
                    args.gain /= 2
                else:
                    print('\x1b[31;40m', usage_line.center(args.columns, '#'),
                          '\x1b[0m', sep='')
                    break
except KeyboardInterrupt:
    parser.exit('Interrupted by user')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))