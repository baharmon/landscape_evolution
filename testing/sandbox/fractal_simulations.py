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
    'fractal_ss_erdep',
    'fractal_ss_flux',
    'fractal_ss_usped',
    'fractal_ss_rusle']

# set parameters
res = 1  # resolution of the region
region = 'elevation_2012@PERMANENT'
nprocs = 4
threads = 2

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
    ss_erdep_params = {}
    ss_erdep_params['elevation'] = 'elevation@{simulation}'.format(simulation=simulations[0])
    ss_erdep_params['runs'] = 'event'
    ss_erdep_params['mode'] = 'simwe_mode'
    ss_erdep_params['rain_intensity'] = 50.0
    ss_erdep_params['rain_duration'] = 120
    ss_erdep_params['rain_interval'] = 120
    ss_erdep_params['start'] = "2018-01-01 00:00:00"
    ss_erdep_params['walkers'] = 1000000
    ss_erdep_params['grav_diffusion'] = 0.05
    ss_erdep_params['threads'] = threads
    ss_erdep_params['flags'] = 'f'
    ss_erdep_params['env'] = envs['{simulation}'.format(simulation=simulations[0])]
    # append dictionary to options list
    options_list.append(ss_erdep_params)

    # dictionary of parameters for steady state flux simulation
    ss_flux_params = {}
    ss_flux_params['elevation'] = 'elevation@{simulation}'.format(simulation=simulations[1])
    ss_flux_params['runs'] = 'event'
    ss_flux_params['mode'] = 'simwe_mode'
    ss_flux_params['rain_intensity'] = 25.0
    ss_flux_params['rain_duration'] = 120
    ss_flux_params['rain_interval'] = 120
    ss_flux_params['start'] = "2018-01-01 00:00:00"
    ss_flux_params['grav_diffusion'] = 0.05
    ss_flux_params['detachment_value'] = 0.0001
    ss_flux_params['transport_value'] = 0.01
    ss_flux_params['threads'] = threads
    ss_flux_params['flags'] = 'f'
    ss_flux_params['env'] = envs['{simulation}'.format(simulation=simulations[1])]
    # append dictionary to options list
    options_list.append(ss_flux_params)

    # dictionary of parameters for steady state usped simulation
    ss_usped_params = {}
    ss_usped_params['elevation'] = 'elevation@{simulation}'.format(simulation=simulations[2])
    ss_usped_params['runs'] = 'event'
    ss_usped_params['mode'] = 'usped_mode'
    ss_usped_params['rain_intensity'] = 50.0
    ss_usped_params['rain_duration'] = 120
    ss_usped_params['rain_interval'] = 120
    ss_usped_params['start'] = "2016-01-01 00:00:00"
    ss_usped_params['grav_diffusion'] = 0.05
    ss_usped_params['flags'] = 'f'
    ss_usped_params['env'] = envs['{simulation}'.format(simulation=simulations[2])]
    # append dictionary to options list
    options_list.append(ss_usped_params)

    # dictionary of parameters for rusle simulation
    ss_rusle_params = {}
    ss_rusle_params['elevation'] = 'elevation@{simulation}'.format(simulation=simulations[3])
    ss_rusle_params['runs'] = 'event'
    ss_rusle_params['mode'] = 'rusle_mode'
    ss_rusle_params['rain_intensity'] = 75.0
    ss_rusle_params['rain_duration'] = 120
    ss_rusle_params['rain_interval'] = 120
    ss_rusle_params['start'] = "2018-01-01 00:00:00"
    ss_rusle_params['grav_diffusion'] = 0.05
    ss_rusle_params['flags'] = 'f'
    ss_rusle_params['env'] = envs['{simulation}'.format(simulation=simulations[3])]
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
        # set region
        gscript.run_command('g.region',
            n=151030,
            s=150580,
            e=597645,
            w=597195,
            res=res)
        gscript.run_command('r.surf.fractal ',
            output='elevation',
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
