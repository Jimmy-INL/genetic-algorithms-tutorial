#!/usr/bin/gnuplot -persist

set terminal png
set output "styb-tang-map.png"
set xlabel "x_1" font ",10"
set ylabel "x_2" font ",10"
set pm3d map
set isosamples 2000
unset key
set xtics -5, 5, 5 font ",8"
set ytics -5, 5, 5 font ",8"
set xrange [-5:5]
set yrange [-5:5]
set autoscale xfix
set autoscale yfix
splot 0.5 * ((x**4 - 16*(x**2) + 5*x) + (y**4 - 16*(y**2) + 5*y))
