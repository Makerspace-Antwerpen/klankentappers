#!/bin/bash


micName=$1
audioName=$2

./db-compare.py -d 1 > $micName"_"$audioName".log"

