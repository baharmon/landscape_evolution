
""" band pass filter """

# assign variables
average_elevation = 'average_elevation'
oscillation = 'oscillation'
sign = 'sign'
averaging_span = 3
attenuation = 0.5
threshold = 0.01
filtered_elevation = 'filtered_elevation' # temporary

# compute average elevation
gscript.run_command('r.neighbors',
    input=evolved_elevation,
    output=average_elevation,
    method='average',
    size=averaging_span,
    overwrite=True)

# compute the difference between the evolved elevation and average elevation
gscript.run_command('r.mapcalc',
    expression="{oscillation} = {evolved_elevation}-{average_elevation}".format(oscillation=oscillation,
        evolved_elevation=evolved_elevation,
        average_elevation=average_elevation),
    overwrite=True)

# determine if the oscillation is positive or negative
gscript.run_command('r.mapcalc',
    expression="{sign} = if({oscillation}>0,1,-1)".format(sign=sign,
        oscillation=oscillation),
    overwrite=True)

# determine if the oscillation is positive or negative
gscript.run_command('r.mapcalc',
    expression="{filtered_elevation} = {average_elevation}+{attenuation}*{oscillation}+(1-{attenuation})*{sign}*threshold".format(filtered_elevation=filtered_elevation,
        average_elevation=average_elevation,
        attenuation=attenuation,
        oscillation=oscillation,
        sign=sign,
        threshold=threshold),
    overwrite=True)

r.mapcalc mod.elev="ave.elev+$8*osc.elev+(1-$8)*osc.sign*$9"
r.mapcalc $1_$2.elev="elin+temp.elev"
