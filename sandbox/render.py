#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@brief: rendering maps

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
mapset = env['MAPSET']

# set rendering directory
render = os.path.join(gisdbase, location, "rendering", mapset)

# set variables
res = 0.3  # resolution of the region
brighten = 0  # percent brightness of shaded relief
render_multiplier = 1  # multiplier for rendering size
whitespace = 1.5
fontsize = 36 * render_multiplier  # legend font size
legend_coord = (10, 50, 1, 4)  # legend display coordinates

# map name variables
elevation = 'elevation'
contours = 'contours'
step = 1
relief = 'relief'
zscale = 1
net_difference = 'net_difference'

# 3d variables
color_3d = "192:192:192"
res_3d = 1
height_3d = 2000
perspective = 15 #25
light_position = (0.68, -0.68, 0.95)
position = (1, 1)
zexag = 2
fringe = "se"
fringe_elevation = 50
format_3d = "tif"
size_3d = (1000, 1000)
# vpoint_size = 4
# vpoint_marker = "x"
# vpoint_color = "red"
# vline_width = 2
# vline_color = "black"
# arrow_position = (100, 100)
# arrow_size = 100

# color rules
difference_colors = """\
-15000 100 0 100
-100 magenta
-10 red
-1 orange
-0.1 yellow
0 200 255 200
0.1 cyan
1 aqua
10 blue
100 0 0 100
15000 black
"""

def main():

    # loop through mapsets with
    # g.mapset mapset=

    render_2d()
    # render_3d()
    atexit.register(cleanup)
    sys.exit(0)

def render_2d():

    # set region
    gscript.run_command('g.region',
        rast='elevation',
        res=res)
    info = gscript.parse_command('r.info',
        map=elevation,
        flags='g')
    width = int(info.cols)*render_multiplier*whitespace
    height = int(info.rows)*render_multiplier
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, net_difference+".png"),
        overwrite=overwrite)
    gscript.write_command('r.colors',
        map=net_difference,
        rules='-',
        stdin=difference_colors)
    gscript.run_command('r.relief',
        input='elevation',
        output=relief,
        altitude=90,
        azimuth=45,
        zscale=zscale,
        overwrite=overwrite)
    # gscript.run_command('r.contour',
    #     input=elevation,
    #     output=contours,
    #     step=step,
    #     overwrite=overwrite)
    gscript.run_command('d.shade',
        shade=relief,
        color=net_difference,
        brighten=brighten)
    # gscript.run_command('d.rast',
    #     map=net_difference)
    gscript.run_command('d.vect', map=contours, display="shape")
    gscript.run_command('d.legend',
        raster=net_difference,
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

def render_3d():

    gscript.run_command('g.region',
        rast='elevation',
        res=res)
    gscript.write_command('r.colors',
        map=net_difference,
        rules='-',
        stdin=difference_colors)
    gscript.run_command('m.nviz.image',
        elevation_map=elevation,
        color_map=net_difference,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        position=position,
        zexag=zexag,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        output=os.path.join(render, net_difference+'_3d'),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

def cleanup():
    # gscript.run_command('d.mon', stop=driver)
    pass

if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())
