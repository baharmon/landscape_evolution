# -*- coding: utf-8 -*-

"""
@brief: landscape evolution model

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

import grass.script as gscript

class evolution:
    def __init__(self, dem, start, rain_intensity, rain_interval, walkers, runoff, mannings, detachment, transport, shearstress, density, mass, erdepmin, erdepmax, fluxmin, fluxmax):
        self.dem = dem
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
    def erosion_deposition(self):
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
        time = self.start+self.rain_interval
        evolved_dem='dem_'+str(time)
        
        ## parse time
        #t = self.start.rsplit(":")
        #minutes = int(t[1])
        #t = t[0].rsplit()
        #hours = int(t[1])
        #time=self.start.replace(self.start[-2:],str(counter)).replace(" ","_").replace("-","_").replace(":","_")
        ## advance time
        #end_time = self.start.replace(self.start[-2:],str(counter))

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
        time = self.start+self.rain_interval
        evolved_dem='dem_'+time


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

    # set temporal parameters
    #start="2010-01-01 00:00"
    start=0

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
    evol = evolution(dem=dem, start=start, rain_intensity=rain_intensity, rain_interval=rain_interval, walkers=walkers, runoff=runoff, mannings=mannings, detachment=detachment, transport=transport, shearstress=shearstress, density=density, mass=mass, erdepmin=erdepmin, erdepmax=erdepmax, fluxmin=fluxmin, fluxmax=fluxmax)

    # run model
    evol.erosion_deposition()

    # run detachment limited model
    #evol.flux()
