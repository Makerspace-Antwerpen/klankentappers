# Usage: gnuplot -c plot.gnuplot datafile.log output.png

DATAFILE = ARG1
PNGFILE = ARG2

set terminal png
set output PNGFILE

set xlabel "Referentie dbA"
set ylabel "Berekening dbA"
set key title DATAFILE

plot [0:120][0:120] DATAFILE u 2:1 notitle, x
