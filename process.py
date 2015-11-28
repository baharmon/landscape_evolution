# -*- coding: utf-8 -*-

"""
@brief: landscape evolution model

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

import grass.script as gscript
import datetime

class Evolution:
    def __init__(self, dem, precipitation, start, rain_intensity, rain_interval, walkers, runoff, mannings, detachment, transport, shearstress, density, mass, erdepmin, erdepmax, fluxmin, fluxmax):
        self.dem = dem
        self.precipitation = precipitation
        self.start = start
        self.rain_intensity = rain_intensity
        self.rain_interval = rain_interval
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

    # small-scale landscape evolution model based on net erosion and deposition
    def erosion_deposition(self, ):
        """a process-based landscape evolution model using simulated erosion and deposition to carve a DEM"""

        # assign variables
        slope = 'slope'
        aspect = 'aspect'
        dx = 'dx'
        dy = 'dy'
        rain = 'rain'
        depth = 'depth'
        dc = 'dc'
        tc = 'tc'
        tau = 'tau'
        rho = 'rho'
        erdep = 'erdep'
        flux = 'flux'
        erosion_deposition = 'erosion_deposition'

        # parse time
        year=int(self.start[:4])
        month=int(self.start[5:7])
        day=int(self.start[8:10])
        hours=int(self.start[11:13])
        minutes=int(self.start[14:16])
        seconds=int(self.start[17:19])
        time = datetime.datetime(year,month,day,hours,minutes,seconds)
        
        # advance time
        time = time + datetime.timedelta(minutes = self.rain_interval)
        time = time.isoformat(" ")

        # timestamp
        evolved_dem='dem_'+time.replace(" ","_").replace("-","_").replace(":","_")

        # compute slope
        gscript.run_command('r.param.scale', input=self.dem, output=slope, size=9, method="slope", overwrite=True)
        gscript.run_command('r.param.scale', input=self.dem, output=aspect, size=9, method="aspect", overwrite=True)

        # hyrdology parameters
        gscript.run_command('r.mapcalc', expression="{rain} = {rain_intensity}*{runoff}".format(rain=rain, rain_intensity=self.rain_intensity,runoff=self.runoff), overwrite=True)

        # hydrologic simulation
        gscript.run_command('r.sim.water', elevation=self.dem, dx=dx, dy=dy, rain=rain, man_value=self.mannings, depth=depth, niterations=self.rain_interval, nwalkers=self.walkers, overwrite=True)

        # erosion parameters
        gscript.run_command('r.mapcalc', expression="{dc} = {detachment}".format(dc=dc, detachment=self.detachment), overwrite=True)
        gscript.run_command('r.mapcalc', expression="{tc} = {transport}".format(tc=tc, transport=self.transport), overwrite=True)
        gscript.run_command('r.mapcalc', expression="{tau} = {shearstress}".format(tau=tau, shearstress=self.shearstress), overwrite=True)
        gscript.run_command('r.mapcalc', expression="{rho} = {density}*1000".format(rho=rho, density=self.density), overwrite=True) # convert g/cm^3 to kg/m^3

        # erosion-deposition simulation
        gscript.run_command('r.sim.sediment', elevation=self.dem, water_depth=depth, dx=dx, dy=dy, detachment_coeff=dc, transport_coeff=tc, shear_stress=tau, man_value=self.mannings, erosion_deposition=erdep, sediment_flux=flux, niterations=self.rain_interval, nwalkers=self.walkers, overwrite=True)

        # filter outliers
        gscript.run_command('r.mapcalc', expression="{erosion_deposition} = if({erdep}<{erdepmin},{erdepmin},if({erdep}>{erdepmax},{erdepmax},{erdep}))".format(erosion_deposition=erosion_deposition, erdep=erdep, erdepmin=self.erdepmin, erdepmax=self.erdepmax), overwrite=True)
        gscript.run_command('r.colors', map=erosion_deposition, raster=erdep)

        # evolve landscape
        """change in elevation (m) = change in time (s) * net erosion-deposition (kg/m^2s) / sediment mass density (kg/m^3)"""
        gscript.run_command('r.mapcalc', expression="{evolved_dem} = {dem}-({rain_interval}*60*{erosion_deposition}/{rho})".format(evolved_dem=evolved_dem, dem=self.dem, rain_interval=self.rain_interval, erosion_deposition=erosion_deposition, rho=rho), overwrite=True)
        gscript.run_command('r.colors', map=evolved_dem, flags='e', color='elevation')

        return evolved_dem, time

    # detachment limited gully evolution model based on sediment flux
    def flux(self):
        """a process-based landscape evolution model using simulated sediment flux to carve a DEM"""

        # assign variables
        slope='slope'
        aspect='aspect'
        dx='dx'
        dy='dy'
        rain='rain'
        depth='depth'
        dc='dc'
        tc='tc'
        tau='tau'
        rho='rho'
        flux='flux'
        sedflux='sedflux'       

        # parse time
        year=int(self.start[:4])
        month=int(self.start[5:7])
        day=int(self.start[8:10])
        hours=int(self.start[11:13])
        minutes=int(self.start[14:16])
        seconds=int(self.start[17:19])
        time = datetime.datetime(year,month,day,hours,minutes,seconds)
        
        # advance time
        time = time + datetime.timedelta(minutes = self.rain_interval)
        time = time.isoformat(" ")

        # timestamp
        evolved_dem='dem_'+time.replace(" ","_").replace("-","_").replace(":","_")

        # compute slope
        gscript.run_command('r.slope.aspect', elevation=self.dem, slope=slope, aspect=aspect, dx=dx, dy=dy, overwrite=True)

        # hyrdology parameters
        gscript.run_command('r.mapcalc', expression="{rain} = {rain_intensity}*{runoff}".format(rain=rain, rain_intensity=self.rain_intensity,runoff=self.runoff), overwrite=True)

        # hydrologic simulation
        gscript.run_command('r.sim.water', elevation=self.dem, dx=dx, dy=dy, rain=rain, man_value=self.mannings, depth=depth, niterations=self.rain_interval, nwalkers=self.walkers, overwrite=True)

        # erosion parameters
        gscript.run_command('r.mapcalc', expression="{dc} = {detachment}".format(dc=dc, detachment=self.detachment), overwrite=True)
        gscript.run_command('r.mapcalc', expression="{tc} = {transport}".format(tc=tc, transport=self.transport), overwrite=True)
        gscript.run_command('r.mapcalc', expression="{tau} = {shearstress}".format(tau=tau, shearstress=self.shearstress), overwrite=True)
        gscript.run_command('r.mapcalc', expression="{rho} = {mass}".format(rho=rho, mass=self.mass), overwrite=True)

        # erosion-deposition simulation
        gscript.run_command('r.sim.sediment', elevation=self.dem, water_depth=depth, dx=dx, dy=dy, detachment_coeff=dc, transport_coeff=tc, shear_stress=tau, man_value=self.mannings, sediment_flux=flux, niterations=self.rain_interval, nwalkers=self.walkers, overwrite=True)

        # filter outliers
        gscript.run_command('r.mapcalc', expression="{sedflux} = if({flux}<{fluxmin},{fluxmin},if({flux}>{fluxmax},{fluxmax},{flux}))".format(sedflux=sedflux, flux=flux, fluxmin=self.fluxmin, fluxmax=self.fluxmax), overwrite=True)
        gscript.run_command('r.colors', map=sedflux, raster=flux)

        # evolve landscape
        """change in elevation (m) = change in time (s) * sediment flux (kg/ms) / mass of sediment per unit area (kg/m^2)"""
        gscript.run_command('r.mapcalc', expression="{evolved_dem} = {dem}-({rain_interval}*60*{sedflux}/{rho})".format(evolved_dem=evolved_dem, dem=self.dem, rain_interval=self.rain_interval, sedflux=sedflux), overwrite=True)
        gscript.run_command('r.colors', map=evolved_dem, flags='e', color='elevation')

        return evolved_dem, time

if __name__ == '__main__':

    # set input digital elevation model
    dem='dem'

    # set precipitation filepath
    precipitation="Harmon_Brendan_LAKE_Minute_Precip.txt"
    
    # set temporal parameters
    start="2010-01-01 00:00:00"

    # set model parameters
    walkers=10000  # max walkers = 7000000

    # set rainfall parameter
    rain_intensity=155 # mm/hr
    rain_interval=10 # minutes

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

    # create evolution object
    evol = Evolution(dem=dem, precipitation=precipitation, start=start, rain_intensity=rain_intensity, rain_interval=rain_interval, walkers=walkers, runoff=runoff, mannings=mannings, detachment=detachment, transport=transport, shearstress=shearstress, density=density, mass=mass, erdepmin=erdepmin, erdepmax=erdepmax, fluxmin=fluxmin, fluxmax=fluxmax)

    # run model
    evol.erosion_deposition()

    # run detachment limited model
    #evol.flux()
