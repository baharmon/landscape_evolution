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
simulations = ['erdep','flux']

# set parameters
res = 0.3  # resolution of the region
nprocs = 5
threads = 5

precipitation = os.path.join(gisdbase, location, 'rain_events_2004_2016.csv')

# color rules
difference_colors = """\
-15000 100 0 100
-100 magenta
-10 red
-1 orange
-0.1 yellow
0 200 255 200
0.1 cyan
1 aqua
10 blue
100 0 0 100
15000 black
"""

def main():

    # try to install dependencies
    dependencies()

    # create mapsets and environments
    envs = create_environments(simulations)

    # create list of options for each simulation
    options_list = []

    # dictionary of parameters for erosion-deposition simulation
    erdep_params = {}
    erdep_params['elevation'] = 'elevation@erdep'
    erdep_params['runs'] = 'series'
    erdep_params['mode'] = 'simwe_mode'
    erdep_params['precipitation'] = precipitation
    erdep_params['start'] = "2004-01-01 00:00:00"
    erdep_params['walkers'] = 1000000
    erdep_params['grav_diffusion'] = 0.2
    erdep_params['threads'] = threads
    erdep_params['env'] = envs['erdep']
    # append dictionary to options list
    options_list.append(erdep_params)

    # dictionary of parameters for flux simulation
    flux_params = {}
    flux_params['elevation'] = 'elevation@flux'
    flux_params['runs'] = 'series'
    flux_params['mode'] = 'simwe_mode'
    flux_params['precipitation'] = precipitation
    flux_params['start'] = "2004-01-01 00:00:00"
    flux_params['walkers'] = 1000000
    flux_params['grav_diffusion'] = 0.2
    flux_params['transport_value'] = 100
    flux_params['detachment_value'] = 0.01
    flux_params['threads'] = threads
    flux_params['env'] = envs['flux']
    # append dictionary to options list
    options_list.append(flux_params)

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
            raster=['elevation_2004@PERMANENT','elevation'],
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
    env['GRASS_REGION'] = gscript.region_env(raster='elevation_2004@PERMANENT')
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

def render_2d(envs):

    # set rendering parameters
    brighten = 0  # percent brightness of shaded relief
    render_multiplier = 1  # multiplier for rendering size
    whitespace = 1.5
    fontsize = 36 * render_multiplier  # legend font size
    legend_coord = (10, 50, 1, 4)  # legend display coordinates
    zscale = 1

    # create rendering directory
    render = os.path.join(gisdbase, location, 'rendering')
    if not os.path.exists(render):
        os.makedirs(render)

    for mapset in simulations:

        # change mapset
        gscript.read_command('g.mapset',
            mapset=mapset,
            location=location)
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
        gscript.run_command('r.colors',
            map='net_difference',
            color='differences')
        # gscript.write_command('r.colors',
        #     map='net_difference',
        #     rules='-',
        #     stdin=difference_colors)
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

    # # try to remove temporary environment files
    # for simulation in simulations:
    #     try:
    #         os.remove(tmp_gisrc_files[simulation])
    #     except Exception as e:
    #         raise

if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())
