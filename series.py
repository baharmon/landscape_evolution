# -*- coding: utf-8 -*-

"""
@brief: dynamic landscape evolution model

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

import grass.script as gscript

import dynamics

class EvolutionSeries:
    def __init__(self, dem, rain_intensity, rain_duration, rain_interval, temporaltype, strds, title, description, start, walkers, runoff, mannings, detachment, transport, shearstress, density, mass, erdepmin, erdepmax, fluxmin, fluxmax):
        self.dem = dem
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
        """To DO: add rain event data"""

    """TO DO: function to erase temporary maps"""
    #def remove_temporary_maps(self):

    def rainfall_series(self):
        """a dynamic, process-based landscape evolution model of a series of rainfall events that generates a timeseries of digital elevation models"""

        # assign local temporal variables
        datatype='strds'
        increment=str(self.rain_interval)+" minutes"
        raster='raster'
        iterations=self.rain_duration/self.rain_interval  
    
        # create a raster space time dataset
        gscript.run_command('t.create', type=datatype, temporaltype=self.temporaltype, output=self.strds, title=self.title, description=self.description, overwrite=True)

        # register the initial digital elevation model
        gscript.run_command('t.register', type=raster, input=self.strds, maps=self.dem, start=self.start, increment=increment, flags='i', overwrite=True)

        # create dynamic evolution object
        dyn = dynamics.DynamicEvolution(dem=self.dem, start=self.start, rain_intensity=self.rain_intensity, rain_interval=self.rain_interval, walkers=self.walkers, runoff=self.runoff, mannings=self.mannings, detachment=self.detachment, transport=self.transport, shearstress=self.shearstress, density=self.density, mass=self.mass, erdepmin=self.erdepmin, erdepmax=self.erdepmax, fluxmin=self.fluxmin, fluxmax=self.fluxmax)
        
        # run model
        evolved_dem, time = dyn.rainfall_series()

        # run the landscape evolution model as a series of rainfall intervals in a rainfall event
        i=1
        while i <= iterations:

            # update the elevation and time
            dyn.dem=evolved_dem
            print dyn.dem
            dyn.start=time
            print dyn.start

            # run model
            evolved_dem, time = dyn.rainfall_series()

            # register the evolved digital elevation model
            gscript.run_command('t.register', type=raster, input=self.strds, maps=evolved_dem, start=dyn.start, increment=increment, flags='i', overwrite=True)
            
            i=i+1

        return evolved_dem, time


if __name__ == '__main__':

    # set input digital elevation model
    dem='dem'

    """TO DO: parse list of rainfall events"""

    # set rainfall parameter
    rain_intensity=155 # mm/hr
    rain_duration=60 # total duration of the storm event in minutes
    rain_interval=10 # time interval in minutes

    # set temporal parameters
    temporaltype='absolute'
    strds='dynamics'
    title="dynamics"
    description="timeseries of digital elevation models simulated using a dynamic, process-based landscape evolution model of a single rainfall event"
    start="2010-01-01 00:00:00"

    # set model parameters
    walkers=10000  # max walkers = 7000000

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

    # set minimum and maximum values for erosion-deposition
    erdepmin=-3 # kg/m^2s
    erdepmax=3 # kg/m^2s

    # set minimum and maximum values for sediment flux
    fluxmin=-3 # kg/ms
    fluxmax=3 # kg/ms

    # create dynamic_evolution object
    series = EvolutionSeries(dem=dem, rain_intensity=rain_intensity, rain_duration=rain_duration, rain_interval=rain_interval, temporaltype=temporaltype, strds=strds, title=title, description=description, start=start, walkers=walkers, runoff=runoff, mannings=mannings, detachment=detachment, transport=transport, shearstress=shearstress, density=density, mass=mass, erdepmin=erdepmin, erdepmax=erdepmax, fluxmin=fluxmin, fluxmax=fluxmax)

    # run model
    dem = series.rainfall_series()
