# assign variables
echo " "
echo "*** Applying band-pass filter"
echo " "
echo "--span of averaging   = $7"
echo "--alpha(attentuation) = $8"
echo "--sigma(threshold)    = $9"
#
r.neighbors input=temp.elev output=ave.elev method=average size=$7
r.mapcalc osc.elev="temp.elev-ave.elev"
r.mapcalc osc.sign="if(osc.elev>0,1,-1)"
r.mapcalc mod.elev="ave.elev+$8*osc.elev+(1-$8)*osc.sign*$9"
echo " "
echo "*** Computing change in elevation..."
echo " "
r.mapcalc $1_$2.elev="elin+temp.elev"


# compute average elevation
gscript.run_command('r.neighbors',
    input=evolved_elevation,
    output=smoothed_elevation,
    method='average',
    size=3,
    overwrite=True)

#
gscript.run_command('r.mapcalc',
    expression="{} = {evolved_elevation}-{smoothed_elevation}".format(),
    overwrite=True)
