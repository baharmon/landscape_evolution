def rusle2d(self):
    """a detachment limited landscape evolution model
    using an experimental 2-dimensional form of the
    RUSLE (Revised Universal Soil Loss Equation) model
    to evolve a digital elevation model"""

    # assign variables
    rain_energy = 'rain_energy'
    rain_volume = 'rain_volume'
    erosivity = 'erosivity'
    r_factor = 'r_factor'
    ls_factor = 'ls_factor'
    slope = 'slope'
    aspect = 'aspect'
    qsx = 'qsx'
    qsxdx = 'qsxdx'
    qsy = 'qsy'
    qsydy = 'qsydy'
    dxx = 'dxx'
    dyy = 'dyy'
    grow_slope = 'grow_slope'
    grow_aspect  = 'grow_aspect'
    grow_qsxdx = 'grow_qsxdx'
    grow_qsydy = 'grow_qsydy'
    grow_dxx = 'grow_dxx'
    grow_dyy = 'grow_dyy'
    erdep = 'erdep' # kg/m^2s
    divergence = 'divergence'
    settled_elevation = 'settled_elevation'
    smoothed_elevation = 'smoothed_elevation'
    sedflow = 'sedflow'

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

    # derive rainfall energy (MJ ha^-1 mm^-1)
    gscript.run_command('r.mapcalc',
        expression="{rain_energy} = 0.29*(1.-(0.72*exp(-0.05*{rain_intensity})))".format(rain_energy=rain_energy,
            rain_intensity=self.rain_intensity),
        overwrite=True)

    # derive rainfall volume (mm) = rainfall intensity (mm/hr) * (rainfall interval (min) * (1 hr / 60 min))
    gscript.run_command('r.mapcalc',
        expression="{rain_volume} = {rain_intensity}*({rain_interval}/60.)".format(rain_volume=rain_volume,
            rain_intensity=self.rain_intensity,
            rain_interval=self.rain_interval),
        overwrite=True)

    # derive event erosivity index (MJ mm ha^-1 hr^-1)
    gscript.run_command('r.mapcalc',
        expression="{erosivity} = ({rain_energy}*{rain_volume})*{rain_intensity}*1.".format(erosivity=erosivity,
            rain_energy=rain_energy,
            rain_volume=rain_volume,
            rain_intensity=self.rain_intensity),
        overwrite=True)

    # multiply by rainfall interval in seconds (MJ mm ha^-1 hr^-1 s^-1)
    gscript.run_command('r.mapcalc',
        expression="{r_factor} = {erosivity}/({rain_interval}*60.)".format(r_factor=r_factor,
            erosivity=erosivity,
            rain_interval=self.rain_interval),
        overwrite=True)

    # compute slope and aspect
    gscript.run_command('r.slope.aspect',
        elevation=self.elevation,
        slope=slope,
        aspect=aspect,
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

    # compute flow accumulation
    gscript.run_command('r.watershed',
        elevation=self.elevation,
        accumulation=depth,
        overwrite=True)

    # compute dimensionless topographic factor
    gscript.run_command('r.mapcalc',
        expression="{ls_factor} = ({m} + 1.0) * (({flowacc} / 22.1)^ {m}) * ((sin({slope}) / 0.09)^{n})".format(ls_factor=ls_factor,
            m=self.m,
            flowacc=depth,
            slope=slope,
            n=self.n),
        overwrite=True)

    # compute sediment flow at sediment transport capacity
    """E = R * K * LS * C * P
    where
    E is average annual soil loss
    R is rainfall factor
    K is soil erodibility factor
    LS is a dimensionless topographic (length-slope) factor
    C is a dimensionless land cover factor
    P is a dimensionless prevention measures factor
    """
    gscript.run_command('r.mapcalc',
        expression="{sedflow} = {r_factor} * {k_factor} * {ls_factor} * {c_factor}".format(r_factor=r_factor,
            k_factor=self.k_factor,
            c_factor=self.c_factor,
            ls_factor=ls_factor,
            slope=slope,
            flowacc=depth,
            sedflow=sedflow),
        overwrite=True)

    # convert sediment flow from tons/ha to kg/ms
    gscript.run_command('r.mapcalc',
        expression="{converted_sedflow} = {sedflow} * {ton_to_kg} / {ha_to_m2}".format(converted_sedflow=sediment_flux,
            sedflow=sedflow,
            ton_to_kg=1000.,
            ha_to_m2=10000.),
        overwrite=True)

    # compute sediment flow rate in x direction (m^2/s)
    gscript.run_command('r.mapcalc',
        expression="{qsx} = {sedflow} * cos({aspect})".format(sedflow=sediment_flux,
            aspect=aspect, qsx=qsx),
        overwrite=True)

    # compute sediment flow rate in y direction (m^2/s)
    gscript.run_command('r.mapcalc',
        expression="{qsy} = {sedflow} * sin({aspect})".format(sedflow=sediment_flux,
            aspect=aspect,
            qsy=qsy),
        overwrite=True)

    # compute change in sediment flow in x direction as partial derivative of sediment flow field
    gscript.run_command('r.slope.aspect',
        elevation=qsx,
        dx=qsxdx,
        overwrite=True)

    # compute change in sediment flow in y direction as partial derivative of sediment flow field
    gscript.run_command('r.slope.aspect',
        elevation=qsy,
        dy=qsydy,
        overwrite=True)

    # grow border to fix edge effects of moving window computations
    gscript.run_command('r.grow.distance',
        input=qsydy,
        value=grow_qsydy,
        overwrite=True)
    qsydy = grow_qsydy
    gscript.run_command('r.grow.distance',
        input=qsxdx,
        value=grow_qsxdx,
        overwrite=True)
    qsxdx = grow_qsxdx

    # compute net erosion-deposition (kg/m^2s) as divergence of sediment flow
    gscript.run_command('r.mapcalc',
        expression="{erdep} = {qsxdx} + {qsydy}".format(erdep=erdep,
            qsxdx=qsxdx,
            qsydy=qsydy),
        overwrite=True)

    # filter outliers
    gscript.run_command('r.mapcalc',
        expression="{erosion_deposition} = if({erdep}<{erdepmin},{erdepmin},if({erdep}>{erdepmax},{erdepmax},{erdep}))".format(erosion_deposition=erosion_deposition,
            erdep=erdep,
            erdepmin=self.erdepmin,
            erdepmax=self.erdepmax),
        overwrite=True)

    # set color table
    gscript.write_command('r.colors',
        map=erosion_deposition,
        rules='-',
        stdin='-15000 100 0 100\n-100 magenta\n-10 red\n-1 orange\n-0.1 yellow\n0 200 255 200\n0.1 cyan\n1 aqua\n10 blue\n100 0 0 100\n18000 black')

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
        expression="{difference} = {elevation}-{evolved_elevation}".format(difference=difference, elevation=self.elevation, evolved_elevation=evolved_elevation),
        overwrite=True)
    gscript.write_command('r.colors',
        map=difference,
        rules='-',
        stdin='-15000 100 0 100\n-100 magenta\n-10 red\n-1 orange\n-0.1 yellow\n0 200 255 200\n0.1 cyan\n1 aqua\n10 blue\n100 0 0 100\n18000 black')

    # remove temporary maps
    gscript.run_command('g.remove',
        type='raster',
        name=['slope',
            'aspect',
            'qsx',
            'qsy',
            'qsxdx',
            'qsydy',
            'dxx',
            'dyy',
            'grow_slope',
            'grow_aspect',
            'grow_qsxdx',
            'grow_qsydy',
            'grow_dxx',
            'grow_dyy',
            'erdep',
            'smoothed_elevation',
            'sedflow',
            'settled_elevation',
            'divergence',
            'rain_energy',
            'rain_volume',
            'erosivity',
            'r_factor',
            'ls_factor'],
        flags='f')

    return evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference
