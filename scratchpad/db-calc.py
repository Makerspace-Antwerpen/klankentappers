#!/bin/python3
import math

def calcRa(freq):
    ra = (148693636 * freq**4)/((freq**2 + 424.36) * math.sqrt((freq**2 + 11599.29)*(freq**2 + 544496.41)) * (freq**2 + 148693636))
    return ra

def dbaWeight(freq):
    ra = calcRa(freq)
    a = (20 * math.log(ra,10)) + 2 #- ( 20 * math.log(calcRa(1000),10))
    return a
    
def calcDb(amp):
    if amp == 0:
        return 0
    db = 20 * math.log(amp/0.00002,10)
    return db

def dBaPlot(freqList):
    for freq in freqList:
        print(str(freq) + " " + str(dbaWeight(freq)))

freqList = list()
for x in range(10,20000,10):
    freqList.append(x)

dBaPlot(freqList)