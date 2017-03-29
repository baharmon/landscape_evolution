#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MODULE:    r.evolution

AUTHOR(S): Brendan Harmon <brendan.harmon@gmail.com>

PURPOSE:   Dynamic landscape evolution model

COPYRIGHT: (C) 2016 Brendan Harmon, and by the GRASS Development Team

           This program is free software under the GNU General Public
           License (>=v2). Read the file COPYING that comes with GRASS
           for details.
"""

#%module
#% description: Dynamic landscape evolution model
#% keyword: raster
#% keyword: terrain
#% keyword: landscape
#% keyword: evolution
#%end

#%option G_OPT_R_ELEV
#% key: elevation
#% required: yes
#% guisection: Basic
#%end

#%option
#% key: runs
#% type: string
#% required: yes
#% multiple: no
#% answer: series
#% options: event,series
#% description: Run for a single rainfall event or a series of events
#% descriptions: event;single rainfall event;series;series of rainfall events
#% guisection: Basic
#%end

#%option
#% key: mode
#% type: string
#% required: yes
#% multiple: no
#% answer: simwe_mode
#% options: simwe_mode,usped_mode,rusle_mode
#% description: Erosion deposition, transport limited, or detachment limited mode
#% descriptions: simwe_mode;erosion-deposition mode;usped_mode;transport limited mode;rusle_mode;detachment limited mode
#% guisection: Basic
#%end

#%option
#% key: rain_intensity
#% type: integer
#% description: Rainfall intensity in mm/hr
#% answer: 150
#% multiple: no
#% required: no
#% guisection: Event
#%end

#%option
#% key: rain_duration
#% type: integer
#% description: Total duration of storm event in minutes
#% answer: 60
#% multiple: no
#% required: no
#% guisection: Event
#%end

#%option G_OPT_F_INPUT
#% key: precipitation
#% description: Name of input precipitation file
#% label: Precipitation file
#% required: no
#% guisection: Series
#%end

#%option G_OPT_R_INPUT
#% key: k_factor
#% description: Soil erodibility factor
#% label: K factor
#% required: no
#% guisection: Transport limited
#%end

#%option
#% key: k_factor_value
#% type: double
#% description: Soil erodibility constant
#% label: K factor constant
#% answer: 0.25
#% multiple: no
#% guisection: Transport limited
#%end

#%option G_OPT_R_INPUT
#% key: c_factor
#% description: Land cover factor
#% label: C factor
#% required: no
#% guisection: Transport limited
#%end

#%option
#% key: c_factor_value
#% type: double
#% description: Land cover constant
#% label: C factor constant
#% answer: 0.1
#% multiple: no
#% guisection: Transport limited
#%end

#%option
#% key: m
#% type: double
#% description: Water flow exponent
#% label: Water flow exponent
#% answer: 1.0
#% multiple: no
#% guisection: Transport limited
#%end

#%option
#% key: n
#% type: double
#% description: Slope exponent
#% label: Slope exponent
#% answer: 1.0
#% multiple: no
#% guisection: Transport limited
#%end

#%option
#% key: walkers
#% type: integer
#% description: Number of walkers (max = 7000000)
#% answer: 1000000
#% multiple: no
#% required: yes
#% guisection: Input
#%end

#%option G_OPT_R_INPUT
#% key: runoff
#% description: Runoff coefficient (0.6 for bare earth, 0.35 for grass or crops, 0.5 for shrubs and trees, 0.25 for forest, 0.95 for roads)
#% label: Runoff coefficient
#% required: no
#% guisection: Input
#%end

#%option
#% key: runoff_value
#% type: double
#% description: Runoff coefficient (0.6 for bare earth, 0.35 for grass or crops, 0.5 for shrubs and trees, 0.25 for forest, 0.95 for roads)
#% label: Runoff coefficient
#% answer: 0.35
#% multiple: no
#% guisection: Input
#%end

#%option G_OPT_R_INPUT
#% key: mannings
#% description: Manning's roughness coefficient
#% label: Manning's roughness coefficient
#% required: no
#% guisection: Input
#%end

#%option
#% key: mannings_value
#% type: double
#% description: Manning's roughness coefficient
#% label: Manning's roughness coefficient
#% answer: 0.04
#% multiple: no
#% guisection: Input
#%end

#%option G_OPT_R_INPUT
#% key: detachment
#% description: Detachment coefficient
#% label: Detachment coefficient
#% required: no
#% guisection: Input
#%end

#%option
#% key: detachment_value
#% type: double
#% description: Detachment coefficient
#% label: Detachment coefficient
#% answer: 0.01
#% multiple: no
#% guisection: Input
#%end

#%option G_OPT_R_INPUT
#% key: transport
#% description: Transport coefficient
#% label: Transport coefficient
#% required: no
#% guisection: Input
#%end

#%option
#% key: transport_value
#% type: double
#% description: Transport coefficient
#% label: Transport coefficient
#% answer: 0.01
#% multiple: no
#% guisection: Input
#%end

#%option G_OPT_R_INPUT
#% key: shearstress
#% description: Shear stress coefficient
#% label: Shear stress coefficient
#% required: no
#% guisection: Input
#%end

#%option
#% key: shearstress_value
#% type: double
#% description: Shear stress coefficient
#% label: Shear stress coefficient
#% answer: 0.0
#% multiple: no
#% guisection: Input
#%end

#%option G_OPT_R_INPUT
#% key: density
#% description: Sediment mass density in g/cm^3
#% label: Sediment mass density
#% required: no
#% guisection: Input
#%end

#%option
#% key: density_value
#% type: double
#% description: Sediment mass density in g/cm^3
#% label: Sediment mass density
#% answer: 1.4
#% multiple: no
#% guisection: Input
#%end

#%option G_OPT_R_INPUT
#% key: mass
#% description: Mass of sediment per unit area in kg/m^2
#% label: Mass of sediment per unit area
#% required: no
#% guisection: Input
#%end

#%option
#% key: mass_value
#% type: double
#% description: Mass of sediment per unit area in kg/m^2
#% label: Mass of sediment per unit area
#% answer: 116.
#% multiple: no
#% guisection: Input
#%end

#%option
#% key: grav_diffusion
#% type: double
#% description: Gravitational diffusion coefficient in m^2/s
#% label: Gravitational diffusion coefficient
#% answer: 0.2
#% multiple: no
#% guisection: Input
#%end

#%option
#% key: smoothing
#% type: double
#% description: Neighborhood size for smoothing
#% label: Neighborhood size for smoothing
#% answer: 3
#% multiple: no
#% guisection: Input
#%end

#%option
#% key: erdepmin
#% type: double
#% description: Minimum values for erosion-deposition in kg/m^2s
#% label: Minimum values for erosion-deposition
#% answer: -1.0
#% multiple: no
#% guisection: Input
#%end

#%option
#% key: erdepmax
#% type: double
#% description: Maximum values for erosion-deposition in kg/m^2s
#% label: Maximum values for erosion-deposition
#% answer: 1.0
#% multiple: no
#% guisection: Input
#%end

#%option
#% key: fluxmax
#% type: double
#% description: Maximum values for sediment flux in kg/ms
#% label: Maximum values for sediment flux
#% answer: 3.0
#% multiple: no
#% guisection: Input
#%end

#%option
#% key: start
#% type: string
#% description: Start time in year-month-day hour:minute:second format
#% answer: 2015-10-06 00:00:00
#% multiple: no
#% required: yes
#% guisection: Temporal
#%end

#%option
#% key: rain_interval
#% type: integer
#% description: Time interval between evolution events in minutes
#% answer: 10
#% multiple: no
#% required: yes
#% guisection: Temporal
#%end

#%option G_OPT_T_TYPE
#% key: temporaltype
#% answer: absolute
#% required: yes
#% guisection: Temporal
#%end

#%option G_OPT_STRDS_OUTPUT
#% key: elevation_timeseries
#% answer: elevation_timeseries
#% required: yes
#% guisection: Output
#%end

#%option G_OPT_STRDS_OUTPUT
#% key: depth_timeseries
#% answer: depth_timeseries
#% required: no
#% guisection: Output
#%end

#%option G_OPT_STRDS_OUTPUT
#% key: erdep_timeseries
#% answer: erdep_timeseries
#% required: no
#% guisection: Output
#%end

#%option G_OPT_STRDS_OUTPUT
#% key: flux_timeseries
#% answer: flux_timeseries
#% required: no
#% guisection: Output
#%end

#%option G_OPT_STRDS_OUTPUT
#% key: difference_timeseries
#% answer: difference_timeseries
#% required: no
#% guisection: Output
#%end

import os
import sys
import atexit
import csv
import datetime
from math import exp
import grass.script as gscript
from grass.exceptions import CalledModuleError

def main():
    options, flags = gscript.parser()
    elevation = options['elevation']
    runs = options['runs']
    mode = options['mode']
    precipitation = options['precipitation']
    start = options['start']
    rain_intensity = options['rain_intensity']
    rain_duration = options['rain_duration']
    rain_interval = options['rain_interval']
    temporaltype = options['temporaltype']
    elevation_timeseries = options['elevation_timeseries']
    elevation_title = 'Evolved elevation'
    elevation_description = 'Time-series of evolved digital elevation models'
    depth_timeseries = options['depth_timeseries']
    depth_title = 'Evolved depth'
    depth_description = 'Time-series of evolved water depth'
    erdep_timeseries = options['erdep_timeseries']
    erdep_title = 'Evolved erosion-deposition'
    erdep_description = 'Time-series of evolved erosion-deposition'
    flux_timeseries = options['flux_timeseries']
    flux_title = 'Evolved flux'
    flux_description = 'Time-series of evolved sediment flux'
    difference_timeseries = options['difference_timeseries']
    difference_title = 'Evolved difference'
    difference_description = 'Time-series of evolved difference in elevation'
    walkers = options['walkers']
    runoff = options['runoff']
    runoff_value = options['runoff_value']
    mannings = options['mannings']
    mannings_value = options['mannings_value']
    detachment = options['detachment']
    detachment_value = options['detachment_value']
    transport = options['transport']
    transport_value = options['transport_value']
    shearstress = options['shearstress']
    shearstress_value = options['shearstress_value']
    density = None
    density_raster = options['density']
    density_value = options['density_value']
    mass = options['mass']
    mass_value = options['mass_value']
    grav_diffusion = options['grav_diffusion']
    smoothing = options['smoothing']
    erdepmin = options['erdepmin']
    erdepmax = options['erdepmax']
    fluxmax = options['fluxmax']
    k_factor = options['k_factor']
    c_factor = options['c_factor']
    k_factor_value = options['k_factor_value']
    c_factor_value = options['c_factor_value']
    m = options['m']
    n = options['n']

    # check for alternative input parameters
    if not runoff:
        runoff = 'runoff'
        gscript.run_command('r.mapcalc',
            expression="runoff = {runoff_value}".format(**locals()),
            overwrite=True)

    if not mannings:
        mannings = 'mannings'
        gscript.run_command('r.mapcalc',
            expression="mannings = {mannings_value}".format(**locals()),
            overwrite=True)

    if not detachment:
        detachment = 'detachment'
        gscript.run_command('r.mapcalc',
            expression="detachment = {detachment_value}".format(**locals()),
            overwrite=True)

    if not transport:
        transport = 'transport'
        gscript.run_command('r.mapcalc',
            expression="transport = {transport_value}".format(**locals()),
            overwrite=True)

    if not shearstress:
        shearstress = 'shearstress'
        gscript.run_command('r.mapcalc',
            expression="shearstress = {shearstress_value}".format(**locals()),
            overwrite=True)

    if not mass:
        mass = 'mass'
        gscript.run_command('r.mapcalc',
            expression="mass = {mass_value}".format(**locals()),
            overwrite=True)

    density = 'density'
    if density_raster:
        # convert g/cm^3 to kg/m^3
        gscript.run_command('r.mapcalc',
            expression="density = {density_raster} * 1000".format(**locals()),
            overwrite=True)
    else:
        # convert g/cm^3 to kg/m^3
        gscript.run_command('r.mapcalc',
            expression="density = {density_value} * 1000".format(**locals()),
            overwrite=True)

    if not c_factor:
        c_factor = 'c_factor'
        gscript.run_command('r.mapcalc',
            expression="c_factor = {c_factor_value}".format(**locals()),
            overwrite=True)

    if not k_factor:
        k_factor = 'k_factor'
        gscript.run_command('r.mapcalc',
            expression="k_factor = {k_factor_value}".format(**locals()),
            overwrite=True)

    # create dynamic_evolution object
    event = DynamicEvolution(elevation=elevation,
        mode=mode,
        precipitation=precipitation,
        rain_intensity=rain_intensity,
        rain_duration=rain_duration,
        rain_interval=rain_interval,
        temporaltype=temporaltype,
        elevation_timeseries=elevation_timeseries,
        elevation_title=elevation_title,
        elevation_description=elevation_description,
        depth_timeseries=depth_timeseries,
        depth_title=depth_title,
        depth_description=depth_description,
        erdep_timeseries=erdep_timeseries,
        erdep_title=erdep_title,
        erdep_description=erdep_description,
        flux_timeseries=flux_timeseries,
        flux_title=flux_title,
        flux_description=flux_description,
        difference_timeseries=difference_timeseries,
        difference_title=difference_title,
        difference_description=difference_description,
        start=start,
        walkers=walkers,
        runoff=runoff,
        mannings=mannings,
        detachment=detachment,
        transport=transport,
        shearstress=shearstress,
        density=density,
        mass=mass,
        grav_diffusion=grav_diffusion,
        smoothing=smoothing,
        erdepmin=erdepmin,
        erdepmax=erdepmax,
        fluxmax=fluxmax,
        k_factor=k_factor,
        c_factor=c_factor,
        m=m,
        n=n)

    # determine type of model and run
    if runs == "series":
        elevation = event.rainfall_series()

    if runs == "event":
        elevation = event.rainfall_event()

    atexit.register(cleanup)
    sys.exit(0)

class Evolution:
    def __init__(self, elevation, precipitation, start, rain_intensity,
        rain_interval, walkers, runoff, mannings, detachment, transport,
        shearstress, density, mass, grav_diffusion, smoothing,
        erdepmin, erdepmax, fluxmax, k_factor, c_factor, m, n):
        self.elevation = elevation
        self.precipitation = precipitation
        self.start = start
        self.rain_intensity = float(rain_intensity)
        self.rain_interval = int(rain_interval)
        self.walkers = walkers
        self.runoff = runoff
        self.mannings = mannings
        self.detachment = detachment
        self.transport = transport
        self.shearstress = shearstress
        self.density = density
        self.mass = mass
        self.grav_diffusion = grav_diffusion
        self.smoothing = smoothing
        self.erdepmin = erdepmin
        self.erdepmax = erdepmax
        self.fluxmax = fluxmax
        self.k_factor = k_factor
        self.c_factor = c_factor
        self.m = m
        self.n = n

    def erosion_deposition(self):
        """a small-scale, process-based landscape evolution model
        using simulated net erosion and deposition
        to carve a digital elevation model"""

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
            erosion_deposition=erdep,
            sediment_flux=sedflux,
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

        gscript.run_command('r.mapcalc',
            expression="{sediment_flux} = if({sedflux}>{fluxmax},{fluxmax},{sedflux})".format(sediment_flux=sediment_flux,
                sedflux=sedflux,
                fluxmax=self.fluxmax),
            overwrite=True)
        gscript.run_command('r.colors',
            map=sediment_flux,
            raster=sedflux)

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
            name=['rain',
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

        return evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference

    def flux(self):
        """a detachment limited gully evolution model
        using simulated sediment flux to carve
        a digital elevation model"""

        # assign variables
        slope = 'slope'
        aspect = 'aspect'
        dx = 'dx'
        dy = 'dy'
        grow_slope = 'grow_slope'
        grow_aspect  = 'grow_aspect'
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

        # sediment flux simulation
        gscript.run_command('r.sim.sediment',
            elevation=self.elevation,
            water_depth=depth,
            dx=dx,
            dy=dy,
            detachment_coeff=self.detachment,
            transport_coeff=self.transport,
            shear_stress=self.shearstress,
            man=self.mannings,
            erosion_deposition=erdep,
            sediment_flux=sedflux,
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

        # filter outliers
        gscript.run_command('r.mapcalc',
            expression="{sediment_flux} = if({sedflux}>{fluxmax},{fluxmax},{sedflux})".format(sediment_flux=sediment_flux,
                sedflux=sedflux,
                fluxmax=self.fluxmax),
            overwrite=True)
        gscript.run_command('r.colors',
            map=sediment_flux,
            raster=sedflux)

        # evolve landscape
        """change in elevation (m) = change in time (s) * sediment flux (kg/ms) / mass of sediment per unit area (kg/m^2)"""
        gscript.run_command('r.mapcalc',
            expression="{evolved_elevation} = {elevation}-({rain_interval}*60*{sediment_flux}/{density})".format(evolved_elevation=evolved_elevation,
                elevation=self.elevation,
                rain_interval=self.rain_interval,
                sediment_flux=sediment_flux,
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
            name=['rain',
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

        return evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference

    def usped(self):
        """a transport limited landscape evolution model
        using the USPED (Unit Stream Power Based Model) model to evolve
        a digital elevation model"""

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

        # compute event-based erosivity (R) factor (MJ mm ha^-1 hr^-1)

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
        # add depression parameter to r.watershed
        # derive from landcover class

        # compute dimensionless topographic factor
        gscript.run_command('r.mapcalc',
            expression="{ls_factor} = ({flowacc} ^ {m}) * (sin({slope})^{n})".format(ls_factor=ls_factor,
                m=self.m,
                flowacc=depth,
                slope=slope,
                n=self.n),
            overwrite=True)

        # compute sediment flow at sediment transport capacity
        """
        T = R * K * C * P * LST
        where
        E is average annual soil loss
        R is rainfall factor
        K is soil erodibility factor
        C is a dimensionless land cover factor
        P is a dimensionless prevention measures factor
        LST is the topographic component of sediment transport capacity of overland flow
        """
        gscript.run_command('r.mapcalc',
            expression="{sedflow} = {r_factor} * {k_factor} * {c_factor} * {ls_factor}".format(r_factor=r_factor,
                k_factor=self.k_factor,
                c_factor=self.c_factor,
                ls_factor=ls_factor,
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

    def rusle(self):
        """a detachment limited landscape evolution model
        using the RUSLE3D (Revised Universal Soil Loss Equation 3D) model
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
            # length_slope=ls_factor
            overwrite=True)
        # use length_slope output from r.watershed for LS
        # add depression parameter to r.watershed
        # derive from landcover class

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


