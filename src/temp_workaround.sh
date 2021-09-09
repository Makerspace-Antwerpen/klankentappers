#!/bin/bash

set -o errexit

path="$1"/scripts
file="$path"/module.lds.S
output_file="$path"/module.lds
# dest_folder="/usr/src/app/$3"
echo path
echo file
echo output_file
# Workaround if module.lds is not created in last debian versions, copy lds.S and remove the # line at the end
if [ ! -f "$output_file" ]; then
	if [ -f "$file" ]; then
		cp "$file" "$output_file"
		sed -i '/#/d' "$output_file"
	fi
fi