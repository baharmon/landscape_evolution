#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@brief: run a set of landscape evolution simulations

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

import os
import sys
import atexit
import grass.script as gscript
from grass.exceptions import CalledModuleError
from multiprocessing import Pool

# set environment
env = gscript.gisenv()
gisdbase = env['GISDBASE']
location = env['LOCATION_NAME']

# set parameters
res = 3 #0.3  # resolution of the region
nprocs = 6

# set map variables
reference_elevation = 'elevation_30cm_2015@PERMANENT'

def main():

    # list of simulations to run
    simulations = ['erdep','flux','transport','usped','rusle']

    # # try to install dependencies
    # dependencies()

    # create mapsets and environments
    tmp_gisrc_files, envs = create_environments(simulations)

    # create list of options for each simulation
    options_list = []

    # dictionary of parameters for erosion-deposition simulation
    erdep_params = {}
    erdep_params['elevation'] = 'elevation@erdep'
    erdep_params['runs'] = 'event'
    erdep_params['mode'] = 'simwe_mode'
    erdep_params['rain_duration'] = 1
    erdep_params['rain_interval'] = 1
    erdep_params['start'] = "2015-01-01 00:00:00"
    erdep_params['walkers'] = 1000000
    erdep_params['grav_diffusion'] = 0.2
    erdep_params['transport_value'] = 0.01
    erdep_params['detachment_value'] = 0.01
    erdep_params['m'] = 1.5
    erdep_params['n'] = 1.2
    erdep_params['env'] = envs['erdep']
    # append dictionary to options list
    options_list.append(erdep_params)

    # dictionary of parameters for flux simulation
    flux_params = {}
    flux_params['elevation'] = 'elevation@flux'
    flux_params['runs'] = 'event'
    flux_params['mode'] = 'simwe_mode'
    flux_params['rain_duration'] = 1
    flux_params['rain_interval'] = 1
    flux_params['start'] = "2015-01-01 00:00:00"
    flux_params['walkers'] = 1000000
    flux_params['grav_diffusion'] = 0.2
    flux_params['transport_value'] = 100
    flux_params['detachment_value'] = 0.01
    flux_params['m'] = 1.5
    flux_params['n'] = 1.2
    flux_params['env'] = envs['flux']
    # append dictionary to options list
    options_list.append(flux_params)

    #print options_list


    # run simulations in parallel
    parallel_simulations(options_list)

    # atexit.register(cleanup())
    sys.exit(0)

def simulate(params):
    gscript.run_command('r.evolution', **params)

# def erdep(envs):
#     gscript.run_command('r.evolution',
#         elevation='elevation@erdep',
#         runs='event',
#         mode='simwe_mode',
#         rain_duration=1,
#         rain_interval=1,
#         start="2015-01-01 00:00:00",
#         env=envs['erdep'])

# def flux(envs):
#     gscript.run_command('r.evolution',
#         elevation='elevation',
#         runs='event',
#         mode='simwe_mode',
#         rain_duration=1,
#         rain_interval=1,
#         start="2015-01-01 00:00:00",
#         transport_value=100,
#         env=envs['flux'])

# def transport(envs):
#     gscript.run_command('r.evolution',
#         elevation='elevation',
#         runs='event',
#         mode='simwe_mode',
#         rain_duration=1,
#         rain_interval=1,
#         start="2015-01-01 00:00:00",
#         detachment_value=1,
#         env=envs['transport'])
#
# def usped(envs):
#     gscript.run_command('r.evolution',
#         elevation='elevation',
#         runs='event',
#         mode='usped_mode',
#         rain_duration=1,
#         rain_interval=1,
#         start="2015-01-01 00:00:00",
#         n=1.2,
#         m=1.5,
#         env=envs['usped'])
#
# def rusle(envs):
#     gscript.run_command('r.evolution',
#         elevation='elevation',
#         runs='event',
#         mode='rusle_mode',
#         rain_duration=1,
#         rain_interval=1,
#         start="2015-01-01 00:00:00",
#         n=1.2,
#         m=0.5,
#         env=envs['rusle'])
#
# def erdep_with_landcover(envs):
#     gscript.run_command('g.copy',
#         raster=['mannings_2014@PERMANENT','mannings_2014'],
#         env=env['erdep_with_landcover'])
#     gscript.run_command('g.copy',
#         raster=['runoff_2014@PERMANENT','runoff_2014'],
#         env=envs['erdep_with_landcover'])
#     gscript.run_command('r.evolution',
#         elevation='elevation',
#         runs='event',
#         mode='simwe_mode',
#         rain_duration=1,
#         rain_interval=1,
#         start="2015-01-01 00:00:00",
#         mannings='mannings_2014',
#         runoff='runoff_2014',
#         env=envs['erdep_with_landcover'])

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
            raster=[reference_elevation,'elevation'],
            env=envs[mapset])

    return tmp_gisrc_files, envs

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
    env['GRASS_REGION'] = gscript.region_env(raster=reference_elevation)
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

    # # try_remove temporary env files
    # # make global dictionary for temporary files
    # for simulation in simulations:
    #     try:
    #         os.remove(tmp_gisrc_files[simulation])
    #         pass
    #     except Exception as e:
    #         raise

if __name__ == "__main__":
    #atexit.register(cleanup())
    sys.exit(main())
