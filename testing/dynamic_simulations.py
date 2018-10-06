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
    'erdep',
    'flux',
    'usped',
    'rusle']

# set parameters
res = 1  # resolution of the region
region = 'elevation_2012@PERMANENT'
nprocs = 4
threads = 3

def main():
    """install dependencies, create mapsets and environments,
    create dictionaries with params, and then run simulations in parallel"""

    # # try to install dependencies
    # dependencies()

    # create mapsets and environments
    envs = create_environments(simulations)

    # create list of options for each simulation
    options_list = []

    # dictionary of parameters for steady state erosion-deposition simulation
    erdep_params = {}
    erdep_params['elevation'] = 'elevation@{simulation}'.format(
        simulation=simulations[0])
    erdep_params['runs'] = 'event'
    erdep_params['mode'] = 'simwe_mode'
    erdep_params['rain_intensity'] = 50.0
    erdep_params['rain_duration'] = 120
    erdep_params['rain_interval'] = 3
    erdep_params['start'] = "2016-01-01 00:00:00"
    erdep_params['walkers'] = 1000000
    erdep_params['grav_diffusion'] = 0.05
    erdep_params['density_value'] = 1.6
    erdep_params['erdepmin'] = -0.25
    erdep_params['erdepmax'] = 0.25
    erdep_params['mannings'] = 'mannings'
    erdep_params['runoff'] = 'runoff'
    erdep_params['threads'] = threads
    erdep_params['flags'] = 'f'
    erdep_params['env'] = envs['{simulation}'.format(simulation=simulations[0])]
    # append dictionary to options list
    options_list.append(erdep_params)

    # dictionary of parameters for steady state flux simulation
    flux_params = {}
    flux_params['elevation'] = 'elevation@{simulation}'.format(
        simulation=simulations[1])
    flux_params['runs'] = 'event'
    flux_params['mode'] = 'simwe_mode'
    flux_params['rain_intensity'] = 150.0
    flux_params['rain_duration'] = 120
    flux_params['rain_interval'] = 3
    flux_params['start'] = "2016-01-01 00:00:00"
    flux_params['grav_diffusion'] = 0.05
    flux_params['density_value'] = 1.6
    flux_params['fluxmax'] = 0.25
    flux_params['detachment_value'] = 0.0001
    flux_params['transport_value'] = 0.01
    flux_params['mannings'] = 'mannings'
    flux_params['runoff'] = 'runoff'
    flux_params['threads'] = threads
    flux_params['flags'] = 'f'
    flux_params['env'] = envs['{simulation}'.format(
        simulation=simulations[1])]
    # append dictionary to options list
    options_list.append(flux_params)

    # dictionary of parameters for usped simulation
    usped_params = {}
    usped_params['elevation'] = 'elevation@{simulation}'.format(simulation=simulations[2])
    usped_params['runs'] = 'event'
    usped_params['mode'] = 'usped_mode'
    usped_params['rain_intensity'] = 50.0
    usped_params['rain_duration'] = 120
    usped_params['rain_interval'] = 3
    usped_params['start'] = "2016-01-01 00:00:00"
    usped_params['grav_diffusion'] = 0.05
    usped_params['erdepmin'] = -0.25
    usped_params['erdepmax'] = 0.25
    usped_params['density_value'] = 1.6
    usped_params['m'] = 1.5
    usped_params['n'] = 1.2
    usped_params['c_factor'] = 'c_factor'
    usped_params['k_factor'] = 'k_factor'
    usped_params['flags'] = 'f'
    usped_params['env'] = envs['{simulation}'.format(simulation=simulations[2])]
    # append dictionary to options list
    options_list.append(usped_params)

    # dictionary of parameters for rusle simulation
    rusle_params = {}
    rusle_params['elevation'] = 'elevation@{simulation}'.format(simulation=simulations[3])
    rusle_params['runs'] = 'event'
    rusle_params['mode'] = 'rusle_mode'
    rusle_params['rain_intensity'] = 50.0
    rusle_params['rain_duration'] = 120
    rusle_params['rain_interval'] = 3
    rusle_params['start'] = "2016-01-01 00:00:00"
    rusle_params['grav_diffusion'] = 0.05
    rusle_params['fluxmax'] = 0.25
    rusle_params['m'] = 0.4
    rusle_params['n'] = 1.3
    rusle_params['c_factor'] = 'c_factor'
    rusle_params['k_factor'] = 'k_factor'
    rusle_params['flags'] = 'f'
    rusle_params['env'] = envs['{simulation}'.format(simulation=simulations[3])]
    # append dictionary to options list
    options_list.append(rusle_params)

    # run simulations in parallel
    parallel_simulations(options_list)
    atexit.register(cleanup)
    sys.exit(0)

def simulate(params):
    """run the dynamic landscape evolution model with the given parameters"""
    gscript.run_command('r.sim.terrain', **params)

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
            extension='r.sim.terrain',
            operation='add',
            url='github.com/baharmon/landscape_evolution')
    except CalledModuleError:
        pass

def cleanup():
    pass

if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())
