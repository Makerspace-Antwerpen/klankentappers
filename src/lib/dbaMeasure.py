#!/bin/python3

from lib.iir import IIR
import numpy as np
import math

class DBAMeasure:
    # Callibration vallues are created with the micCal.py script
    # stable noise source and callibrated db meter are required
    # inserted vallue is the average rms at a certain noise level
    # this noise level is then added to end result to get db measurement
    def __init__(self, rmsReference: float, dbaReference: float):
        self.rmsReference = rmsReference
        self.dbaReference = dbaReference
        self.dbaIIRSetup()

    def dbaIIRSetup(self):
        #a and b vals for dba weighting IIR
        a_vals_dba = [1.0, -2.12979364760736134, 0.42996125885751674, 1.62132698199721426, -0.96669962900852902, 0.00121015844426781, 0.04400300696788968]
        b_vals_dba = [0.169994948147430, 0.280415310498794, -1.120574766348363, 0.131562559965936, 0.974153561246036, -0.282740857326553, -0.152810756202003]

        dbaIIR = IIR(a_vals_dba, b_vals_dba)
        self.dbaIIR = dbaIIR

    def calcDb(self, amp):
        if amp == 0:
            return 0
        db = 20 * math.log(amp,10)
        return db

    def dbaFromInput(self, input):
        rms = self.AWeightedRMS(input)
        dba = self.calcDb(rms/self.rmsReference) + self.dbaReference # DB correction factor. Mic specific
        # dba = self.calcDb(rms/0.008324243692980756) + 71.5
        return dba

    def AWeightedRMS(self, input):
        # apply IIR filtering
        weightedInput = self.dbaIIR.applyFilter(input)
        # get rid of any dc shift
        balancedInput = weightedInput - np.mean(weightedInput)
        rms = np.sqrt(np.mean(balancedInput**2))
        return rms

    def getNormalizationFactor(self):
        ex = (120 - self.dbaReference) / 20
        rmsdb = 10**ex * self.rmsReference
        print(rmsdb)
        return 1 / rmsdb