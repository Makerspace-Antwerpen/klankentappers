#!/bin/bash

micName=$1
audioName=$2

fullName=$micName"_"$audioName

gnuplot -c plot.gnuplot $fullName".log" $fullName".png"