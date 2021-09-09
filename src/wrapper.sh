#!/bin/bash


installed=$( lsmod | grep snd_i2smic_rpi )

if [ "$installed" = "" ]; then
  insmod output/i2s_mic_module_raspberrypi4-64_"$VERSION"/snd-i2smic-rpi.ko rpi_platform_generation=2
fi

python3 recordEvents.py
