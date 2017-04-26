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

# define GRASS DATABASE
gisdb = os.path.join(os.path.expanduser("~"), "grassdata")

# specify (existing) location and mapset
location = "nc_spm_evolution"
mapset   = "PERMANENT"

# use temporary region
gscript.use_temp_region()

# set environment
env = gscript.gisenv()

overwrite = True
env['GRASS_OVERWRITE'] = overwrite
env['GRASS_VERBOSE'] = False
env['GRASS_MESSAGE_FORMAT'] = 'standard'
env['GISDBASE'] = gisdb
env['LOCATION_NAME'] = location
env['MAPSET'] = mapset
# gisdbase = env['GISDBASE']
# location = env['LOCATION_NAME']
# mapset = env['MAPSET']

# set parameters
res = 3 #0.3  # resolution of the region

# set map variables
reference_elevation = 'elevation_30cm_2015@PERMANENT'

# list of simulations to run
simulations = ['erdep','flux','transport','usped','rusle']

def main():

    # try to install dependencies
    dependencies()

    # set region
    gscript.run_command('g.region',
        raster=reference_elevation,
        res=res)

    for simulation in simulations:

        # create mapset
        gscript.read_command('g.mapset',
            mapset=simulation,
            location=location,
            flags='c')

        # copy maps
        gscript.run_command('g.copy',
            raster=[reference_elevation,'elevation'],
            overwrite=overwrite)

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
        runs='event',
        mode='simwe_mode',
        rain_duration=1,
        rain_interval=1,
        start="2015-01-01 00:00:00")

def flux():
    gscript.run_command('r.evolution',
        elevation='elevation',
        runs='event',
        mode='simwe_mode',
        rain_duration=1,
        rain_interval=1,
        start="2015-01-01 00:00:00",
        transport_value=100)

def transport():
    gscript.run_command('r.evolution',
        elevation='elevation',
        runs='event',
        mode='simwe_mode',
        rain_duration=1,
        rain_interval=1,
        start="2015-01-01 00:00:00",
        detachment_value=1)

def usped():
    gscript.run_command('r.evolution',
        elevation='elevation',
        runs='event',
        mode='usped_mode',
        rain_duration=1,
        rain_interval=1,
        start="2015-01-01 00:00:00",
        n=1.2,
        m=1.5)

def rusle():
    gscript.run_command('r.evolution',
        elevation='elevation',
        runs='event',
        mode='rusle_mode',
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
        runs='event',
        mode='simwe_mode',
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
