#!/bin/bash

installed=$(lsmod | grep snd_i2smic_rpi)
RES_VERSION=None
for i in $VERSION; do
  echo $i
  for j in $RESIN_HOST_OS_VERSION; do
    # we want to compare the entries in this list with the RESIN_HOST_OS_VERSION env variable
    if [[ $i == *$j* ]]; then
      echo "It's there!" $i $j
      RES_VERSION=$i
    fi
  done
done

if [ "$installed" = "" ]; then
  insmod output/i2s_mic_module_raspberrypi4-64_"$RES_VERSION"/snd-i2smic-rpi.ko rpi_platform_generation=2
fi

python3 recordEvents.py