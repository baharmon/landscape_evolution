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
simulations = ['event_2','event_5','event_10','series_2','series_5','series_10']

# set parameters
res = 1  # resolution of the region
nprocs = 6
threads = 2

design_storm_2m = os.path.join(gisdbase, location, 'design_storm_2m.txt')
design_storm_5m = os.path.join(gisdbase, location, 'design_storm_5m.txt')
design_storm_10m = os.path.join(gisdbase, location, 'design_storm_10m.txt')

def main():

    # try to install dependencies
    dependencies()

    # create mapsets and environments
    envs = create_environments(simulations)

    # create list of options for each simulation
    options_list = []

    # dictionary of parameters for 2m event simulation
    event_2_params = {}
    event_2_params['elevation'] = 'elevation@event_2'
    event_2_params['runs'] = 'event'
    event_2_params['mode'] = 'simwe_mode'
    event_2_params['rain_intensity'] = 50.0
    event_2_params['rain_duration'] = 60
    event_2_params['rain_interval'] = 2
    event_2_params['start'] = "2015-01-01 00:00:00"
    event_2_params['walkers'] = 1000000
    event_2_params['grav_diffusion'] = 0.1
    event_2_params['mannings'] = 'mannings'
    event_2_params['runoff'] = 'runoff'
    event_2_params['threads'] = threads
    event_2_params['env'] = envs['event_2']
    # append dictionary to options list
    options_list.append(event_2_params)

    # dictionary of parameters for 5m event simulation
    event_5_params = {}
    event_5_params['elevation'] = 'elevation@event_5'
    event_5_params['runs'] = 'event'
    event_5_params['mode'] = 'simwe_mode'
    event_5_params['rain_intensity'] = 50.0
    event_5_params['rain_duration'] = 60
    event_5_params['rain_interval'] = 5
    event_5_params['start'] = "2015-01-01 00:00:00"
    event_5_params['walkers'] = 1000000
    event_5_params['grav_diffusion'] = 0.1
    event_5_params['mannings'] = 'mannings'
    event_5_params['runoff'] = 'runoff'
    event_5_params['threads'] = threads
    event_5_params['env'] = envs['event_5']
    # append dictionary to options list
    options_list.append(event_5_params)

    # dictionary of parameters for 10m event simulation
    event_10_params = {}
    event_10_params['elevation'] = 'elevation@event_10'
    event_10_params['runs'] = 'event'
    event_10_params['mode'] = 'simwe_mode'
    event_10_params['rain_intensity'] = 50.0
    event_10_params['rain_duration'] = 60
    event_10_params['rain_interval'] = 10
    event_10_params['start'] = "2015-01-01 00:00:00"
    event_10_params['walkers'] = 1000000
    event_10_params['grav_diffusion'] = 0.1
    event_10_params['mannings'] = 'mannings'
    event_10_params['runoff'] = 'runoff'
    event_10_params['threads'] = threads
    event_10_params['env'] = envs['event_10']
    # append dictionary to options list
    options_list.append(event_10_params)

    # dictionary of parameters for 2m series simulation
    series_2_params = {}
    series_2_params['elevation'] = 'elevation@series_2'
    series_2_params['runs'] = 'series'
    series_2_params['mode'] = 'simwe_mode'
    series_2_params['precipitation'] = design_storm_2m
    series_2_params['rain_interval'] = 2
    series_2_params['start'] = "2015-01-01 00:00:00"
    series_2_params['walkers'] = 1000000
    series_2_params['grav_diffusion'] = 0.1
    series_2_params['mannings'] = 'mannings'
    series_2_params['runoff'] = 'runoff'
    series_2_params['threads'] = threads
    series_2_params['env'] = envs['series_2']
    # append dictionary to options list
    options_list.append(series_2_params)

    # dictionary of parameters for 5m series simulation
    series_5_params = {}
    series_5_params['elevation'] = 'elevation@series_5'
    series_5_params['runs'] = 'series'
    series_5_params['mode'] = 'simwe_mode'
    series_5_params['precipitation'] = design_storm_5m
    series_5_params['rain_interval'] = 5
    series_5_params['start'] = "2015-01-01 00:00:00"
    series_5_params['walkers'] = 1000000
    series_5_params['grav_diffusion'] = 0.1
    series_5_params['mannings'] = 'mannings'
    series_5_params['runoff'] = 'runoff'
    series_5_params['threads'] = threads
    series_5_params['env'] = envs['series_5']
    # append dictionary to options list
    options_list.append(series_5_params)

    # dictionary of parameters for 10m series simulation
    series_10_params = {}
    series_10_params['elevation'] = 'elevation@series_10'
    series_10_params['runs'] = 'series'
    series_10_params['mode'] = 'simwe_mode'
    series_10_params['precipitation'] = design_storm_10m
    series_5_params['rain_interval'] = 10
    series_10_params['start'] = "2015-01-01 00:00:00"
    series_10_params['walkers'] = 1000000
    series_10_params['grav_diffusion'] = 0.1
    series_10_params['mannings'] = 'mannings'
    series_10_params['runoff'] = 'runoff'
    series_10_params['threads'] = threads
    series_10_params['env'] = envs['series_10']
    # append dictionary to options list
    options_list.append(series_10_params)

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
