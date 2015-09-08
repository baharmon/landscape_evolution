# -*- coding: utf-8 -*-

"""
@brief: landscape evolution model for gully formation

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

from grass.script import core as gcore

# small-scale landscape evolution model based on net erosion and deposition
def landscape(dem, walkers, rainintensity, stormduration, runoff, mannings, detachment, transport, shearstress, density, fluxmin, fluxmax):
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
    tlds='tlds'
    flux='flux'
    erdep='erdep'
    sedflux='sedflux'
    evolved_dem='evolved_dem'

    # set region
    gcore.run_command('g.region', rast=dem, res=1)

    # compute slope
    gcore.run_command('r.slope.aspect', elevation=dem, slope=slope, aspect=aspect, dx=dx, dy=dy, overwrite=True)

    # hyrdology parameters
    gcore.run_command('r.mapcalc', expression="{rain} = {rainintensity}*{runoff}".format(rain=rain, rainintensity=rainintensity,runoff=runoff), overwrite=True)

    # hydrologic simulation
    gcore.run_command('r.sim.water', elevation=dem, dx=dx, dy=dy, rain=rain, man=mannings, depth=depth, niterations=stormduration, nwalkers=walkers, overwrite=True)

    # erosion parameters
    gcore.run_command('r.mapcalc', expression="{dc} = {detachment}".format(dc=dc, detachment=detachment), overwrite=True)
    gcore.run_command('r.mapcalc', expression="{tc} = {transport}".format(tc=tc, transport=transport), overwrite=True)
    gcore.run_command('r.mapcalc', expression="{tau} = {shearstress}".format(tau=tau, shearstress=shearstress), overwrite=True)
    gcore.run_command('r.mapcalc', expression="{rho} = {density}*1000".format(rho=rho, density=density), overwrite=True) # convert g/cm^3 to kg/m^3

    # erosion-deposition simulation
    gcore.run_command('r.sim.sediment', elevation=dem, water_depth=depth, dx=dx, dy=dy, detachment_coeff=dc, transport_coeff=tc, shear_stress=tau, man=mannings, tlimit_erosion_deposition=tlds, flux=flux, erosion_deposition=erdep, niterations=stormduration, nwalkers=walkers, overwrite=True)

    # remove flux outliers
    gcore.run_command('r.mapcalc', expression="{sedflux} = if({flux} <{fluxmin},{fluxmin},if({flux}>{fluxmax},{fluxmax},{flux}))".format(sedflux=sedflux, flux=flux, fluxmin=fluxmin, fluxmax=fluxmax), overwrite=True)
    gcore.run_command('r.colors', map=sedflux, raster=flux)

    # evolve landscape
    """change in elevation (m) = change in time (s) * net erosion-deposition (kg/m^2s) / sediment mass density (kg/m^3)"""
    gcore.run_command('r.mapcalc', expression="{evolved_dem} = {dem}-({stormduration}*60*{erdep}/{rho})".format(evolved_dem=evolved_dem, dem=dem, stormduration=stormduration, erdep=erdep, rho=rho), overwrite=True)
    gcore.run_command('r.colors', map=evolved_dem, flags='e', color='elevation')


# detachment limited gully evolution model based on sediment flux
def gully(dem, walkers, rainintensity, stormduration, runoff, mannings, detachment, transport, shearstress, mass, fluxmin, fluxmax):
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
    tlds='tlds'
    flux='flux'
    erdep='erdep'
    sedflux='sedflux'
    evolved_dem='evolved_dem'

    # set region
    gcore.run_command('g.region', rast=dem, res=1)

    # compute slope
    gcore.run_command('r.slope.aspect', elevation=dem, slope=slope, aspect=aspect, dx=dx, dy=dy, overwrite=True)

    # hyrdology parameters
    gcore.run_command('r.mapcalc', expression="{rain} = {rainintensity}*{runoff}".format(rain=rain, rainintensity=rainintensity,runoff=runoff), overwrite=True)

    # hydrologic simulation
    gcore.run_command('r.sim.water', elevation=dem, dx=dx, dy=dy, rain=rain, man=mannings, depth=depth, niterations=stormduration, nwalkers=walkers, overwrite=True)

    # erosion parameters
    gcore.run_command('r.mapcalc', expression="{dc} = {detachment}".format(dc=dc, detachment=detachment), overwrite=True)
    gcore.run_command('r.mapcalc', expression="{tc} = {transport}".format(tc=tc, transport=transport), overwrite=True)
    gcore.run_command('r.mapcalc', expression="{tau} = {shearstress}".format(tau=tau, shearstress=shearstress), overwrite=True)
    gcore.run_command('r.mapcalc', expression="{rho} = {mass}".format(rho=rho, mass=mass), overwrite=True)

    # erosion-deposition simulation
    gcore.run_command('r.sim.sediment', elevation=dem, water_depth=depth, dx=dx, dy=dy, detachment_coeff=dc, transport_coeff=tc, shear_stress=tau, man=mannings, tlimit_erosion_deposition=tlds, flux=flux, erosion_deposition=erdep, niterations=stormduration, nwalkers=walkers, overwrite=True)

    # remove flux outliers
    gcore.run_command('r.mapcalc', expression="{sedflux} = if({flux} <{fluxmin},{fluxmin},if({flux}>{fluxmax},{fluxmax},{flux}))".format(sedflux=sedflux, flux=flux, fluxmin=fluxmin, fluxmax=fluxmax), overwrite=True)
    gcore.run_command('r.colors', map=sedflux, raster=flux)

    # evolve landscape
    """change in elevation (m) = change in time (s) * sediment flux (kg/ms) / mass of sediment per unit area (kg/m^2)"""
    gcore.run_command('r.mapcalc', expression="{evolved_dem} = {dem}-({stormduration}*60*{sedflux}/{rho})".format(evolved_dem=evolved_dem, dem=dem, stormduration=stormduration, sedflux=sedflux), overwrite=True)
    gcore.run_command('r.colors', map=evolved_dem, flags='e', color='elevation')


if __name__ == '__main__':

    # set input digital elevation model
    dem='dem'

    # set model parameters
    walkers=6500000  # max walkers = 7000000

    # set rainfall parameter
    rainintensity=155 # mm/hr
    stormduration=10 # minutes

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

    # run model
    landscape(dem=dem, walkers=walkers, rainintensity=rainintensity, stormduration=stormduration, runoff=runoff, mannings=mannings, detachment=detachment, transport=transport, shearstress=shearstress, density=density, fluxmin=fluxmin, fluxmax=fluxmax)

    # run detachment limited model
    # gully(dem=dem, walkers=walkers, rainintensity=rainintensity, stormduration=stormduration, runoff=runoff, mannings=mannings, detachment=detachment, transport=transport, shearstress=shearstress, mass=mass, fluxmin=fluxmin, fluxmax=fluxmax)
