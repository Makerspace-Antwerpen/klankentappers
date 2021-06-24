#!/bin/python3

import math
import rx
import time
import datetime

class StatsGen(rx.core.typing.Observer):
    def __init__(self, tbConnection, morningHour=7,eveningHour=22):
        self.tbConnection = tbConnection
        self.dayTimeData = list()
        self.nightTimeData = list()
        self.morningHour = morningHour
        self.eveningHour = eveningHour
        self.dataProcessed = False

    def processData(self):
        LDay = self.getLogarithmicAverage(self.dayTimeData)
        LNight = self.getLogarithmicAverage(self.nightTimeData)
        
        LDayNight = self.getDayNightAverage(LDay, LNight)
        self.nightTimeData.clear()
        self.dayTimeData.clear()
        self.tbConnection.addTelemetry("LDay", LDay, "stats")
        self.tbConnection.addTelemetry("LNight", LNight, "stats")
        self.tbConnection.addTelemetry("LDayNight", LDayNight)
        self.tbConnection.sendTelemetry("stats")


    def getDayNightAverage(self, LDay, LNight):
        dayTime = self.eveningHour - self.morningHour
        nightTime = 24 - dayTime
        logSumDay = (dayTime/24) * math.pow(10,(LDay/10))
        logSumNight = (nightTime/24) * math.pow(10, ((LNight+10)/10))
        logSumTot = logSumDay + logSumNight
        LDayNight = 10 * math.log(logSumTot,10)
        return LDayNight



    def getLogarithmicAverage(self, inList, weighting=1, shift=0):
        if len(inList) == 0:
            return 0
        div = 10
        deLogSum = 0
        for val in inList:
            deLogSum += math.pow(10, (val + shift)/div)
        return div * math.log(weighting*(deLogSum/len(inList)), 10)
    
    def on_next(self,val):
        dateTime  = datetime.datetime.fromtimestamp(val[2])
        hour = dateTime.hour
        if hour == self.morningHour:
            if not self.dataProcessed:
                self.dataProcessed = True
                self.processData()
        else:
                self.dataProcessed = False
        if hour < self.morningHour or self.eveningHour <= hour:
            self.nightTimeData.append(val[0])
        else:
            self.dayTimeData.append(val[0])
    
    def on_error(self,error):
        print(error)

    def on_completed(self):
        print("statsGen is done.")