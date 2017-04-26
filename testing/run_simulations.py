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

# use temporary region
gscript.use_temp_region()

# set environment
env = gscript.gisenv()

overwrite = True
env['GRASS_OVERWRITE'] = overwrite
env['GRASS_VERBOSE'] = False
env['GRASS_MESSAGE_FORMAT'] = 'standard'
gisdbase = env['GISDBASE']
location = env['LOCATION_NAME']
mapset = env['MAPSET']

# set parameters
res = 0.3  # resolution of the region

# list of simulations to run
simulations = ['erdep','flux','transport','usped','rusle']

def main():

    # try to install dependencies
    dependencies()

    for simulation in simulations:

        # create mapset
        gscript.read_command('g.mapset',
            mapset=simulation,
            location=location,
            flags='c')

        # copy maps
        gscript.run_command('g.copy',
            raster=['elevation_30cm_2015@PERMANENT','elevation'],
            overwrite=overwrite)

        # set region
        gscript.run_command('g.region',
            raster='elevation',
            res=res)

        # get simulation function
        possibles = globals().copy()
        possibles.update(locals())
        method = possibles.get(simulation)
        if not method:
             raise NotImplementedError("Not implemented")
        # call simulation function
        method()

    atexit.register(cleanup)
    sys.exit(0)

def erdep():
    gscript.run_command('r.evolution',
        elevation='elevation',
        runs=event,
        mode=simwe_mode,
        rain_duration=1,
        rain_interval=1,
        start="2015-01-01 00:00:00")

def flux():
    gscript.run_command('r.evolution',
        elevation='elevation',
        runs=event,
        mode=simwe_mode,
        rain_duration=1,
        rain_interval=1,
        start="2015-01-01 00:00:00",
        transport_value=100)

def transport():
    gscript.run_command('r.evolution',
        elevation='elevation',
        runs=event,
        mode=simwe_mode,
        rain_duration=1,
        rain_interval=1,
        start="2015-01-01 00:00:00",
        detachment_value=1)

def usped():
    gscript.run_command('r.evolution',
        elevation='elevation',
        runs=event,
        mode=usped_mode,
        rain_duration=1,
        rain_interval=1,
        start="2015-01-01 00:00:00",
        n=1.2,
        m=1.5)

def rusle():
    gscript.run_command('r.evolution',
        elevation='elevation',
        runs=event,
        mode=rusle_mode,
        rain_duration=1,
        rain_interval=1,
        start="2015-01-01 00:00:00",
        n=1.2,
        m=0.5)

def erdep_with_landcover():
    gscript.run_command('g.copy',
        raster=['mannings_2014@PERMANENT','mannings_2014'],
        overwrite=overwrite)
    gscript.run_command('g.copy',
        raster=['runoff_2014@PERMANENT','runoff_2014'],
        overwrite=overwrite)
    gscript.run_command('r.evolution',
        elevation='elevation',
        runs=event,
        mode=simwe_mode,
        rain_duration=1,
        rain_interval=1,
        start="2015-01-01 00:00:00",
        mannings='mannings_2014',
        runoff='runoff_2014')

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
