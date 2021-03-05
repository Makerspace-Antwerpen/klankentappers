import sys
import math

if len(sys.argv) < 2:
    print( "usage: " + sys.argv[ 0 ] + " logfile.log" )
    sys.exit()

mse = 0.0
n = 0

with open( sys.argv[ 1 ], 'r' ) as f:
    for line in f:
        fields = line.split()

        computed_db = float( fields[ 0 ] )
        measured_db = float( fields[ 1 ] )

        mse += ( computed_db - measured_db ) * ( computed_db - measured_db )
        n += 1

mse = mse / n
rmse = math.sqrt( mse )
print( rmse )
