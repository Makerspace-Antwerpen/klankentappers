#!/bin/python3

#import sys

#def hello(var):
#  print(var)

#data = sys.stdin.read()
#hello(data)


import fileinput
import math



def freqBinToOct(freqBin):
    total = 0
    for freq in freqBin:
        freq *= 100000
        total += (freq**2)
    power = math.sqrt( total )
    db = 20 * math.log(power/20000000)
    return db

freqList = [ 11.2 , 14.1 , 17.8 , 22.4 , 28.2 , 35.5 , 44.7 , 56.2 , 70.8 , 89.1 , 112 , 141 , 178 ,
        224 , 282 , 355 , 447 , 562 , 708 , 891 , 1122 , 1413 , 1778 , 2239 , 2818 , 3548 ,
        4467 , 5623 , 7079 , 8913 , 11220 , 14130 , 17780 , 22390 ]
stepCount = 0;
nextOctaveList = list()
nextFreqBin = list()

with fileinput.input() as f_input:
    for line in f_input:
        dataEntry = line.split(" ")
        if dataEntry[0] != "":
            if len(dataEntry) == 3:
                freq = float(dataEntry[0])
                val = float(dataEntry[2])
                #print(freq)
                
                if freq < freqList[stepCount]:
                    nextFreqBin.append(val);
                else:
                    #print(nextFreqBin)
                    nextOctaveList.append(freqBinToOct(nextFreqBin))
                    nextFreqBin.clear()
                    stepCount += 1

                if stepCount > 33 or freq == 0:
                    print(nextOctaveList)
                    nextOctaveList.clear()
                    stepCount = 0
                #print(len(dataEntry))
                #print(dataEntry[0] + " " + dataEntry[2])

