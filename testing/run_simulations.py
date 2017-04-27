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

# list of simulations to run
simulations = ['erdep','flux','transport','usped','rusle']

def main():

    # # try to install dependencies
    # dependencies()

    # create mapsets and environments
    tmp_gisrc_files, envs = create_environments()

    # run simulations in parallel
    simulate(envs)

    atexit.register(cleanup(tmp_gisrc_files))
    sys.exit(0)

def erdep(envs):
    gscript.run_command('r.evolution',
        elevation='elevation@erdep',
        runs='event',
        mode='simwe_mode',
        rain_duration=1,
        rain_interval=1,
        start="2015-01-01 00:00:00",
        env=env['erdep'])

def flux(envs):
    gscript.run_command('r.evolution',
        elevation='elevation',
        runs='event',
        mode='simwe_mode',
        rain_duration=1,
        rain_interval=1,
        start="2015-01-01 00:00:00",
        transport_value=100,
        env=envs['flux'])

def transport(envs):
    gscript.run_command('r.evolution',
        elevation='elevation',
        runs='event',
        mode='simwe_mode',
        rain_duration=1,
        rain_interval=1,
        start="2015-01-01 00:00:00",
        detachment_value=1,
        env=envs['transport'])

def usped(envs):
    gscript.run_command('r.evolution',
        elevation='elevation',
        runs='event',
        mode='usped_mode',
        rain_duration=1,
        rain_interval=1,
        start="2015-01-01 00:00:00",
        n=1.2,
        m=1.5,
        env=env['usped'])

def rusle(envs):
    gscript.run_command('r.evolution',
        elevation='elevation',
        runs='event',
        mode='rusle_mode',
        rain_duration=1,
        rain_interval=1,
        start="2015-01-01 00:00:00",
        n=1.2,
        m=0.5,
        env=env['rusle'])

def erdep_with_landcover(envs):
    gscript.run_command('g.copy',
        raster=['mannings_2014@PERMANENT','mannings_2014'],
        env=env['erdep_with_landcover'])
    gscript.run_command('g.copy',
        raster=['runoff_2014@PERMANENT','runoff_2014'],
        env=env['erdep_with_landcover'])
    gscript.run_command('r.evolution',
        elevation='elevation',
        runs='event',
        mode='simwe_mode',
        rain_duration=1,
        rain_interval=1,
        start="2015-01-01 00:00:00",
        mannings='mannings_2014',
        runoff='runoff_2014',
        env=env['erdep_with_landcover'])

def create_environments():

    tmp_gisrc_files = {}
    envs = {}

    for simulation in simulations:

        # create mapset
        gscript.read_command('g.mapset',
            mapset=simulation,
            location=location,
            flags='c')

        # create env
        tmp_gisrc_file, env = getEnvironment(gisdbase, location, simulation)
        tmp_gisrc_files[simulation] = tmp_gisrc_file
        envs[simulation] = env

        # copy maps
        gscript.run_command('g.copy',
            raster=[reference_elevation,'elevation'],
            env=envs[simulation])

    return tmp_gisrc_files, envs

def simulate(envs):

    for simulation in simulations:

        # get simulation function
        possibles = globals().copy()
        possibles.update(locals())
        method = possibles.get(simulation,envs)
        if not method:
             raise NotImplementedError("Not implemented")

        # multiprocessing
        pool = Pool(nprocs)
        p = pool.map_async(method, envs)
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
    atexit.register(cleanup())
    sys.exit(main())
