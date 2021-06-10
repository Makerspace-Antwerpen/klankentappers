#!/bin/bash

OS_VERSION=$(echo "$BALENA_HOST_OS_VERSION" | cut -d " " -f 2)
echo "OS Version is $OS_VERSION"

cd output
mod_dir="i2s_mic_module_${BALENA_DEVICE_TYPE}_${OS_VERSION}*"
for each in $mod_dir; do
	echo Loading module from "$each"
	insmod "$each/snd-i2smic-rpi.ko" rpi_platform_generation=2
	lsmod | grep sndi2smic-rpi
	#rmmod sndi2smic-rpi
done

while true; do
	sleep 60
done

