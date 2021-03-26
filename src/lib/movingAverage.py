#!/bin/python3

class MovingAverage:
    def __init__(self, size, initValue):
        self.movingAverageList = [initValue] * size

    def addValue(self, value):
        self.movingAverageList.append(value)
        self.movingAverageList.pop(0)

    def getMA(self):
        return sum(self.movingAverageList) / len(self.movingAverageList)