#!/bin/python3

from lib.mic import Mic
from lib.iir import IIR
import sounddevice as sd

def micSetup():
    a_vals_flat = [1.0, -1.997675693595542, 0.997677044195563]
    b_vals_flat = [1.001240684967527, -1.996936108836337, 0.995703101823006]
    
    iir_l = IIR(a_vals_flat, b_vals_flat)

    mic = Mic(sd)
    mic.addFilter(iir_l)
    return mic