# DBA measurement on raspberry pi with an i2s mic

## structure of the repo
Previous test results go in the logs directory. Testcode goes in the scratchpad directory

In the main directory there is several python scripts which are explained further down this document. There's also a .gnuplot file to generate graphs from the collected data.


## Basic PI setup
### connections between i2s and pi
- Mic 3V to PI 3.3V
- Mic GND to PI GND
- Mic SEL to PI GND
- Mic BCLK to BCM 18 (pin 12)
- Mic DOUT to BCM 20 (pin 38)
- Mic LRCL to BCM 19 (pin 35)

### Basic setup pi
starting from basic raspberry PI OS

```
sudo apt update && apt upgrade
sudo apt install python3-pip
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2smic.py
sudo python3 i2smic.py
```


You can test wether the mic is working with:
```bash
# to list mic's available
arecord -l

# to record a wav file of 1 second
arecord -D plughw:0 -c1 -d 1 -r 48000 -f S32_LE -t wav -V mono -v output.wav
# -D plughw:0 --> soundcard 0 selecteren
# -c1 --> er is maar 1 channel
# -d n --> zorgt ervoor dat er slechts n seconden worden opgenomen. Kan worden weggelaten
# -r n --> sample rate
# -f x --> sample format zie man page arecord
# -t wav --> output type wav
# -V mono --> VU-meter mono
# -v verbose --> meer info voor debug
```
## python scripts
There is a collection of python scripts in the main folder of the repo:
1. db-compare.py: compare readings from the raspberry pi with the readings from the arduino
2. iir.py: class that implements an IIR filter
3. arduinoSer.py: class that sets up communication with the arduino
4. micCal.py: script that put's out the rms value of the mic together with the db vallue coming from the arduino. This can be used to get the calibration vallues for the db-compare script. 
