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

def main():

    # render 2d maps
    render_region_2d(mapset)
    render_subregion_2d(mapset)

    # # render 3d maps
    # render_region_3d(mapset)
    # render_subregion_3d(mapset)

    atexit.register(cleanup)
    sys.exit(0)

def render_region_2d(mapset):
    """2D rendering of region"""

    # create rendering directory
    render = os.path.join(gisdbase, 'images', mapset)
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region',
        n=151030,
        s=150580,
        e=597645,
        w=597195,
        res=res)

    # render net difference with shaded relief
    gscript.run_command('d.mon',
        start=driver,
        width=width+border,
        height=height,
        output=os.path.join(render, 'net_difference'+'.png'),
        overwrite=overwrite)
    gscript.run_command('r.relief',
        input='elevation',
        output='relief',
        altitude=90,
        azimuth=45,
        zscale=3,
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief',
        color='net_difference',
        brighten=0)
    gscript.run_command('d.legend',
        raster='net_difference',
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)


def render_subregion_2d(mapset):

    # create rendering directory
    render = os.path.join(gisdbase, 'images', mapset)
    if not os.path.exists(render):
        os.makedirs(render)

    gscript.run_command('g.region',
        n=150870,
        s=150720,
        e=597440,
        w=597290,
        res=res)

    # render net difference with shaded relief
    gscript.run_command('d.mon',
        start=driver,
        width=width+border,
        height=height,
        output=os.path.join(render, 'gully_net_difference'+'.png'),
        overwrite=overwrite)
    gscript.run_command('r.relief',
        input='elevation',
        output='relief',
        altitude=90,
        azimuth=45,
        zscale=3,
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief',
        color='net_difference',
        brighten=0)
    gscript.run_command('d.legend',
        raster='net_difference',
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)


def render_region_3d(mapset):
    """3D rendering of region with nviz"""

    # set 3d rendering parameters
    camera_height = 750
    perspective = 15
    position = 1.0,1.0
    light_position = (0.68, -0.68, 0.95)
    fringe = "se"
    fringe_color = "255:255:245" #"244:244:244" #"254:246:232"
    fringe_elevation = 85
    size = (1600, 1200)
    zexag = 3

    # create rendering directory
    render = os.path.join(gisdbase, 'images', mapset+'_3d')
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region',
        n=151030,
        s=150580,
        e=597645,
        w=597195,
        res=res)

    # list of rasters to render
    rasters = ['net_difference']

    for raster in rasters:
        # 3D render raster
        gscript.run_command('m.nviz.image',
            elevation_map='elevation',
            color_map=raster,
            resolution_fine=1,
            height=camera_height,
            position=position,
            perspective=perspective,
            zexag=zexag,
            light_position=light_position,
            fringe=fringe,
            fringe_color=fringe_color,
            fringe_elevation=fringe_elevation,
            output=os.path.join(render,raster),
            format='tif',
            size=size,
            errors='ignore'
            )


def render_subregion_3d(mapset):
    """3D rendering of subregion with nviz"""

    # set 3d rendering parameters
    camera_height = 300
    perspective = 16
    position = 1.0,1.0
    light_position = (0.68, -0.68, 0.99)
    fringe = "se"
    fringe_color = "255:255:245" #"244:244:244" #"254:250:236"
    fringe_elevation = 94
    size = (1600, 1200)
    zexag = 3

    # create rendering directory
    render = os.path.join(gisdbase, 'images', mapset+'_3d')
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region',
        n=150870,
        s=150720,
        e=597440,
        w=597290,
        res=res)

    # list of rasters to render
    rasters = ['net_difference']

    for raster in rasters:
        # 3D render raster
        gscript.run_command('m.nviz.image',
            elevation_map='elevation',
            color_map=raster,
            resolution_fine=1,
            height=camera_height,
            position=position,
            perspective=perspective,
            zexag=zexag,
            light_position=light_position,
            fringe=fringe,
            fringe_color=fringe_color,
            fringe_elevation=fringe_elevation,
            output=os.path.join(render,'gully_'+raster),
            format='tif',
            size=size,
            errors='ignore'
            )


def cleanup():
    try:
        # stop cairo monitor
        gscript.run_command('d.mon', stop=driver)
    except CalledModuleError:
        pass

if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())
