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
from multiprocessing import Pool
import grass.script as gscript
from grass.exceptions import CalledModuleError

# set environment
env = gscript.gisenv()
gisdbase = env['GISDBASE']
location = env['LOCATION_NAME']

# list of simulations to run
simulations = [
    'bragg_ss_usped',
    'bragg_ss_rusle']

# set parameters
res = 10  # resolution of the region
region = 'fortbragg_elevation_10m_2012@PERMANENT'
nprocs = 6

def main():
    """install dependencies, create mapsets and environments,
    create dictionaries with params, and then run simulations in parallel"""

    # # try to install dependencies
    # dependencies()

    # create mapsets and environments
    envs = create_environments(simulations)

    # create list of options for each simulation
    options_list = []

    # dictionary of parameters for steady state usped simulation
    ss_usped_params = {}
    ss_usped_params['elevation'] = 'elevation@{simulation}'.format(
        simulation=simulations[0])
    ss_usped_params['runs'] = 'event'
    ss_usped_params['mode'] = 'usped_mode'
    ss_usped_params['rain_intensity'] = 50.0
    ss_usped_params['rain_duration'] = 60
    ss_usped_params['rain_interval'] = 60
    ss_usped_params['start'] = "2016-01-01 00:00:00"
    ss_usped_params['grav_diffusion'] = 0.0
    ss_usped_params['density_value'] = 1.6
    ss_usped_params['erdepmin'] = -0.25
    ss_usped_params['erdepmax'] = 0.25
    ss_usped_params['m'] = 1.5
    ss_usped_params['n'] = 1.2
    ss_usped_params['flags'] = 'f'
    ss_usped_params['env'] = envs['{simulation}'.format(
        simulation=simulations[0])]
    # append dictionary to options list
    options_list.append(ss_usped_params)

    # dictionary of parameters for rusle simulation
    ss_rusle_params = {}
    ss_rusle_params['elevation'] = 'elevation@{simulation}'.format(
        simulation=simulations[1])
    ss_rusle_params['runs'] = 'event'
    ss_rusle_params['mode'] = 'rusle_mode'
    ss_rusle_params['rain_intensity'] = 75.0
    ss_rusle_params['rain_duration'] = 60
    ss_rusle_params['rain_interval'] = 60
    ss_rusle_params['start'] = "2012-01-01 00:00:00"
    ss_rusle_params['grav_diffusion'] = 0.0
    ss_rusle_params['fluxmax'] = 0.25
    ss_rusle_params['m'] = 0.4
    ss_rusle_params['n'] = 1.3
    ss_rusle_params['flags'] = 'f'
    ss_rusle_params['env'] = envs['{simulation}'.format(
        simulation=simulations[1])]
    # append dictionary to options list
    options_list.append(ss_rusle_params)

    # run simulations in parallel
    parallel_simulations(options_list)
    atexit.register(cleanup)
    sys.exit(0)

def simulate(params):
    """run the dynamic landscape evolution model with the given parameters"""
    gscript.run_command('r.evolution', **params)

def create_environments(simulations):
    """generate environment settings and copy maps"""
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
    return envs

def parallel_simulations(options_list):
    """run simulations in parallel"""
    pool = Pool(nprocs)
    p = pool.map_async(simulate, options_list)
    try:
        p.get()
    except (KeyboardInterrupt, CalledModuleError):
        return

def getEnvironment(gisdbase, location, mapset):
    """Creates an environment to be passed in run_command.
    Returns a tuple with a temporary file path and an environment.
    The user should delete this temporary file."""
    tmp_gisrc_file = gscript.tempfile()
    with open(tmp_gisrc_file, 'w') as f:
        f.write('MAPSET: {mapset}\n'.format(mapset=mapset))
        f.write('GISDBASE: {g}\n'.format(g=gisdbase))
        f.write('LOCATION_NAME: {l}\n'.format(l=location))
        f.write('GUI: text\n')
    env = os.environ.copy()
    env['GISRC'] = tmp_gisrc_file
    env['GRASS_REGION'] = gscript.region_env(raster=region,res=res)
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

def cleanup():
    pass

if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())
