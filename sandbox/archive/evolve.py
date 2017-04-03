
def smooth_elevation(self):
    """smooth evolved elevation"""

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

def gravitational_diffusion(self):
    """compute settling caused by gravitational diffusion"""

    # compute second order partial derivatives of evolved elevation
    gscript.run_command('r.slope.aspect',
        elevation=evolved_elevation,
        dxx=dxx,
        dyy=dyy,
        overwrite=True)

    # grow border to fix edge effects of moving window computations
    gscript.run_command('r.grow.distance',
        input=dxx,
        value=grow_dxx,
        overwrite=True)
    dxx = grow_dxx
    gscript.run_command('r.grow.distance',
        input=dyy,
        value=grow_dyy,
        overwrite=True)
    dyy = grow_dyy

    # compute divergence
    # from the sum of the second order derivatives of elevation
    gscript.run_command('r.mapcalc',
        expression="{divergence} = {dxx}+{dyy}".format(divergence=divergence,
            dxx=dxx,
            dyy=dyy),
        overwrite=True)

    # compute settling caused by gravitational diffusion
    """change in elevation (m) = elevation (m) - (change in time (s) / sediment mass density (kg/m^3) * gravitational diffusion coefficient (m^2/s) * divergence (m^-1))"""
    gscript.run_command('r.mapcalc',
        expression="{settled_elevation} = {evolved_elevation}-({rain_interval}*60/{density}*{grav_diffusion}*{divergence})".format(settled_elevation=settled_elevation,
            evolved_elevation=evolved_elevation,
            density=self.density,
            grav_diffusion=self.grav_diffusion,
            rain_interval=self.rain_interval,
            divergence=divergence),
        overwrite=True)

    # update elevation
    gscript.run_command('r.mapcalc',
        expression="{evolved_elevation} = {settled_elevation}".format(evolved_elevation=evolved_elevation,
            settled_elevation=settled_elevation),
        overwrite=True)
    gscript.run_command('r.colors',
        map=evolved_elevation,
        color='elevation')

def elevation_change(self):
    """compute elevation change"""

    # compute elevation change
    gscript.run_command('r.mapcalc',
        expression="{difference} = {elevation}-{evolved_elevation}".format(difference=difference, elevation=self.elevation, evolved_elevation=evolved_elevation),
    overwrite=True)
gscript.write_command('r.colors',
    map=difference,
    rules='-',
    stdin='-15000 100 0 100\n-100 magenta\n-10 red\n-1 orange\n-0.1 yellow\n0 200 255 200\n0.1 cyan\n1 aqua\n10 blue\n100 0 0 100\n18000 black')
