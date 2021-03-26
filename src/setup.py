#!/bin/python3

import sounddevice as sd

print("Welkom in het setupscript van de klankpi")
print("Hieronder ziet u een lijst van de beschikbare audioAparaten:")
print(sd.query_devices())
audioDeviceNumber = input("Geef het nummer in van de device die je wenst te gebruiken:\n")
print("We hebben nu een device. Dit moet nu wel nog gekalibreert worden.")
print("Leg je klankpi in een open ruimte met een zo constant mogelijk geluidsniveau.")
print("Zet een continue geluidsbron op 1m van je klankpi en leg een reeds gecalibreerde geluidsmeter naast je klankpi")
print("Als geluidsbron gebruik je best white noise (te vinden online) afgespeeld op een telefoon of speakers")
dbRefLevel = input("Geef het geluidsniveau in dat je afleest op de reeds gecalibreerde geluidsmeter")
print("Nu gaan we 20 seconden calibreren")