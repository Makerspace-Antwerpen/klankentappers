# Klankentappers Software

Voor de PoC workshop werd de software voorbereid als een docker image via Balena Cloud. Dit laat ons toe om "over the air" software updates naar de Raspebrry Pi's te sturen. De SD kaarten werden reeds voorbereid met de juiste image, voorzien van de WiFi gegevens in de makerspace, en de juiste tokens om data naar Thingsboard te sturen.

## Balena
This repo is structured to work with balena cloud. You can run the recordEvents.py script without balena but you'll need to provide the neccesary environment variables manualy in the shell where you run it.
### Environment
The project needs following ENV variables to run correctly:
- AI_SAMPLE_DIR --> This is the folder where audio samples are stored.
- EVENT_START_THRESHOLD_DB --> This is the amount the sound level can rise above the nominal before a event is stored in the ai sample directory.
- EVENT_END_THRESHOLD --> This is the amount above the nominal sound level at which an event is ended.
- EVENT_PADDING_TIME --> This is the amount of time that is added on the end en beginning of each audio sample.
- MIC_AUDIODEVICE --> This is the audiodevice to do the recording with. 1 for the i2s mic.
- MIC_REF_DBA --> This is the sound level in dBa for which a reference RMS level is given.
- MIC_REF_RMS --> This is the RMS level of the mic at the given dBa sound level. This value can be aquired with the setup.py script in the src directory
- TB_INTERVAL_TIME --> This is the interval between thingsboard updates.
- TB_SERVER --> This is the thingsboard server to connect with.
- TB_SECRET --> This is the access token to use for connecting to the thingsboard server.


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
sudo apt install python3-pip libsndfile1 libportaudio2 libatlas-base-dev
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2smic.py
sudo python3 i2smic.py
pip3 install numpy soundfile sounddevice scipy
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
Don't forget to set the environment variables before running the scripts. the db-compare.py and setup.py scripts are made to run on a regular py and only need/generate a config file. The recordEvents.py script is made to run on a balena pi and needs the environment variables to be setup.

### Balena pi
This service exists of 2 containers managed by a docker compose. The wifi connect container is the default of balena. The meter container runs the actual sound meter.
Wifi container is a submodule so it might be needed to download it seperatly.

## python scripts
In the src/ folder there are several scripts. The recordEvents.py records events that happen around the sensor. Event sensitivity can be set with the env vars. The mic section of the env vars can be generated with thes setup.py script. 

