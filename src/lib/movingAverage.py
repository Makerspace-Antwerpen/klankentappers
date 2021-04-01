#!/bin/python3

import math

class MovingAverage:
    def __init__(self, size, initValue):
        self.movingAverageList = [initValue] * size

    def addValue(self, value):
        self.movingAverageList.append(value)
        self.movingAverageList.pop(0)

    def getMA(self):
        return sum(self.movingAverageList) / len(self.movingAverageList)

    def getLMA(self):
        div = 20
        deLogSum = 0
        for val in self.movingAverageList:
            deLogSum += math.pow(10, val/div)
        return div * math.log(deLogSum/len(self.movingAverageList), 10)

    def getMAX(self):
        return max(self.movingAverageList)