#!/bin/python3

#import sys

#def hello(var):
#  print(var)

#data = sys.stdin.read()
#hello(data)


import fileinput
import math

class DFTPair:
    def __init__(self, freq, amp):
        self.freq = freq
        self.amp = amp


def calcRa(freq):
    ra = (148693636 * freq**4)/((freq**2 + 424.36) * math.sqrt((freq**2 + 11599.29)*(freq**2 + 544496.41)) * (freq**2 + 148693636))
    return ra;

def dbaWeight(freq):
    ra = calcRa(freq)
    a = (20 * math.log(ra,10)) + 2 #- ( 20 * math.log(calcRa(1000),10))
    return a;
    
def calcDb(amp):
    if amp == 0:
        return 0
    db = 20 * math.log(amp/0.00002,10)
    return db


def freqBinToOct(freqBin): #needs mod to take in amplitude correction.
    total = 0
    for freq in freqBin:
        freq *= 100000
        total += (freq**2)
    power = math.sqrt( total )
    db = 20 * math.log(power/20000000,10)
    return db

def calcDBaFromDFT(dft):
    subtotal = 0
    for dftPair in dft:
        if dftPair.freq == 0:
            continue
        db = calcDb(dftPair.amp)
        weight = dbaWeight(dftPair.freq)
        #print("freq: " + str(dftPair.freq) + " weight: " + str(weight))
        weightedDb = db + weight
        if weightedDb < 0:
            weightedDb = 0
        subtotal += (weightedDb/10)**10
    if subtotal == 0: # it's ugly I know. 
        subtotal = 1
    #print("subtotal: " + str(subtotal))
    return math.log(subtotal,10)*10;

freqList = [ 11.2 , 14.1 , 17.8 , 22.4 , 28.2 , 35.5 , 44.7 , 56.2 , 70.8 , 89.1 , 112 , 141 , 178 ,
        224 , 282 , 355 , 447 , 562 , 708 , 891 , 1122 , 1413 , 1778 , 2239 , 2818 , 3548 ,
        4467 , 5623 , 7079 , 8913 , 11220 , 14130 , 17780 , 22390 ]
stepCount = 0;
nextOctaveList = list()
nextFreqBin = list()
nextDFT = list()


with fileinput.input() as f_input:
    for line in f_input:
        dataEntry = line.split(" ")
        if dataEntry[0] != "":
            if len(dataEntry) == 3:
                freq = float(dataEntry[0])
                amp = float(dataEntry[2])
                #print(freq)
                nextDFT.append(DFTPair(freq, amp))
                
                if freq < freqList[stepCount]:
                    nextFreqBin.append(amp);
                else:
                    #print(nextFreqBin)
                    nextOctaveList.append(freqBinToOct(nextFreqBin))
                    nextFreqBin.clear()
                    stepCount += 1

                if stepCount > 33 or freq == 0:
                    db = calcDBaFromDFT(nextDFT)
                    print(db)
                    nextDFT.clear()
                    #print(nextOctaveList)
                    nextOctaveList.clear()
                    stepCount = 0
                #print(len(dataEntry))
                #print(dataEntry[0] + " " + dataEntry[2])

