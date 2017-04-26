#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@brief: loop through mapsets

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
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
current_mapset = env['MAPSET']

def main():

    # loop through mapsets in location
    string = gscript.read_command('g.mapset',
        mapset=current_mapset,
        location=location,
        flags='l')
    mapsets = string.split()
    sets.remove('PERMANENT')

    for mapset in mapsets:
        gscript.read_command('g.mapset',
            mapset=mapset,
            location=location)

    atexit.register(cleanup)
    sys.exit(0)

def cleanup():
    pass

if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())
