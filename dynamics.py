#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@brief: dynamic landscape evolution model

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

# TO DO:
# return depth, erdep, and difference
# register depth, erdep, difference, and flux in temporal framwork
# refactor code as one script
# create new functions for rainfall_flux and series_flux
# prepare as grass add-on
# optional outputs: depth, erdep, flux, difference, net_difference
# allow choice of maps or constants as inputs
# rain as list, input parameters, or maps
# time as list or input parameters
# convert both maps and constants' units
# option to compute mannings from difference between dem and dsm
# test by experimenting with diferent dems and parameters
# test with uav timeseries
# test with field data
# empirically calibrate parameters
# create documentation

import os
import sys
import atexit
import csv
import grass.script as gscript
from grass.exceptions import CalledModuleError
import process

class DynamicEvolution:
    def __init__(self, dem, precipitation, rain_intensity, rain_duration, rain_interval, temporaltype, strds, title, description, start, walkers, runoff, mannings, detachment, transport, shearstress, density, mass, erdepmin, erdepmax, fluxmin, fluxmax):
        self.dem = dem
        self.precipitation = precipitation
        self.start = start
        self.rain_intensity = rain_intensity
        self.rain_duration = rain_duration
        self.rain_interval = rain_interval
        self.temporaltype = temporaltype
        self.strds = strds
        self.title = title
        self.description = description
        self.start = start
        self.walkers = walkers
        self.runoff = runoff
        self.mannings = mannings
        self.detachment = detachment
        self.transport = transport
        self.shearstress = shearstress
        self.density = density
        self.mass = mass
        self.erdepmin = erdepmin
        self.erdepmax = erdepmax
        self.fluxmin = fluxmin
        self.fluxmax = fluxmax

    def rainfall_event(self):
        """a dynamic, process-based landscape evolution model of a single rainfall event that generates a timeseries of digital elevation models"""

        # assign local temporal variables
        datatype = 'strds'
        increment = str(self.rain_interval)+" minutes"
        raster = 'raster'
        iterations = self.rain_duration/self.rain_interval
        rain_excess = 'rain_excess'
        net_difference = 'net_difference'

        # create a raster space time dataset
        gscript.run_command('t.create', type=datatype, temporaltype=self.temporaltype, output=self.strds, title=self.title, description=self.description, overwrite=True)

        # register the initial digital elevation model
        gscript.run_command('t.register', type=raster, input=self.strds, maps=self.dem, start=self.start, increment=increment, flags='i', overwrite=True)

        # create evolution object
        evol = process.Evolution(dem=self.dem, precipitation=self.precipitation, start=self.start, rain_intensity=self.rain_intensity, rain_interval=self.rain_interval, walkers=self.walkers, runoff=self.runoff, mannings=self.mannings, detachment=self.detachment, transport=self.transport, shearstress=self.shearstress, density=self.density, mass=self.mass, erdepmin=self.erdepmin, erdepmax=self.erdepmax, fluxmin=self.fluxmin, fluxmax=self.fluxmax)

        # run model
        evolved_dem, time, depth = evol.erosion_deposition()

        # run the landscape evolution model as a series of rainfall intervals in a rainfall event
        i=1
        while i <= iterations:

            # update the elevation
            evol.dem = evolved_dem
            print evol.dem

            # update time
            evol.start = time
            print evol.start

            # derive excess water (mm/hr) from rain intensity (mm/hr) plus the product of depth (m) and the rainfall interval (min)
            gscript.run_command('r.mapcalc', expression="{rain_excess} = {rain_intensity}+(({depth}*(1/1000))*({rain_interval}*(1/60)))".format(rain_excess=rain_excess, rain_intensity=self.rain_intensity, depth=depth, rain_interval=self.rain_interval), overwrite=True)

            # update excess rainfall
            evol.rain_intensity = rain_excess

            # run model
            evolved_dem, time, depth = evol.erosion_deposition()
