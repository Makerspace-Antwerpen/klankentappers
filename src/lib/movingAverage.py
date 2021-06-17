#!/bin/python3

import math
import rx

class MovingAverage(rx.core.typing.Observer):
    def __init__(self, size):
        self.movingAverageList = list()
        self.size = size
        self.initCounter = 0

    def addValue(self, value):
        if self.initCounter < 10:
            self.initCounter += 1
            return
        self.movingAverageList.append(value)
        if self.size <= len(self.movingAverageList):
            self.movingAverageList.pop(0)

    def getMA(self):
        if len(self.movingAverageList) == 0:
            return 0
        return sum(self.movingAverageList) / len(self.movingAverageList)

    def getLMA(self):
        if len(self.movingAverageList) == 0:
            return 0
        div = 10
        deLogSum = 0
        for val in self.movingAverageList:
            deLogSum += math.pow(10, val/div)
        return div * math.log(deLogSum/len(self.movingAverageList), 10)

    def getMAX(self):
        if len(self.movingAverageList) == 0:
            return 0
        return max(self.movingAverageList)
    
    def on_next(self,val):
        self.addValue(val[0])
    
    def on_error(self,error):
        print(error)

    def on_completed(self):
        print("movingaverage is done.")