#!/bin/python3

from lib.mic import Mic
from lib.iir import IIR
import sounddevice as sd

def micSetup():
    a_vals_flat = [1.0, -1.995669899865592, 0.995674587307386]
    b_vals_flat = [0.998630484460097, -1.988147138656733, 0.989537448149796]
    
    iir_l = IIR(a_vals_flat, b_vals_flat)

    mic = Mic(sd)
    mic.addFilter(iir_l)
    return mic