#            evolved_dem, time, depth = evol.flux()

            # register the evolved digital elevation model
            gscript.run_command('t.register', type=raster, input=self.strds, maps=evolved_dem, start=evol.start, increment=increment, flags='i', overwrite=True)

            # remove temporary maps
            gscript.run_command('g.remove', type='raster', name=['rain_excess'], flags='f')

            i=i+1

        # compute net elevation change
        gscript.run_command('r.mapcalc', expression="{net_difference} = {dem}-{evolved_dem}".format(net_difference=net_difference, dem=self.dem, evolved_dem=evol.dem), overwrite=True)
        gscript.run_command('r.colors', map=net_difference, color='differences')

    def rainfall_series(self):
        """a dynamic, process-based landscape evolution model for a series of rainfall events that generates a timeseries of digital elevation models"""

        # assign local temporal variables
        datatype = 'strds'
        increment = str(self.rain_interval)+" minutes"
        raster = 'raster'
        rain_excess = 'rain_excess'
        net_difference = 'net_difference'
        #iterations = sum(1 for row in precip)

        # create a raster space time dataset
        gscript.run_command('t.create', type=datatype, temporaltype=self.temporaltype, output=self.strds, title=self.title, description=self.description, overwrite=True)

        # register the initial digital elevation model
        gscript.run_command('t.register', type=raster, input=self.strds, maps=self.dem, start=self.start, increment=increment, flags='i', overwrite=True)

        # create evolution object
        evol = process.Evolution(dem=self.dem, precipitation=self.precipitation, start=self.start, rain_intensity=self.rain_intensity, rain_interval=self.rain_interval, walkers=self.walkers, runoff=self.runoff, mannings=self.mannings, detachment=self.detachment, transport=self.transport, shearstress=self.shearstress, density=self.density, mass=self.mass, erdepmin=self.erdepmin, erdepmax=self.erdepmax, fluxmin=self.fluxmin, fluxmax=self.fluxmax)

        # open txt file with precipitation data
        with open(precipitation) as csvfile:

            # check for header
            has_header = csv.Sniffer().has_header(csvfile.read(1024))

            # rewind
            csvfile.seek(0)

            # skip header
            if has_header:
                next(csvfile)

            # parse time and precipitation
            precip = csv.reader(csvfile, delimiter=',', skipinitialspace=True)

            # initial run
            initial=next(precip)
            evol.start=initial[0]
            evol.rain_intensity=float(initial[1]) # mm/hr
            evolved_dem, time, depth = evol.erosion_deposition()

            # run the landscape evolution model for each rainfall record
            for row in precip:

                # update the elevation
                evol.dem=evolved_dem

                # update time
                evol.start=row[0]

                # derive excess water (mm/hr) from rain intensity (mm/hr) plus the product of depth (m) and the rainfall interval (min)
                gscript.run_command('r.mapcalc', expression="{rain_excess} = {rain_intensity}+(({depth}*(1/1000))*({rain_interval}*(1/60)))".format(rain_excess=rain_excess, rain_intensity=float(row[1]), depth=depth, rain_interval=self.rain_interval), overwrite=True)

                # update excess rainfall
                evol.rain_intensity = rain_excess

                # run model
                evolved_dem, time, depth = evol.erosion_deposition()
#                evolved_dem, time, depth = evol.flux()

                # register the evolved digital elevation model
                gscript.run_command('t.register', type=raster, input=self.strds, maps=evolved_dem, start=evol.start, increment=increment, flags='i', overwrite=True)

                # remove temporary maps
                gscript.run_command('g.remove', type='raster', name=['rain_excess'], flags='f')

            # compute net elevation change
            gscript.run_command('r.mapcalc', expression="{net_difference} = {dem}-{evolved_dem}".format(net_difference=net_difference, dem=self.dem, evolved_dem=evol.dem), overwrite=True)
            gscript.run_command('r.colors', map=net_difference, color='differences')

def cleanup():
    try:
        # remove temporary maps
        gscript.run_command('g.remove', type='raster', name=['rain_excess', 'rain', 'evolving_dem', 'dc', 'tc', 'tau', 'rho', 'dx', 'dy', 'grow_slope', 'grow_aspect', 'grow_dx', 'grow_dy'], flags='f')

    except CalledModuleError:
        pass

if __name__ == '__main__':

    # set input digital elevation model
    dem='dem'

    # set precipitation filepath
    precipitation=os.path.abspath("C://Users//Brendan//landscape_evolution//precipitation.txt")

    # set rainfall parameter
    rain_intensity=155 # mm/hr
    rain_duration=60 # total duration of the storm event in minutes
    rain_interval=1 # time interval in minutes

    # set temporal parameters
    temporaltype='absolute'
    strds='dynamics'
    title="dynamics"
    description="timeseries of digital elevation models simulated using a dynamic, process-based landscape evolution model of a single rainfall event"
    start="2015-10-06 00:00:00"

    # set model parameters
    walkers=10000  # max walkers = 7000000

    # set landscape parameters
    runoff=0.25 # runoff coefficient
    # 0.6 for bare earth
    # 0.35 for grass or crops
    # 0.5 for shrubs and trees
    # 0.25 for forest
    # 0.95 for roads
    mannings=0.04 # manning's roughness coefficient
    # 0.03 for bare earth
    # 0.04 for grass or crops
    # 0.06 for shrubs and trees
    # 0.1 for forest
    # 0.015 for roads
    detachment=0.01 # detachment coefficient
    transport=0.01 # transport coefficient
    shearstress=0 # shear stress coefficient
    density=1.4 # sediment mass density in g/cm^3
    mass=116 # mass of sediment per unit area in kg/m^2

    # set minimum and maximum values for erosion-deposition
    erdepmin=-1 # kg/m^2s
    erdepmax=1 # kg/m^2s

    # set minimum and maximum values for sediment flux
    fluxmin=-3 # kg/ms
    fluxmax=3 # kg/ms

    # create dynamic_evolution object
    event = DynamicEvolution(dem=dem, precipitation=precipitation, rain_intensity=rain_intensity, rain_duration=rain_duration, rain_interval=rain_interval, temporaltype=temporaltype, strds=strds, title=title, description=description, start=start, walkers=walkers, runoff=runoff, mannings=mannings, detachment=detachment, transport=transport, shearstress=shearstress, density=density, mass=mass, erdepmin=erdepmin, erdepmax=erdepmax, fluxmin=fluxmin, fluxmax=fluxmax)

    # run model
    dem = event.rainfall_event()
    dem = event.rainfall_series()

    atexit.register(cleanup)
    sys.exit(0)
