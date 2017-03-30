def transport_limited(self):
    """a small-scale, process-based landscape evolution model
    using simulated transport limited erosion and deposition
    to evolve a digital elevation model"""

    # assign variables
    slope = 'slope'
    aspect = 'aspect'
    dx = 'dx'
    dy = 'dy'
    grow_slope = 'grow_slope'
    grow_aspect = 'grow_aspect'
    grow_dx = 'grow_dx'
    grow_dy = 'grow_dy'
    rain = 'rain'
    erdep = 'erdep' # kg/m^2s
    sedflux = 'flux' # kg/ms
    dxx = 'dxx'
    dyy = 'dyy'
    grow_dxx = 'grow_dxx'
    grow_dyy = 'grow_dyy'
    divergence = 'divergence'
    smoothed_elevation = 'smoothed_elevation'
    settled_elevation = 'settled_elevation'

    # parse time
    year = int(self.start[:4])
    month = int(self.start[5:7])
    day = int(self.start[8:10])
    hours = int(self.start[11:13])
    minutes = int(self.start[14:16])
    seconds = int(self.start[17:19])
    time = datetime.datetime(year, month, day, hours, minutes, seconds)

    # advance time
    time = time + datetime.timedelta(minutes=self.rain_interval)
    time = time.isoformat(" ")

    # timestamp
    evolved_elevation = 'elevation_' + time.replace(" ", "_").replace("-", "_").replace(":", "_") # m
    depth = 'depth_' + time.replace(" ", "_").replace("-", "_").replace(":", "_") # m
    sediment_flux = 'flux_' + time.replace(" ", "_").replace("-", "_").replace(":", "_") # kg/ms
    erosion_deposition = 'erosion_deposition_' + time.replace(" ", "_").replace("-", "_").replace(":", "_") # kg/m2s
    difference = 'difference_' + time.replace(" ", "_").replace("-", "_").replace(":", "_") # m

    # compute slope, aspect, and partial derivatives
    gscript.run_command('r.slope.aspect',
        elevation=self.elevation,
        slope=slope,
        aspect=aspect,
        dx=dx,
        dy=dy,
        overwrite=True)

    # grow border to fix edge effects of moving window computations
    gscript.run_command('r.grow.distance',
        input=slope,
        value=grow_slope,
        overwrite=True)
    slope = grow_slope
    gscript.run_command('r.grow.distance',
        input=aspect,
        value=grow_aspect,
        overwrite=True)
    aspect = grow_aspect
    gscript.run_command('r.grow.distance',
        input=dx,
        value=grow_dx,
        overwrite=True)
    dx = grow_dx
    gscript.run_command('r.grow.distance',
        input=dy,
        value=grow_dy,
        overwrite=True)
    dy = grow_dy

    # hyrdology parameters
    gscript.run_command('r.mapcalc',
        expression="{rain} = {rain_intensity}*{runoff}".format(rain=rain,
            rain_intensity=self.rain_intensity,
            runoff=self.runoff),
        overwrite=True)

    # hydrologic simulation
    gscript.run_command('r.sim.water',
        elevation=self.elevation,
        dx=dx,
        dy=dy,
        rain=rain,
        man=self.mannings,
        depth=depth,
        niterations=self.rain_interval,
        nwalkers=self.walkers,
        overwrite=True)

    # erosion-deposition simulation
    gscript.run_command('r.sim.sediment',
        elevation=self.elevation,
        water_depth=depth,
        dx=dx,
        dy=dy,
        detachment_coeff=self.detachment,
        transport_coeff=self.transport,
        shear_stress=self.shearstress,
        man=self.mannings,
        tlimit_erosion_deposition=erdep,
        niterations=self.rain_interval,
        nwalkers=self.walkers,
        overwrite=True)

    # filter outliers
    gscript.run_command('r.mapcalc',
        expression="{erosion_deposition} = if({erdep}<{erdepmin},{erdepmin},if({erdep}>{erdepmax},{erdepmax},{erdep}))".format(erosion_deposition=erosion_deposition,
            erdep=erdep,
            erdepmin=self.erdepmin,
            erdepmax=self.erdepmax),
        overwrite=True)
    gscript.run_command('r.colors',
        map=erosion_deposition,
        raster=erdep)

    # evolve landscape
    """change in elevation (m) = change in time (s) * net erosion-deposition (kg/m^2s) / sediment mass density (kg/m^3)"""
    gscript.run_command('r.mapcalc',
        expression="{evolved_elevation} = {elevation}-({rain_interval}*60*{erosion_deposition}/{density})".format(evolved_elevation=evolved_elevation,
            elevation=self.elevation,
            rain_interval=self.rain_interval,
            erosion_deposition=erosion_deposition,
            density=self.density),
        overwrite=True)

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

    # compute elevation change
    gscript.run_command('r.mapcalc',
        expression="{difference} = {evolved_elevation}-{elevation}".format(difference=difference,
            elevation=self.elevation,
            evolved_elevation=evolved_elevation),
        overwrite=True)
    gscript.write_command('r.colors',
        map=difference,
        rules='-',
        stdin='-15000 100 0 100\n-100 magenta\n-10 red\n-1 orange\n-0.1 yellow\n0 200 255 200\n0.1 cyan\n1 aqua\n10 blue\n100 0 0 100\n18000 black')

    # remove temporary maps
    gscript.run_command('g.remove',
        type='raster',
        name=['rain',
            'erdep',
            'evolving_elevation',
            'smoothed_elevation',
            'settled_elevation',
            'divergence',
            'dx',
            'dy',
            'dxx',
            'dyy',
            'grow_slope',
            'grow_aspect',
            'grow_dx',
            'grow_dy',
            'grow_dxx',
            'grow_dyy'],
        flags='f')

    return evolved_elevation, time, depth, erosion_deposition, difference
