#!/bin/python3

import serial

class ArduinoSerDBA():
    def __init__(self, baud, port):
        self.ser = serial.Serial(
        port=port, \
        baudrate=baud, \
        parity=serial.PARITY_NONE, \
        stopbits=serial.STOPBITS_ONE, \
        bytesize=serial.EIGHTBITS,\
        timeout=0)

    def readSerDBA(self):
        self.ser.write(1)
        rawDuino = str(self.ser.readline())
        split1 = rawDuino.split("'")
        duinoVal = split1[1].split("\\")[0]
        return duinoVal

