# smooth evolved elevation
gscript.run_command('r.neighbors',
    input=evolved_elevation,
    output=smoothed_elevation,
    method='average',
    size=self.smoothing,
    overwrite=True)
# update elevation
gscript.run_command('r.mapcalc',
    expression="{evolved_elevation} = {smoothed_elevation}".format(evolved_elevation=evolved_elevation,
        smoothed_elevation=smoothed_elevation),
    overwrite=True)
