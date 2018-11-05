#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AUTHOR:    Brendan Harmon <brendan.harmon@gmail.com>

PURPOSE:   Parallel processing of a dynamic landscape evolution model

COPYRIGHT: (C) 2017 Brendan Harmon

LICENSE:   This program is free software under the GNU General Public
           License (>=v2).
"""

import os
import sys
import atexit
import grass.script as gscript
from grass.exceptions import CalledModuleError
from multiprocessing import Pool

# set graphics driver
driver = "cairo"

# set environment
env = gscript.gisenv()
gisdbase = env['GISDBASE']
location = env['LOCATION_NAME']

# list of simulations to run
simulations = [
    'design_erdep',
    'design_flux']

# set parameters
res = 1  # resolution of the region
region = 'elevation_2012@PERMANENT'
nprocs = 5
threads = 2

design_storm = os.path.join(gisdbase, location, 'design_storm.txt')

def main():

    # try to install dependencies
    dependencies()

    # create mapsets and environments
    envs = create_environments(simulations)

    # create list of options for each simulation
    options_list = []

    # dictionary of parameters
    # for erosion-deposition simulation with a design storm
    design_erdep_params = {}
    design_erdep_params['elevation'] = 'elevation@design_erdep'
    design_erdep_params['runs'] = 'series'
    design_erdep_params['mode'] = 'simwe_mode'
    design_erdep_params['precipitation'] = design_storm
    design_erdep_params['rain_interval'] = 3
    design_erdep_params['start'] = "2016-01-01 00:00:00"
    design_erdep_params['walkers'] = 5000000
    design_erdep_params['grav_diffusion'] = 0.05
    design_erdep_params['mannings'] = 'mannings'
    design_erdep_params['runoff'] = 'runoff'
    design_erdep_params['threads'] = threads
    design_erdep_params['env'] = envs['design_erdep']
    # append dictionary to options list
    options_list.append(design_erdep_params)

    # dictionary of parameters
    # for flux simulation with a design storm
    design_flux_params = {}
    design_flux_params['elevation'] = 'elevation@design_flux'
    design_flux_params['runs'] = 'series'
    design_flux_params['mode'] = 'simwe_mode'
    design_flux_params['precipitation'] = design_storm
    design_flux_params['rain_interval'] = 3
    design_flux_params['start'] = "2016-01-01 00:00:00"
    design_flux_params['walkers'] = 5000000
    design_flux_params['detachment_value'] = 0.0001
    design_flux_params['transport_value'] = 0.01
    design_flux_params['grav_diffusion'] = 0.05
    design_flux_params['mannings'] = 'mannings'
    design_flux_params['runoff'] = 'runoff'
    design_flux_params['threads'] = threads
    design_flux_params['env'] = envs['design_flux']
    # append dictionary to options list
    options_list.append(design_flux_params)

    # run simulations in parallel
    parallel_simulations(options_list)

    # render maps
    render_2d(envs)

    atexit.register(cleanup)
    sys.exit(0)

def simulate(params):
    gscript.run_command('r.evolution', **params)

def create_environments(simulations):

    tmp_gisrc_files = {}
    envs = {}

    for mapset in simulations:

        # create mapset
        gscript.read_command('g.mapset',
            mapset=mapset,
            location=location,
            flags='c')

        # create env
        tmp_gisrc_file, env = getEnvironment(gisdbase, location, mapset)
        tmp_gisrc_files[mapset] = tmp_gisrc_file
        envs[mapset] = env

        # copy maps
        gscript.run_command('g.copy',
            raster=[region,'elevation'],
            env=envs[mapset])
        gscript.run_command('g.copy',
            raster=['mannings@PERMANENT','mannings'],
            env=envs[mapset])
        gscript.run_command('g.copy',
            raster=['runoff@PERMANENT','runoff'],
            env=envs[mapset])
        gscript.run_command('g.copy',
            raster=['c_factor@PERMANENT','c_factor'],
            env=envs[mapset])
        gscript.run_command('g.copy',
            raster=['k_factor@PERMANENT','k_factor'],
            env=envs[mapset])

    return envs

def parallel_simulations(options_list):

    # multiprocessing
    pool = Pool(nprocs)
    p = pool.map_async(simulate, options_list)
    try:
        p.get()
    except (KeyboardInterrupt, CalledModuleError):
        return

def getEnvironment(gisdbase, location, mapset):
    """Creates environment to be passed in run_command for example.
    Returns tuple with temporary file path and the environment. The user
    of this function is responsile for deleting the file."""
    tmp_gisrc_file = gscript.tempfile()
    with open(tmp_gisrc_file, 'w') as f:
        f.write('MAPSET: {mapset}\n'.format(mapset=mapset))
        f.write('GISDBASE: {g}\n'.format(g=gisdbase))
        f.write('LOCATION_NAME: {l}\n'.format(l=location))
        f.write('GUI: text\n')
    env = os.environ.copy()
    env['GISRC'] = tmp_gisrc_file
    env['GRASS_REGION'] = gscript.region_env(raster=region)
    env['GRASS_OVERWRITE'] = '1'
    env['GRASS_VERBOSE'] = '0'
    env['GRASS_MESSAGE_FORMAT'] = 'standard'
    return tmp_gisrc_file, env

def dependencies():
    """try to install required add-ons"""
    try:
        gscript.run_command('g.extension',
            extension='r.evolution',
            operation='add',
            url='github.com/baharmon/landscape_evolution')
    except CalledModuleError:
        pass

    try:
        gscript.run_command('g.extension',
            extension='r.sim.water.mp',
            operation='add')
    except CalledModuleError:
        pass

def render_2d(envs):

    brighten = 0  # percent brightness of shaded relief
    render_multiplier = 1  # multiplier for rendering size
    whitespace = 1.5 # canvas width relative to map for legend
    fontsize = 36 * render_multiplier  # legend font size
    legend_coord = (10, 50, 1, 4)  # legend display coordinates
    zscale = 1 # vertical exaggeration

    # create rendering directory
    render = os.path.join(gisdbase, location, 'rendering')
    if not os.path.exists(render):
        os.makedirs(render)

    for mapset in simulations:

        # change mapset
        gscript.read_command('g.mapset',
            mapset=mapset,
            location=location)

        # set region
        gscript.run_command('g.region', rast=region, res=res)

        # set render size
        info = gscript.parse_command('r.info',
            map='elevation',
            flags='g')
        width = int(info.cols)*render_multiplier*whitespace
        height = int(info.rows)*render_multiplier

        # render net difference
        gscript.run_command('d.mon',
            start=driver,
            width=width,
            height=height,
            output=os.path.join(render, mapset+'_'+'net_difference'+'.png'),
            overwrite=1)
        gscript.run_command('r.relief',
            input='elevation',
            output='relief',
            altitude=90,
            azimuth=45,
            zscale=zscale,
            env=envs[mapset])
        gscript.run_command('d.shade',
            shade='relief',
            color='net_difference',
            brighten=brighten)
        gscript.run_command('d.legend',
            raster='net_difference',
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

def cleanup():
    try:
        # stop cairo monitor
        gscript.run_command('d.mon', stop=driver)
    except CalledModuleError:
        pass

if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())