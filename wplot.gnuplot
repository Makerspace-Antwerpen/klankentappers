set terminal png
#set logscale y
#set logscale x
set output "outputCompare-low.png"
plot [40:] "logbestand.txt" ,x # with lp