class DynamicEvolution:
    def __init__(self, elevation, mode, precipitation, rain_intensity,
        rain_duration, rain_interval, temporaltype, elevation_timeseries,
        elevation_title, elevation_description, depth_timeseries, depth_title,
        depth_description, erdep_timeseries, erdep_title, erdep_description,
        flux_timeseries, flux_title, flux_description, difference_timeseries,
        difference_title, difference_description, start, walkers, runoff,
        mannings, detachment, transport, shearstress, density, mass,
        grav_diffusion, smoothing, erdepmin, erdepmax, fluxmax,
        k_factor, c_factor, m, n):
        self.elevation = elevation
        self.mode = mode
        self.precipitation = precipitation
        self.start = start
        self.rain_intensity = rain_intensity
        self.rain_duration = rain_duration
        self.rain_interval = rain_interval
        self.temporaltype = temporaltype
        self.elevation_timeseries = elevation_timeseries
        self.elevation_title = elevation_title
        self.elevation_description = elevation_description
        self.depth_timeseries=depth_timeseries
        self.depth_title=depth_title
        self.depth_description=depth_description
        self.erdep_timeseries=erdep_timeseries
        self.erdep_title=erdep_title
        self.erdep_description=erdep_description
        self.flux_timeseries=flux_timeseries
        self.flux_title=flux_title
        self.flux_description=flux_description
        self.difference_timeseries=difference_timeseries
        self.difference_title=difference_title
        self.difference_description=difference_description
        self.walkers = walkers
        self.runoff = runoff
        self.mannings = mannings
        self.detachment = detachment
        self.transport = transport
        self.shearstress = shearstress
        self.density = density
        self.mass = mass
        self.grav_diffusion = grav_diffusion
        self.smoothing = smoothing
        self.erdepmin = erdepmin
        self.erdepmax = erdepmax
        self.fluxmax = fluxmax
        self.k_factor = k_factor
        self.c_factor = c_factor
        self.m = m
        self.n = n

    def erosion_regime(self):
        """determine whether transport limited or detachment limited regime"""

        # assign local variables
        rhow = 1000. # ?
        gravity = 9.81 # gravitational acceleration (m/s^2)
        critical_shearstress = 'critical_shearstress'
        sigma = 'sigma' # first order reaction term dependent on soil and cover properties (m^−1)

        # compute slope and partial derivatives
        gscript.run_command('r.slope.aspect',
            elevation=elevation,
            slope=slope,
            dx=dx,
            dy=dy,
            overwrite=True)

        # hyrdology parameters
        gscript.run_command('r.mapcalc',
            expression="{rain} = {rain_intensity}*{runoff}".format(rain=rain,
                rain_intensity=rain_intensity,
                runoff=runoff),
            overwrite=True)

        # hydrologic simulation
        gscript.run_command('r.sim.water',
            elevation=elevation,
            dx=dx,
            dy=dy,
            rain=rain,
            man=mannings,
            depth=depth,
            niterations=rain_interval,
            nwalkers=walkers,
            overwrite=True)

        gscript.run_command('r.mapcalc',
            expression="critical_shearstress = ({rhow} * {gravity}) * {depth} * sin({slope})".format(rhow=rhow,
                gravity=gravity,
                depth=depth,
                slope=slope),
            overwrite=True)

        gscript.run_command('r.mapcalc',
            expression="sigma = if((({critical_shearstress} <= {shearstress}) || ({transport} == 0.)),0., ({detachment} / {transport}) * ({critical_shearstress} - {shearstress}) / ({critical_shearstress}^1.5))".format(critical_shearstress=critical_shearstress,
                shearstress=shearstress,
                transport=transport,
                detachment=detachment),
            overwrite=True)

        # detachment capacity = sigma * transport capacity
        # transport capacity >> detachment capacity when sigma -> 0
        univar = gscript.parse_command('r.univar',
            map=elevation,
            separator='newline',
            flags='g')
        mean_sigma = float(univar['mean'])
        if mean_sigma > 0.:
            regime = "detachment limited"
        else:
            regime = "transport limited"

        # remove temporary maps
        gscript.run_command('g.remove',
            type='raster',
            name=['slope',
                'dx',
                'dy',
                'rain',
                'depth',
                'critical_shearstress',
                'sigma'],
            flags='f')

        return regime

    def rainfall_event(self):
        """a dynamic, process-based landscape evolution model
        of a single rainfall event that generates a timeseries
        of digital elevation models"""

        # assign local variables
        datatype = 'strds'
        increment = str(self.rain_interval)+" minutes"
        raster = 'raster'
        iterations = int(self.rain_duration)/int(self.rain_interval)
        rain_excess = 'rain_excess'
        net_difference = 'net_difference'

        # create raster space time datasets
        gscript.run_command('t.create',
            type=datatype,
            temporaltype=self.temporaltype,
            output=self.elevation_timeseries,
            title=self.elevation_title,
            description=self.elevation_description,
            overwrite=True)
        gscript.run_command('t.create',
            type=datatype,
            temporaltype=self.temporaltype,
            output=self.depth_timeseries,
            title=self.depth_title,
            description=self.depth_description,
            overwrite=True)
        gscript.run_command('t.create',
            type=datatype,
            temporaltype=self.temporaltype,
            output=self.erdep_timeseries,
            title=self.erdep_title,
            description=self.erdep_description,
            overwrite=True)
        gscript.run_command('t.create',
            type=datatype,
            temporaltype=self.temporaltype,
            output=self.flux_timeseries,
            title=self.flux_title,
            description=self.flux_description,
            overwrite=True)
        gscript.run_command('t.create',
            type=datatype,
            temporaltype=self.temporaltype,
            output=self.difference_timeseries,
            title=self.difference_title,
            description=self.difference_description,
            overwrite=True)

        # register the initial digital elevation model
        gscript.run_command('t.register',
            type=raster,
            input=self.elevation_timeseries,
            maps=self.elevation,
            start=self.start,
            increment=increment,
            flags='i',
            overwrite=True)

        # create evolution object
        evol = Evolution(elevation=self.elevation,
            precipitation=self.precipitation,
            start=self.start,
            rain_intensity=self.rain_intensity,
            rain_interval=self.rain_interval,
            walkers=self.walkers,
            runoff=self.runoff,
            mannings=self.mannings,
            detachment=self.detachment,
            transport=self.transport,
            shearstress=self.shearstress,
            density=self.density,
            mass=self.mass,
            grav_diffusion=self.grav_diffusion,
            smoothing=self.smoothing,
            erdepmin=self.erdepmin,
            erdepmax=self.erdepmax,
            fluxmax=self.fluxmax,
            k_factor=self.k_factor,
            c_factor=self.c_factor,
            m = self.m,
            n = self.n)

        # set temporary region
        gscript.use_temp_region()

        # determine mode and run model
        if self.mode == "simwe_mode":

            if self.regime == "detachment limited":
                evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.flux()

            if self.regime == "transport limited":
                evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.erosion_deposition()

        if self.mode == "usped_mode":
            evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.usped()

        if self.mode == "rusle_mode":
            evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.rusle()

        # remove relative timestamps from r.sim.water and r.sim.sediment
        gscript.run_command('r.timestamp',
            map=depth,
            date='none')
        gscript.run_command('r.timestamp',
            map=erosion_deposition,
            date='none')
        gscript.run_command('r.timestamp',
            map=sediment_flux,
            date='none')

        # register the evolved maps
        gscript.run_command('t.register',
            type=raster,
            input=self.elevation_timeseries,
            maps=evolved_elevation,
            start=evol.start,
            increment=increment,
            flags='i',
            overwrite=True)
        gscript.run_command('t.register',
            type=raster,
            input=self.depth_timeseries,
            maps=depth,
            start=evol.start,
            increment=increment,
            flags='i',
            overwrite=True)
        gscript.run_command('t.register',
            type=raster,
            input=self.erdep_timeseries,
            maps=erosion_deposition,
            start=evol.start,
            increment=increment,
            flags='i',
            overwrite=True)
        gscript.run_command('t.register',
            type=raster,
            input=self.flux_timeseries,
            maps=sediment_flux,
            start=evol.start,
            increment=increment,
            flags='i', overwrite=True)
        gscript.run_command('t.register',
            type=raster,
            input=self.difference_timeseries,
            maps=difference,
            start=evol.start,
            increment=increment,
            flags='i',
            overwrite=True)

        # run the landscape evolution model as a series of rainfall intervals in a rainfall event
        i = 1
        while i <= iterations:

            # update the elevation
            evol.elevation = evolved_elevation
            print evol.elevation

            # update time
            evol.start = time
            print evol.start

            # derive excess water (mm/hr) from rainfall rate (mm/hr) plus the product of depth (m) and the rainfall interval (min)
            gscript.run_command('r.mapcalc',
                expression="{rain_excess} = {rain_intensity}+(({depth}*(1/1000))*({rain_interval}*(1/60)))".format(rain_excess=rain_excess, rain_intensity=self.rain_intensity, depth=depth, rain_interval=self.rain_interval),
                overwrite=True)

            # update excess rainfall
            rain_intensity = 'rain_intensity'
            gscript.run_command('r.mapcalc',
                expression="{rain_intensity} = {rain_excess}".format(rain_intensity='rain_intensity',
                    rain_excess=rain_excess),
                overwrite=True)
            evol.rain_intensity = rain_intensity

            # determine mode and run model
            if self.mode == "simwe_mode":

                if self.regime == "detachment limited":
                    evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.flux()

                if self.regime == "transport limited":
                    evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.erosion_deposition()

            if self.mode == "usped_mode":
                evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.usped()

            if self.mode == "rusle_mode":
                evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.rusle()

            # remove relative timestamps from r.sim.water and r.sim.sediment
            gscript.run_command('r.timestamp',
                map=depth,
                date='none')
            gscript.run_command('r.timestamp',
                map=erosion_deposition,
                date='none')
            gscript.run_command('r.timestamp',
                map=sediment_flux,
                date='none')

            # register the evolved maps
            gscript.run_command('t.register',
                type=raster,
                input=self.elevation_timeseries,
                maps=evolved_elevation,
                start=evol.start,
                increment=increment,
                flags='i',
                overwrite=True)
            gscript.run_command('t.register',
                type=raster,
                input=self.depth_timeseries,
                maps=depth,
                start=evol.start,
                increment=increment,
                flags='i',
                overwrite=True)
            gscript.run_command('t.register',
                type=raster,
                input=self.erdep_timeseries,
                maps=erosion_deposition,
                start=evol.start,
                increment=increment,
                flags='i',
                overwrite=True)
            gscript.run_command('t.register',
                type=raster,
                input=self.flux_timeseries,
                maps=sediment_flux,
                start=evol.start,
                increment=increment,
                flags='i', overwrite=True)
            gscript.run_command('t.register',
                type=raster,
                input=self.difference_timeseries,
                maps=difference,
                start=evol.start,
                increment=increment,
                flags='i',
                overwrite=True)

            # remove temporary maps
            gscript.run_command('g.remove',
                type='raster',
                name=['rain_excess'],
                flags='f')

            i = i+1

        # compute net elevation change
        gscript.run_command('r.mapcalc',
            expression="{net_difference} = {elevation}-{evolved_elevation}".format(net_difference=net_difference, elevation=self.elevation, evolved_elevation=evol.elevation),
            overwrite=True)
        gscript.write_command('r.colors',
            map=net_difference,
            rules='-',
            stdin='-15000 100 0 100\n-100 magenta\n-10 red\n-1 orange\n-0.1 yellow\n0 200 255 200\n0.1 cyan\n1 aqua\n10 blue\n100 0 0 100\n18000 black')


    def rainfall_series(self):
        """a dynamic, process-based landscape evolution model
        for a series of rainfall events that generates
        a timeseries of digital elevation models"""

        # assign local temporal variables
        datatype = 'strds'
        increment = str(self.rain_interval)+" minutes"
        raster = 'raster'
        rain_excess = 'rain_excess'
        net_difference = 'net_difference'
        #iterations = sum(1 for row in precip)

        # create a raster space time dataset
        gscript.run_command('t.create',
            type=datatype,
            temporaltype=self.temporaltype,
            output=self.elevation_timeseries,
            title=self.elevation_title,
            description=self.elevation_description,
            overwrite=True)
        gscript.run_command('t.create',
            type=datatype,
            temporaltype=self.temporaltype,
            output=self.depth_timeseries,
            title=self.depth_title,
            description=self.depth_description,
            overwrite=True)
        gscript.run_command('t.create',
            type=datatype,
            temporaltype=self.temporaltype,
            output=self.erdep_timeseries,
            title=self.erdep_title,
            description=self.erdep_description,
            overwrite=True)
        gscript.run_command('t.create',
            type=datatype,
            temporaltype=self.temporaltype,
            output=self.flux_timeseries,
            title=self.flux_title,
            description=self.flux_description,
            overwrite=True)
        gscript.run_command('t.create',
            type=datatype,
            temporaltype=self.temporaltype,
            output=self.difference_timeseries,
            title=self.difference_title,
            description=self.difference_description,
            overwrite=True)

        # register the initial digital elevation model
        gscript.run_command('t.register',
            type=raster,
            input=self.elevation_timeseries,
            maps=self.elevation,
            start=self.start,
            increment=increment,
            flags='i',
            overwrite=True)

        # create evolution object
        evol = Evolution(elevation=self.elevation,
            precipitation=self.precipitation,
            start=self.start,
            rain_intensity=self.rain_intensity,
            rain_interval=self.rain_interval,
            walkers=self.walkers,
            runoff=self.runoff,
            mannings=self.mannings,
            detachment=self.detachment,
            transport=self.transport,
            shearstress=self.shearstress,
            density=self.density,
            mass=self.mass,
            grav_diffusion=self.grav_diffusion,
            smoothing=self.smoothing,
            erdepmin=self.erdepmin,
            erdepmax=self.erdepmax,
            fluxmax=self.fluxmax,
            k_factor=self.k_factor,
            m = self.m,
            n = self.n)

        # open txt file with precipitation data
        with open(evol.precipitation) as csvfile:

            # check for header
            has_header = csv.Sniffer().has_header(csvfile.read(1024))

            # rewind
            csvfile.seek(0)

            # skip header
            if has_header:
                next(csvfile)

            # parse time and precipitation
            precip = csv.reader(csvfile, delimiter=',', skipinitialspace=True)

            # set temporary region
            gscript.use_temp_region()

            # initial run
            initial = next(precip)
            evol.start = initial[0]
            evol.rain_intensity = 'rain_intensity'
            gscript.run_command('r.mapcalc',
                expression="{rain_intensity} = {initial}".format(rain_intensity=evol.rain_intensity,
                    initial=float(initial[1])),
                overwrite=True)

            # determine mode and run model
            if self.mode == "simwe_mode":

                if self.regime == "detachment limited":
                    evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.flux()

                if self.regime == "transport limited":
                    evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.erosion_deposition()

            if self.mode == "usped_mode":
                evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.usped()

            if self.mode == "rusle_mode":
                evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.rusle()

            # remove relative timestamps from r.sim.water and r.sim.sediment
            gscript.run_command('r.timestamp',
                map=depth,
                date='none')
            gscript.run_command('r.timestamp',
                map=erosion_deposition,
                date='none')
            gscript.run_command('r.timestamp',
                map=sediment_flux,
                date='none')

            # register the evolved digital elevation model
            gscript.run_command('t.register',
                type=raster,
                input=self.elevation_timeseries,
                maps=evolved_elevation,
                start=evol.start,
                increment=increment,
                flags='i',
                overwrite=True)
            gscript.run_command('t.register',
                type=raster,
                input=self.depth_timeseries,
                maps=depth,
                start=evol.start,
                increment=increment,
                flags='i',
                overwrite=True)
            gscript.run_command('t.register',
                type=raster,
                input=self.erdep_timeseries,
                maps=erosion_deposition,
                start=evol.start,
                increment=increment,
                flags='i',
                overwrite=True)
            gscript.run_command('t.register',
                type=raster,
                input=self.flux_timeseries,
                maps=sediment_flux,
                start=evol.start,
                increment=increment,
                flags='i',
                overwrite=True)
            gscript.run_command('t.register',
                type=raster,
                input=self.difference_timeseries,
                maps=difference,
                start=evol.start,
                increment=increment,
                flags='i',
                overwrite=True)

            # run the landscape evolution model for each rainfall record
            for row in precip:

                # update the elevation
                evol.elevation=evolved_elevation

                # update time
                evol.start=row[0]

                # derive excess water (mm/hr) from rainfall rate (mm/hr) plus the product of depth (m) and the rainfall interval (min)
                gscript.run_command('r.mapcalc',
                    expression="{rain_excess} = {rain_intensity}+(({depth}*(1/1000))*({rain_interval}*(1/60)))".format(rain_excess=rain_excess,
                        rain_intensity=float(row[1]),
                        depth=depth,
                        rain_interval=self.rain_interval),
                    overwrite=True)

                # update excess rainfall
                rain_intensity = 'rain_intensity'
                gscript.run_command('r.mapcalc',
                    expression="{rain_intensity} = {rain_excess}".format(rain_intensity='rain_intensity',
                        rain_excess=rain_excess),
                    overwrite=True)
                evol.rain_intensity = rain_intensity

                # determine mode and run model
                if self.mode == "simwe_mode":

                    if self.regime == "detachment limited":
                        evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.flux()

                    if self.regime == "transport limited":
                        evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.erosion_deposition()

                if self.mode == "usped_mode":
                    evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.usped()

                if self.mode == "rusle_mode":
                    evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.rusle()

                # remove relative timestamps from r.sim.water and r.sim.sediment
                gscript.run_command('r.timestamp',
                    map=depth,
                    date='none')
                gscript.run_command('r.timestamp',
                    map=erosion_deposition,
                    date='none')
                gscript.run_command('r.timestamp',
                    map=sediment_flux,
                    date='none')

                # register the evolved digital elevation model
                gscript.run_command('t.register',
                    type=raster,
                    input=self.elevation_timeseries,
                    maps=evolved_elevation,
                    start=evol.start,
                    increment=increment,
                    flags='i',
                    overwrite=True)
                gscript.run_command('t.register',
                    type=raster,
                    input=self.depth_timeseries,
                    maps=depth,
                    start=evol.start,
                    increment=increment,
                    flags='i',
                    overwrite=True)
                gscript.run_command('t.register',
                    type=raster,
                    input=self.erdep_timeseries,
                    maps=erosion_deposition,
                    start=evol.start,
                    increment=increment,
                    flags='i',
                    overwrite=True)
                gscript.run_command('t.register',
                    type=raster,
                    input=self.flux_timeseries,
                    maps=sediment_flux,
                    start=evol.start,
                    increment=increment,
                    flags='i',
                    overwrite=True)
                gscript.run_command('t.register',
                    type=raster,
                    input=self.difference_timeseries,
                    maps=difference,
                    start=evol.start,
                    increment=increment,
                    flags='i',
                    overwrite=True)

                # remove temporary maps
                gscript.run_command('g.remove',
                    type='raster',
                    name=['rain_excess'],
                    flags='f')

            # compute net elevation change
            gscript.run_command('r.mapcalc',
                expression="{net_difference} = {elevation}-{evolved_elevation}".format(net_difference=net_difference, elevation=self.elevation, evolved_elevation=evol.elevation),
                overwrite=True)
            gscript.write_command('r.colors',
                map=net_difference,
                rules='-',
                stdin='-15000 100 0 100\n-100 magenta\n-10 red\n-1 orange\n-0.1 yellow\n0 200 255 200\n0.1 cyan\n1 aqua\n10 blue\n100 0 0 100\n18000 black')


def cleanup():
    try:
        # remove temporary maps
        gscript.run_command('g.remove',
            type='raster',
            name=['rain_excess',
                'rain',
                'sedflow',
                'evolving_elevation',
                'smoothed_elevation',
                'settled_elevation',
                'divergence',
                'rain_energy',
                'rain_volume',
                'erosivity',
                'r_factor',
                'ls_factor',
                'dx',
                'dy',
                'dxx',
                'dyy',
                'qsx',
                'qsy',
                'qsxdx',
                'qsydy',
                'grow_slope',
                'grow_aspect',
                'grow_dx',
                'grow_dy',
                'grow_dxx',
                'grow_dyy',
                'grow_qsxdx',
                'grow_qsydy'],
            flags='f')

    except CalledModuleError:
        pass

if __name__ == '__main__':
    main()
