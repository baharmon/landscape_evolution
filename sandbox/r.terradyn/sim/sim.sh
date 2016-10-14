# SIM (SIMWE Iteration Master) Shell Script
# C.S.Thaxton
echo "SIMWE Iteration Master (SIM) shell script is running"
echo "Written by C.S.Thaxton"

# reset elev, dx, dy files to original topography
r.mapcalc elev.6=elev.6.original

r.mapcalc eldx.6=eldx.6.original

r.mapcalc eldy.6=eldy.6.original

for (( i = 1; i <= $2; i++ ))
do
   sis.sh $1 $i
done
echo "Script $0 is complete."
