#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AUTHOR:    Brendan Harmon <brendan.harmon@gmail.com>

PURPOSE:   Rendering 2D and 3D maps of landscape evolution model sample data

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
res=0.3

# set 2D rendering parameters
legend_coord = (2, 32, 2, 4)
border = 400
width = 1600
height = 1600
fontsize = 24

# set data parameters
years = [2004, 2012, 2016]


def main():

    # render 2d maps
    render_region_2d()
    render_subregion_2d()
    render_fortbragg_2d()

    # render 3d maps
    render_region_3d()
    render_subregion_3d()
    render_fortbragg_3d()

    atexit.register(cleanup)
    sys.exit(0)


def render_region_2d():
    """2D rendering of region"""

    # create rendering directory
    render = os.path.join(gisdbase, 'images', 'sample_data')
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region', region='region', res=res)

    # render shaded relief maps
    for year in years:
        gscript.run_command('d.mon',
            start=driver,
            width=width+border,
            height=height,
            output=os.path.join(render, 'elevation_'+str(year)+'.png'),
            overwrite=overwrite)
        gscript.run_command('d.rast',
            map='shaded_relief_'+str(year))
        gscript.run_command('d.legend',
            raster='elevation_'+str(year),
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

    # render landforms
    for year in years:
        gscript.run_command('d.mon',
            start=driver,
            width=width+border+border,
            height=height,
            output=os.path.join(render, 'landforms_'+str(year)+'.png'),
            overwrite=overwrite)
        gscript.run_command('d.shade',
            shade='skyview_'+str(year),
            color='landforms_'+str(year),
            brighten=0)
        gscript.run_command('d.legend',
            raster='landforms_'+str(year),
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

    # render differences 2004-2016
    gscript.run_command('d.mon',
        start=driver,
        width=width+border,
        height=height,
        output=os.path.join(render, 'difference_2004_2016.png'),
        overwrite=overwrite)
    gscript.run_command('d.rast',
        map='difference_2004_2016')
    gscript.run_command('d.legend',
        raster='difference_2004_2016',
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)


    # render differences 2004-2012
    gscript.run_command('d.mon',
        start=driver,
        width=width+border,
        height=height,
        output=os.path.join(render, 'difference_2004_2012.png'),
        overwrite=overwrite)
    gscript.run_command('d.rast',
        map='difference_2004_2012')
    gscript.run_command('d.legend',
        raster='difference_2004_2012',
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)


    # render differences 2012-2016
    gscript.run_command('d.mon',
        start=driver,
        width=width+border,
        height=height,
        output=os.path.join(render, 'difference_2012_2016.png'),
        overwrite=overwrite)
    gscript.run_command('d.rast',
        map='difference_2012_2016')
    gscript.run_command('d.legend',
        raster='difference_2012_2016',
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # render water depth
    gscript.run_command('d.mon',
        start=driver,
        width=width+border,
        height=height,
        output=os.path.join(render, 'depth_2016.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='skyview_2016',
        color='depth_2016',
        brighten=0)
    gscript.run_command('d.legend',
        raster='depth_2016',
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # render imagery
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'naip_2014.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='skyview_2016',
        color='naip_2014',
        brighten=0)
    gscript.run_command('d.mon', stop=driver)

    # render landcover
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'landcover.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='skyview_2016',
        color='landcover',
        brighten=0)
    gscript.run_command('d.legend',
        raster='landcover',
        fontsize=fontsize,
        at=legend_coord,
        flags='n')
    gscript.run_command('d.mon', stop=driver)

def render_subregion_2d():

    # create rendering directory
    render = os.path.join(gisdbase, 'images', 'sample_data')
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region', region='subregion', res=res)

    # render shaded relief maps
    for year in years:
        gscript.run_command('d.mon',
            start=driver,
            width=width+border,
            height=height,
            output=os.path.join(render, 'gully_elevation_'+str(year)+'.png'),
            overwrite=overwrite)
        gscript.run_command('d.rast',
            map='shaded_relief_'+str(year))
        gscript.run_command('d.legend',
            raster='elevation_'+str(year),
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

    # render landforms
    for year in years:
        gscript.run_command('d.mon',
            start=driver,
            width=width+border+border,
            height=height,
            output=os.path.join(render, 'gully_landforms_'+str(year)+'.png'),
            overwrite=overwrite)
        gscript.run_command('d.shade',
            shade='skyview_'+str(year),
            color='landforms_'+str(year),
            brighten=0)
        gscript.run_command('d.legend',
            raster='landforms_'+str(year),
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

    # render difference 2004-2016
    gscript.run_command('d.mon',
        start=driver,
        width=width+border,
        height=height,
        output=os.path.join(render, 'gully_difference_2004_2016.png'),
        overwrite=overwrite)
    gscript.run_command('d.rast',
        map='difference_2004_2016')
    gscript.run_command('d.legend',
        raster='difference_2004_2016',
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # render difference 2004-2012
    gscript.run_command('d.mon',
        start=driver,
        width=width+border,
        height=height,
        output=os.path.join(render, 'gully_difference_2004_2012.png'),
        overwrite=overwrite)
    gscript.run_command('d.rast',
        map='difference_2004_2012')
    gscript.run_command('d.legend',
        raster='difference_2004_2012',
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # render difference 2012-2016
    gscript.run_command('d.mon',
        start=driver,
        width=width+border,
        height=height,
        output=os.path.join(render, 'gully_difference_2012_2016.png'),
        overwrite=overwrite)
    gscript.run_command('d.rast',
        map='difference_2012_2016')
    gscript.run_command('d.legend',
        raster='difference_2012_2016',
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)



def render_fortbragg_2d():

    # create rendering directory
    render = os.path.join(gisdbase, 'images', 'sample_data')
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region', region='fortbragg', res=10)

    # render shaded relief maps
    gscript.run_command('d.mon',
        start=driver,
        width=width+border,
        height=height,
        output=os.path.join(render, 'fortbragg_elevation.png'),
        overwrite=overwrite)
    gscript.run_command('d.rast',
        map='fortbragg_shaded_10m_2012')
    gscript.run_command('d.legend',
        raster='fortbragg_elevation_10m_2012',
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)


def render_region_3d():
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
    render = os.path.join(gisdbase, 'images', 'sample_data_3d')
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region',
                        region='region',
                        res=res)

    # list of 2004 rasters to render
    rasters_2004 = ['colorized_skyview_2004',
        'landforms_2004']

    # list of 2012 rasters to render
    rasters_2012 = ['colorized_skyview_2012',
        'landforms_2012',
        'difference_2004_2012']

    # list of 2016 rasters to render
    rasters_2016 = ['colorized_skyview_2016',
        'depth_2016',
        'landforms_2016',
        'naip_2014',
        'landcover',
        'difference_2004_2016',
        'difference_2012_2016']

    for raster in rasters_2004:
        # 3D render raster
        gscript.run_command('m.nviz.image',
            elevation_map='elevation_2004',
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

    for raster in rasters_2012:
        # 3D render raster
        gscript.run_command('m.nviz.image',
            elevation_map='elevation_2012',
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

    for raster in rasters_2016:
        # 3D render raster
        gscript.run_command('m.nviz.image',
            elevation_map='elevation_2016',
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

def render_subregion_3d():
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
    render = os.path.join(gisdbase, 'images', 'sample_data_3d')
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region',
                        region='subregion',
                        res=res)

    # list of 2004 rasters to render
    rasters_2004 = ['colorized_skyview_2004',
        'landforms_2004']

    # list of 2012 rasters to render
    rasters_2012 = ['colorized_skyview_2012',
        'landforms_2012',
        'difference_2004_2012']

    # list of 2016 rasters to render
    rasters_2016 = ['colorized_skyview_2016',
        'depth_2016',
        'landforms_2016',
        'naip_2014',
        'landcover',
        'difference_2004_2016',
        'difference_2012_2016']

    for raster in rasters_2004:
        # 3D render raster
        gscript.run_command('m.nviz.image',
            elevation_map='elevation_2004',
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

    for raster in rasters_2012:
        # 3D render raster
        gscript.run_command('m.nviz.image',
            elevation_map='elevation_2012',
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

    for raster in rasters_2016:
        # 3D render raster
        gscript.run_command('m.nviz.image',
            elevation_map='elevation_2016',
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

def render_fortbragg_3d():
    """3D rendering of fort bragg region with nviz"""

    # set 3d rendering parameters
    camera_height = 25000
    perspective = 14
    position = 1.0,1.0
    light_position = (0.68, -0.68, 0.95)
    fringe = "se"
    fringe_color = "85:250:182"
    fringe_elevation = 100
    size = (1600, 1200)
    zexag = 3

    # create rendering directory
    render = os.path.join(gisdbase, 'images', 'sample_data_3d')
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region',
                        region='fortbragg',
                        res=10)

    # 3D render elevation
    gscript.run_command('m.nviz.image',
        elevation_map='fortbragg_elevation_10m_2012',
        color_map='fortbragg_elevation_10m_2012',
        resolution_fine=1,
        height=camera_height,
        position=position,
        perspective=perspective,
        zexag=zexag,
        light_position=light_position,
        fringe=fringe,
        fringe_color=fringe_color,
        fringe_elevation=fringe_elevation,
        output=os.path.join(render,'fortbragg_elevation_2012'),
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
