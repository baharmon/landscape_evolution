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
end_time = '2000_01_01_02_00_00'

elevation_colors = """\
0% 0 132 132
-1250 0 191 191
-610 0 255 0
30 255 255 0
670 255 127 0
1310 191 127 63
1950 200 200 200
100% 200 200 200
nv white
default white
"""

def main():

    # # try to install dependencies
    # dependencies()

    # render 2d maps
    render_region_2d(mapset)

    # # render 3d maps
    # render_region_3d(mapset)

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
        n=150845,
        s=150745,
        e=597415,
        w=597315,
        res=res)


    # set elevation color table
    gscript.write_command(
        'r.colors',
        map='elevation_{time}'.format(time=end_time),
        rules='-',
        stdin=elevation_colors)

    # render shaded relief at start time
    gscript.run_command('d.mon',
        start=driver,
        width=width+border,
        height=height,
        output=os.path.join(render, 'elevation'+'.png'),
        overwrite=overwrite)
    gscript.run_command('r.relief',
        input='elevation',
        output='relief',
        altitude=90,
        azimuth=45,
        zscale=0.01,
        overwrite=overwrite)
    gscript.run_command('r.shade',
        shade='relief',
        color='elevation',
        output='shaded_relief',
        brighten=20,
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief',
        color='elevation',
        brighten=20,
        overwrite=overwrite)
    gscript.run_command('d.legend',
        raster='elevation',
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # compute and render shaded relief at end time
    gscript.run_command('d.mon',
        start=driver,
        width=width+border,
        height=height,
        output=os.path.join(render, 'evolved_elevation'+'.png'),
        overwrite=overwrite)
    gscript.run_command('r.relief',
        input='elevation_{time}'.format(time=end_time),
        output='relief',
        altitude=90,
        azimuth=45,
        zscale=0.01,
        overwrite=overwrite)
    gscript.run_command('r.shade',
        shade='relief',
        color='elevation_{time}'.format(time=end_time),
        output='shaded_relief',
        brighten=20,
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief',
        color='elevation_{time}'.format(time=end_time),
        brighten=20,
        overwrite=overwrite)
    gscript.run_command('d.legend',
        raster='elevation_{time}'.format(time=end_time),
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # render net difference
    gscript.run_command('d.mon',
        start=driver,
        width=width+border,
        height=height,
        output=os.path.join(render, 'net_difference'+'.png'),
        overwrite=overwrite)
    # gscript.read_command(
    #     'r.cpt2grass',
    #     map='net_difference',
    #     url='http://soliton.vm.bytemark.co.uk/pub/cpt-city/mpl/magma.cpt',
    #     flags='s')
    gscript.run_command('r.colors',
        map='net_difference',
        color='viridis',
        flags='e')
    gscript.run_command('d.rast',
        map='net_difference')
    gscript.run_command('d.legend',
        raster='net_difference',
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # render water depth with shaded relief
    gscript.run_command('d.mon',
        start=driver,
        width=width+border,
        height=height,
        output=os.path.join(render, 'depth'+'.png'),
        overwrite=overwrite)
    # gscript.run_command('d.shade',
    #     shade='relief',
    #     color='depth_{time}'.format(time=end_time),
    #     brighten=20)
    gscript.run_command('r.colors',
        map='depth_{time}'.format(time=end_time),
        color='water',
        flags='e')
    gscript.run_command('d.rast',
        map='depth_{time}'.format(time=end_time))
    gscript.run_command('d.legend',
        raster='depth_{time}'.format(time=end_time),
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # check for erosion-deposition
    find_raster = gscript.find_file('erosion_deposition_{time}'.format(time=end_time),
        element='cell')
    if find_raster['file']:
        # render erosion-deposition
        gscript.run_command('d.mon',
            start=driver,
            width=width+border,
            height=height,
            output=os.path.join(render, 'erdep'+'.png'),
            overwrite=overwrite)
        gscript.run_command('r.colors',
            map='erosion_deposition_{time}'.format(time=end_time),
            color='viridis',
            flags='e')
        gscript.run_command('d.rast',
            map='erosion_deposition_{time}'.format(time=end_time))
        gscript.run_command('d.legend',
            raster='erosion_deposition_{time}'.format(time=end_time),
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

    # check for flux
    find_raster = gscript.find_file('flux_{time}'.format(time=end_time),
        element='cell')
    if find_raster['file']:
        # render flux
        gscript.run_command('d.mon',
            start=driver,
            width=width+border,
            height=height,
            output=os.path.join(render, 'flux'+'.png'),
            overwrite=overwrite)
        gscript.run_command('r.colors',
            map='flux_{time}'.format(time=end_time),
            color='viridis',
            flags='e')
        # gscript.run_command('d.shade',
        #     shade='relief',
        #     color='flux_{time}'.format(time=end_time),
        #     brighten=20)
        gscript.run_command('d.rast',
            map='flux_{time}'.format(time=end_time))
        gscript.run_command('d.legend',
            raster='flux_{time}'.format(time=end_time),
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

def render_region_3d(mapset):
    """3D rendering of region with nviz"""

    # set 3d rendering parameters
    camera_height = 750
    perspective = 15
    position = 1.0, 1.0
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

def dependencies():
    """try to install required add-ons"""
    try:
        gscript.run_command('g.extension',
            extension='r.geomorphon',
            operation='add')
    except CalledModuleError:
        pass
    try:
        gscript.run_command('g.extension',
            extension='r.cpt2grass',
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
