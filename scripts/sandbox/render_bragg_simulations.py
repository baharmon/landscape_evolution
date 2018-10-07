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

# set 2D rendering parameters
legend_coord = (2, 32, 2, 4)
border = 400
width = 1600
height = 1600
fontsize = 24

# temporal paramters
end_time = '2012_01_01_01_00_00' #'2016_05_05_12_01_00' #2016_01_01_02_00_00'

def main():

    # # try to install dependencies
    # dependencies()

    # render 2d maps
    render_fortbragg_2d()

    atexit.register(cleanup)
    sys.exit(0)

def render_fortbragg_2d():

    # create rendering directory
    render = os.path.join(gisdbase, 'images', mapset)
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region', region='fortbragg', res=10)

    # compute relief
    gscript.run_command('r.relief',
        input='fortbragg_elevation_10m_2012@PERMANENT',
        output='relief',
        altitude=90,
        azimuth=45,
        zscale=3,
        overwrite=overwrite)

    # render net difference
    gscript.run_command('d.mon',
        start=driver,
        width=width+border,
        height=height,
        output=os.path.join(render, 'net_difference'+'.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief',
        color='net_difference',
        brighten=20,
        overwrite=overwrite)

    gscript.run_command('d.legend',
        raster='net_difference',
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

def dependencies():
    """try to install required add-ons"""
    try:
        gscript.run_command('g.extension',
            extension='r.geomorphon',
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
