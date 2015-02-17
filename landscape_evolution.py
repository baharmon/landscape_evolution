# -*- coding: utf-8 -*-

"""
@brief: landscape evolution model for gully formation

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

from grass.script import core as gcore


# landscape evolution model based on sediment flux
def gully_evolution(dem, walkers, rainintensity, stormduration, runoff, roughness, bare, detachment, transport, shearstress, fluxmin, fluxmax):
    """a process-based landscape evolution model using simulated sediment flux to carve a DEM"""
    
    # assign variables
    slope='slope'
    aspect='aspect'
    dx='dx'
    dy='dy'
    rain='rain'
    mannings='mannings'
    informal_trails='informal_trails'
    depth='depth'
    dc='dc'
    tc='tc'
    tau='tau'
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
    gcore.run_command('r.mapcalc', expression="{rain} = {rainintensity}*{runoff}155*0.25".format(rain=rain, rainintensity=rainintensity,runoff=runoff), overwrite=True)
    gcore.run_command('r.mapcalc', expression="{mannings} = if(isnull({informal_trails}),{roughness},{bare})".format(mannings=mannings, informal_trails=informal_trails, roughness=roughness, bare=bare), overwrite=True)
    
    # hydrologic simulation
    gcore.run_command('r.sim.water', elevation=dem, dx=dx, dy=dy, rain=rain, man=mannings, depth=depth, niterations=stormduration, nwalkers=walkers, overwrite=True)

    # erosion parameters
    gcore.run_command('r.mapcalc', expression="{dc} = {detachment}".format(dc=dc, detachment=detachment), overwrite=True)
    gcore.run_command('r.mapcalc', expression="{tc} = {transport}".format(tc=tc, transport=transport), overwrite=True)
    gcore.run_command('r.mapcalc', expression="{tau} = {shearstress}".format(tau=tau, shearstress=shearstress), overwrite=True)

    # erosion-deposition simulation
    gcore.run_command('r.sim.sediment', elevation=dem, water_depth=depth, dx=dx, dy=dy, detachment_coeff=dc, transport_coeff=tc, shear_stress=tau, man=mannings, tlimit_erosion_deposition=tlds, flux=flux, erosion_deposition=erdep, niterations=stormduration, nwalkers=walkers, overwrite=True)

    # remove flux outliers
    gcore.run_command('r.mapcalc', expression="{sedflux} = if({flux} <{fluxmin},{fluxmin},if({flux}>{fluxmax},{fluxmax},{flux}))".format(sedflux=sedflux, flux=flux, fluxmin=fluxmin, fluxmax=fluxmax), overwrite=True)
    gcore.run_command('r.colors', map=sedflux, raster=flux)
    
    # evolve landscape
    """change in elevation (m) = change in time (s) * sediment flux (kg/ms) / mass of sediment per unit area (kg/m^2)"""
    #gcore.run_command('r.mapcalc', expression="{evolved_dem} = {dem}-{sedflux}".format(evolved_dem=evolved_dem, dem=dem, sedflux=sedflux), overwrite=True)
    gcore.run_command('r.mapcalc', expression="{evolved_dem} = {dem}-({stormduration}*60*{sedflux}/116)".format(evolved_dem=evolved_dem, dem=dem, stormduration=stormduration, sedflux=sedflux), overwrite=True)
    gcore.run_command('r.colors', map=evolved_dem, flags='e', color='elevation')

if __name__ == '__main__':
    
    # set input digital elevation model
    dem='dem'
    
    # set model parameters
    walkers=6500000  # max walkers = 7000000
    #walkers=10000
    
    # set rainfall parameter
    rainintensity=155 # mm/hr
    stormduration=10 # minutes
    
    # set landscape parameters
    runoff=0.25 # runoff coefficient
    roughness=0.1 # manning's roughness coefficient
    bare=0.03  # manning's roughness coefficient for bare earth
    detachment=0.001 # detachment coefficient
    transport=0.01 # transport coefficient
    shearstress=0 # shear stress coefficient
    
    # set minimum and maximum values for sediment flux
    fluxmin=-1 # kg/ms 
    fluxmax=1 # kg/ms
    
    # run model
    gully_evolution(dem=dem, walkers=walkers, rainintensity=rainintensity, stormduration=stormduration, runoff=runoff, roughness=roughness, bare=bare, detachment=detachment, transport=transport, shearstress=shearstress, fluxmin=fluxmin, fluxmax=fluxmax)
    

































