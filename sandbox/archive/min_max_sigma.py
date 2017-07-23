info = gscript.parse_command(
    'r.info',
    map=sigma,
    flags='r')
min_sigma = float(info['min'])
max_sigma = float(info['max'])

# determine regime
if rain >= 60. or max_sigma <= 0.01:
    regime = 'detachment limited'
elif min_sigma >= 100.:
    regime = 'transport limited'
else:
    regime = 'erosion deposition'
