# -*- coding: utf-8 -*-

"""
@brief: dynamic landscape evolution model

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

# TO DO:
#
# allow choice of maps or constants as inputs
# rain as list, inputs, or maps
# time as list or inputs
# convert both maps and constants' units
# option to compute mannings from difference between dem and dsm
# test with rain data
# write another module to run this class and create a timeseries of storms
# set min and max for erdep

import grass.script as gscript

import process

class = dynamic_evolution:
    def __init__(self, dem, start, rain_intensity, rain_duration, rain_interval, temporaltype, strds, title, description, start, walkers, runoff, mannings, detachment, transport, shearstress, density, mass, fluxmin, fluxmax):
        self.dem
        self.start
        self.rain_intensity
        self.rain_duration
        self.rain_interval
        self.temporaltype
        self.strds
        self.title
        self.description
        self.start
        self.walkers
        self.runoff
        self.mannings
        self.detachment
        self.transport
        self.shearstress
        self.density
        self.mass
        self.fluxmin
        self.fluxmax

    def rainfall_event(self):
        """a dynamic, process-based landscape evolution model of a single rainfall event that generates a timeseries of digital elevation models"""

        # assign local temporal variables
        datatype='strds'
        increment=str(rain_interval)+" minutes"
        raster='raster'

        # create a raster space time dataset
        gscript.run_command('t.create', type=datatype, temporaltype=temporaltype, output=strds, title=title, description=description)

        # register the initial digital elevation model
        gscript.run_command('t.register', type=raster, input=strds, maps=dem, start=start, increment=increment, flags='i')


        # run the landscape evolution model as a series of rainfall intervals in a rainfall event
        for i in range(iterations):

            # create evolution object
            evol = process.evolution(dem=dem, start=start, rain_intensity=rain_intensity, rain_interval=rain_interval, walkers=walkers, runoff=runoff, mannings=mannings, detachment=detachment, transport=transport, shearstress=shearstress, density=density, mass=mass, fluxmin=fluxmin, fluxmax=fluxmax)

            # run model
            evolved_dem = evol.erosion_deposition()

            # register the evolved digital elevation model
            gscript.run_command('t.register', type=raster, input=strds, maps=evolved_dem, start=start, increment=increment, flags='i')

            i = i+1

        return evolved_dem


if __name__ == '__main__':

    # set input digital elevation model
    dem='dem'

    # set rainfall parameter
    rain_intensity=155 # mm/hr
    rain_duration=60 # total duration of the storm event in minutes
    rain_interval=10 # time interval in minutes
    iterations=rain_duration/rain_interval

    # set temporal parameters
    temporaltype='absolute'
    strds='dynamics'
    title="dynamics"
    description="timeseries of digital elevation models simulated using a dynamic, process-based landscape evolution model of a single rainfall event"
    start="2010-01-01 00:00"


    # set model parameters
    walkers=6500000  # max walkers = 7000000

    # set landscape parameters
    runoff=0.25 # runoff coefficient
    mannings=0.1 # manning's roughness coefficient
    # 0.03 for bare earth
    # 0.04 for grass or crops
    # 0.06 for shrubs and trees
    # 0.1 for forest
    detachment=0.001 # detachment coefficient
    transport=0.01 # transport coefficient
    shearstress=0 # shear stress coefficient
    density=1.4 # sediment mass density in g/cm^3
    mass=116 # mass of sediment per unit area in kg/m^2

    # set minimum and maximum values for sediment flux
    fluxmin=-1 # kg/ms
    fluxmax=1 # kg/ms

    # create dynamic_evolution object
    event = dynamics.dynamic_evolution(dem=dem, start=start, rain_intensity=rain_intensity, rain_interval=rain_interval, temporaltype=temporaltype, strds=strds, title=title, description=description, raster=raster, start=start, walkers=walkers, runoff=runoff, mannings=mannings, detachment=detachment, transport=transport, shearstress=shearstress, density=density, mass=mass, fluxmin=fluxmin, fluxmax=fluxmax)

    # run model
    event.rainfall_event()
