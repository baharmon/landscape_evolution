# -*- coding: utf-8 -*-

"""
@brief: landscape evolution model

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

import grass.script as gscript

class = evolution:
    def __init__(self, dem, start, rain_intensity, rain_interval, walkers, runoff, mannings, detachment, transport, shearstress, density, mass, fluxmin, fluxmax):
        self.dem
        self.start
        self.rain_intensity
        self.rain_interval
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

    # small-scale landscape evolution model based on net erosion and deposition
    def erosion_deposition(self):
        """a process-based landscape evolution model using simulated erosion and deposition to carve a DEM"""

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
        erdep='erdep'
        time=self.start.replace(self.start[-2:],str(self.rain_interval))
        evolved_dem='dem_'+time

        # compute slope
        gscript.run_command('r.slope.aspect', elevation=self.dem, slope=slope, aspect=aspect, dx=dx, dy=dy, overwrite=True)

        # hyrdology parameters
        gscript.run_command('r.mapcalc', expression="{rain} = {rain_intensity}*{runoff}".format(rain=rain, rain_intensity=self.rain_intensity,runoff=self.runoff), overwrite=True)

        # hydrologic simulation
        gscript.run_command('r.sim.water', elevation=self.dem, dx=dx, dy=dy, rain=rain, man=self.mannings, depth=depth, niterations=self.rain_interval, nwalkers=self.walkers, overwrite=True)

        # erosion parameters
        gscript.run_command('r.mapcalc', expression="{dc} = {detachment}".format(dc=dc, detachment=self.detachment), overwrite=True)
        gscript.run_command('r.mapcalc', expression="{tc} = {transport}".format(tc=tc, transport=self.transport), overwrite=True)
        gscript.run_command('r.mapcalc', expression="{tau} = {shearstress}".format(tau=tau, shearstress=self.shearstress), overwrite=True)
        gscript.run_command('r.mapcalc', expression="{rho} = {density}*1000".format(rho=rho, density=self.density), overwrite=True) # convert g/cm^3 to kg/m^3

        # erosion-deposition simulation
        gscript.run_command('r.sim.sediment', elevation=self.dem, water_depth=depth, dx=dx, dy=dy, detachment_coeff=dc, transport_coeff=tc, shear_stress=tau, man=self.mannings, erosion_deposition=erdep, niterations=self.rain_interval, nwalkers=self.walkers, overwrite=True)

        # remove outliers
        #gscript.run_command('r.mapcalc', expression="{sedflux} = if({flux} <{fluxmin},{fluxmin},if({flux}>{fluxmax},{fluxmax},{flux}))".format(sedflux=sedflux, flux=flux, fluxmin=self.fluxmin, fluxmax=self.fluxmax), overwrite=True)
        #gscript.run_command('r.colors', map=sedflux, raster=flux)

        # evolve landscape
        """change in elevation (m) = change in time (s) * net erosion-deposition (kg/m^2s) / sediment mass density (kg/m^3)"""
        gscript.run_command('r.mapcalc', expression="{evolved_dem} = {dem}-({rain_interval}*60*{erdep}/{rho})".format(evolved_dem=evolved_dem, dem=self.dem, rain_interval=self.rain_interval, erdep=erdep, rho=rho), overwrite=True)
        gscript.run_command('r.colors', map=evolved_dem, flags='e', color='elevation')

        return evolved_dem

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
        time=self.start.replace(self.start[-2:],str(self.rain_interval))
        evolved_dem='dem_'+time

        # compute slope
        gscript.run_command('r.slope.aspect', elevation=self.dem, slope=slope, aspect=aspect, dx=dx, dy=dy, overwrite=True)

        # hyrdology parameters
        gscript.run_command('r.mapcalc', expression="{rain} = {rain_intensity}*{runoff}".format(rain=rain, rain_intensity=self.rain_intensity,runoff=self.runoff), overwrite=True)

        # hydrologic simulation
        gscript.run_command('r.sim.water', elevation=self.dem, dx=dx, dy=dy, rain=rain, man=self.mannings, depth=depth, niterations=self.rain_interval, nwalkers=self.walkers, overwrite=True)

        # erosion parameters
        gscript.run_command('r.mapcalc', expression="{dc} = {detachment}".format(dc=dc, detachment=self.detachment), overwrite=True)
        gscript.run_command('r.mapcalc', expression="{tc} = {transport}".format(tc=tc, transport=self.transport), overwrite=True)
        gscript.run_command('r.mapcalc', expression="{tau} = {shearstress}".format(tau=tau, shearstress=self.shearstress), overwrite=True)
        gscript.run_command('r.mapcalc', expression="{rho} = {mass}".format(rho=rho, mass=self.mass), overwrite=True)

        # erosion-deposition simulation
        gscript.run_command('r.sim.sediment', elevation=self.dem, water_depth=depth, dx=dx, dy=dy, detachment_coeff=dc, transport_coeff=tc, shear_stress=tau, man=self.mannings, flux=flux, niterations=self.rain_interval, nwalkers=self.walkers, overwrite=True)

        # remove flux outliers
        gscript.run_command('r.mapcalc', expression="{sedflux} = if({flux} <{fluxmin},{fluxmin},if({flux}>{fluxmax},{fluxmax},{flux}))".format(sedflux=sedflux, flux=flux, fluxmin=self.fluxmin, fluxmax=self.fluxmax), overwrite=True)
        gscript.run_command('r.colors', map=sedflux, raster=flux)

        # evolve landscape
        """change in elevation (m) = change in time (s) * sediment flux (kg/ms) / mass of sediment per unit area (kg/m^2)"""
        gscript.run_command('r.mapcalc', expression="{evolved_dem} = {dem}-({rain_interval}*60*{sedflux}/{rho})".format(evolved_dem=evolved_dem, dem=self.dem, rain_interval=self.rain_interval, sedflux=sedflux), overwrite=True)
        gscript.run_command('r.colors', map=evolved_dem, flags='e', color='elevation')

        return evolved_dem

if __name__ == '__main__':

    # set input digital elevation model
    dem='dem'

    # set temporal parameters
    start="2010-01-01 00:00"

    # set model parameters
    walkers=6500000  # max walkers = 7000000

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

    # set minimum and maximum values for sediment flux
    fluxmin=-1 # kg/ms
    fluxmax=1 # kg/ms

    # create evolution object
    evol = process.evolution(dem=dem, start=start, rain_intensity=rain_intensity, rain_interval=rain_interval, walkers=walkers, runoff=runoff, mannings=mannings, detachment=detachment, transport=transport, shearstress=shearstress, density=density, mass=mass, fluxmin=fluxmin, fluxmax=fluxmax)

    # run model
    evol.erosion_deposition()

    # run detachment limited model
    #evol.flux()
