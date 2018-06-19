#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AUTHOR:    Brendan Harmon <brendan.harmon@gmail.com>

PURPOSE:   Rendering 2D and 3D maps of landscape evolution simulations

COPYRIGHT: (C) 2017 Brendan Harmon

LICENSE:   This program is free software under the GNU General Public
           License (>=v2).
"""

import os
import sys
import atexit
import grass.script as gscript
from grass.exceptions import CalledModuleError

# set graphics driver
driver = "cairo"

# temporary region
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
res=1

# parameters
elevation = "elevation_2016_01_01_01_00_00@{mapset}".format(mapset=mapset)
memory = 6000
depressionless = "depressionless_elevation"
direction = "direction"
mod = 6 #4
size = 6 #4

def main():

    # install dependencies
    dependencies()

    # set region
    gscript.run_command('g.region',
        n=151030,
        s=150580,
        e=597645,
        w=597195,
        res=res)

    # fill sinks
    sink_filling()

    # hydrologically condition
    hydro_conditioning()

    atexit.register(cleanup)
    sys.exit(0)

def sink_filling():
    """Fill sinks in digital elevation model"""
    gscript.run_command('r.fill.dir',
        input=elevation,
        output=depressionless,
        direction=direction,
        overwrite=overwrite)

    # remove temporary maps
    gscript.run_command(
        'g.remove',
        type='raster',
        name=['depressionless',
            'direction'],
        flags='f')

def hydro_conditioning():
    """Hydrologically condition digital elevation model using add-on module"""

    gscript.run_command('r.hydrodem',
        input=elevation,
        memory=memory,
        output=depressionless,
        mod=mod,
        size=size,
        flags='a',
        overwrite=overwrite)

def dependencies():
    """try to install required add-ons"""
    try:
        gscript.run_command('g.extension',
            extension='r.hydrodem',
            operation='add')
    except CalledModuleError:
        pass

def cleanup():
    try:
        # stop cairo monitor
        gscript.run_command('d.mon', stop=driver)
    except CalledModuleError:
        pass

if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())
