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
end_time = '2016_01_01_02_00_00'
# end_time = '2012_01_01_02_00_00'  # params for fort braggw
elevation_colors = """\
0% 0 132 132
89 0 191 191
93.6 0 255 0
98.2 255 255 0
102.8 255 127 0
107.4 191 127 63
112 200 200 200
100% 200 200 200
nv white
default white
"""

def main():
    """try to install dependencies"""
    # dependencies()

    """render maps"""
    render_region_2d(mapset)
    render_region_3d(mapset)
    # render_fortbragg_2d()

    atexit.register(cleanup)
    sys.exit(0)

def render_region_2d(mapset):
    """2D rendering of region"""

    # create rendering directory
    render = os.path.join(gisdbase, 'images', mapset)
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region', region='region', res=res)

    # set mask
    gscript.run_command('r.mask', vector='watershed')

    # set elevation color table
    gscript.write_command(
        'r.colors',
        map='elevation_{time}'.format(time=end_time),
        rules='-',
        stdin=elevation_colors)

    # compute and render shaded relief
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'shaded_relief'+'.png'),
        overwrite=overwrite)
    gscript.run_command('r.relief',
        input='elevation_{time}'.format(time=end_time),
        output='relief',
        altitude=90,
        azimuth=45,
        zscale=3,
        overwrite=overwrite)
    gscript.run_command('r.skyview',
        input='elevation_{time}'.format(time=end_time),
        output='skyview',
        ndir=16,
        colorized_output='colorized_skyview',
        overwrite=overwrite)
    gscript.run_command('r.shade',
        shade='relief',
        color='skyview',
        output='shaded_relief',
        brighten=50,
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief',
        color='colorized_skyview',
        brighten=10,
        overwrite=overwrite)
    gscript.run_command('d.legend',
        raster='elevation_{time}'.format(time=end_time),
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # render net difference
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'net_difference'+'.png'),
        overwrite=overwrite)
    gscript.run_command('d.rast',
        map='net_difference')
    gscript.run_command('d.legend',
        raster='net_difference',
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

# compute and render landforms
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'landforms'+'.png'),
        overwrite=overwrite)
    gscript.run_command('r.geomorphon',
        elevation='elevation_{time}'.format(time=end_time),
        forms='landforms',
        search=64,
        skip=0,
        flat=1,
        dist=0,
        step=0,
        start=0,
        overwrite=overwrite)
    gscript.run_command('d.rast',
        map='landforms')
    gscript.run_command('d.legend',
        raster='landforms',
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # render water depth with shaded relief
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'depth'+'.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='shaded_relief',
        color='depth_{time}'.format(time=end_time),
        brighten=20)
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
            width=width,
            height=height,
            output=os.path.join(render, 'erdep'+'.png'),
            overwrite=overwrite)
        gscript.run_command('d.shade',
            shade='shaded_relief',
            color='erosion_deposition_{time}'.format(time=end_time),
            brighten=20)
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
            width=width,
            height=height,
            output=os.path.join(render, 'flux'+'.png'),
            overwrite=overwrite)
        gscript.run_command('r.colors',
            map='flux_{time}'.format(time=end_time),
            color='viridis',
            flags='e')
        gscript.run_command('d.shade',
            shade='shaded_relief',
            color='flux_{time}'.format(time=end_time),
            brighten=20)
        gscript.run_command('d.legend',
            raster='flux_{time}'.format(time=end_time),
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

    # remove mask
    gscript.run_command('r.mask', flags='r')

def render_fortbragg_2d():

    # create rendering directory
    render = os.path.join(gisdbase, 'images', mapset)
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region', region='fortbragg', res=10)

    # set mask
    gscript.run_command('r.mask', raster='fortbragg_cfactor')

    # compute relief
    gscript.run_command('r.relief',
        input='fortbragg_elevation_10m_2012',
        output='relief',
        altitude=90,
        azimuth=45,
        zscale=3,
        overwrite=overwrite)

    # compute skyview
    gscript.run_command('r.skyview',
        input='fortbragg_elevation_10m_2012',
        output='skyview',
        ndir=16,
        colorized_output='colorized_skyview',
        overwrite=overwrite)

    # render net difference
    gscript.run_command('d.mon',
        start=driver,
        width=width*2,
        height=height,
        output=os.path.join(render, 'net_difference'+'.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='skyview',
        color='net_difference',
        brighten=20,
        overwrite=overwrite)

    gscript.run_command('d.legend',
        raster='net_difference',
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # remove mask
    gscript.run_command('r.mask', flags='r')

def render_region_3d(mapset):
    """3D rendering of region with nviz"""

    # set 3d rendering parameters
    camera_height = 750
    perspective = 15
    position = 1.0, 1.0
    light_position = (0.68, -0.68, 0.95)
    fringe = "se"
    fringe_color = "255:255:255"
    fringe_elevation = 85
    size = (1200, 1200)
    zexag = 3
    vwidth = 3

    # create rendering directory
    render = os.path.join(gisdbase, 'images', mapset+'_3d')
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region',
                        region='region',
                        res=res)

    # mask rasters
    gscript.run_command('r.mask', vector='watershed')
    gscript.run_command('r.mapcalc',
        expression="depth = {raster}".format(raster='depth_'+end_time),
        overwrite=True)
    find_raster = gscript.find_file('flux_{time}'.format(time=end_time),
        element='cell')
    if find_raster['file']:
        gscript.run_command('r.mapcalc',
            expression="flux = {raster}".format(raster='flux_'+end_time),
            overwrite=True)
    find_raster = gscript.find_file('erosion_deposition_{time}'.format(time=end_time),
        element='cell')
    if find_raster['file']:
        gscript.run_command('r.mapcalc',
            expression="erosion_deposition = {raster}".format(raster='erosion_deposition_'+end_time),
            overwrite=True)
    gscript.run_command('r.mapcalc',
        expression="difference = {raster}".format(raster='net_difference'),
        overwrite=True)
    gscript.run_command('r.mask', flags='r')

    # list of rasters to render
    rasters = ['elevation_'+end_time,
        'colorized_skyview',
        'landforms',
        'depth',
        'flux',
        'erosion_deposition',
        'difference']

    for raster in rasters:

        # check if raster exists
        find_raster = gscript.find_file(raster,
            element='cell')
        if find_raster['file']:

            # 3D render raster
            gscript.run_command('m.nviz.image',
                elevation_map='elevation_'+end_time,
                color_map=raster,
                resolution_fine=1,
                vline='watershed',
                vline_width=vwidth,
                vline_color='black',
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

            # render legend
            gscript.run_command('r.out.legend',
                raster=raster,
                file=os.path.join(render,'legend_'+raster+'.png'),
                dimensions=[50,400],
                unit='px',
                resolution='300',
                color='none',
                digits=4,
                fontsize=6,
                overwrite=overwrite)

    # remove temporary maps
    gscript.run_command(
        'g.remove',
        type='raster',
        name=['depth',
            'erdep',
            'flux',
            'difference'],
        flags='f')

def dependencies():
    """try to install required add-ons"""
    try:
        gscript.run_command('g.extension',
            extension='r.skyview',
            operation='add')
    except CalledModuleError:
        pass
    try:
        gscript.run_command('g.extension',
            extension='r.geomorphon',
            operation='add')
    except CalledModuleError:
        pass
    try:
        gscript.run_command('g.extension',
            extension='r.out.legend',
            operation='add')
    except CalledModuleError:
        pass

def cleanup():
    try:
        # stop cairo monitor
        gscript.run_command('d.mon', stop=driver)
    except CalledModuleError:
        pass
    try:
        # remove mask
        gscript.run_command('r.mask', flags='r')
    except CalledModuleError:
        pass

if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())
