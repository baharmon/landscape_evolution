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
res=1

# set 2D rendering parameters
legend_coord = (2, 32, 2, 4)
border = 400
width = 1600
height = 1600
font = 'Lato-Regular'
fontsize = 26
vector_width = 3

# set data parameters
years = [2004, 2012, 2016]

flux_colors = """\
0 255:255:255
0.001 255:255:0
0.1 255:127:0
1 191:127:63
100% 0:0:0
nv 255:255:255
default 255:255:255
"""

lsfactor_colors = """\
0 white
0.01 #FFFFD6
0.02 #FDD995
0.1 #FD993E
0.4 #D86026
1 #983517
100% #652915
"""

def main():

    """render 2d maps"""
    render_region_2d()
    render_subregion_2d()
    # render_map_elements()
    # render_fortbragg_2d()

    """render 3d maps"""
    # render_region_3d()
    # render_legends()
    # render_fortbragg_3d()

    atexit.register(cleanup)
    sys.exit(0)


def render_region_2d():
    """2D rendering of region"""

    # create rendering directory
    render = os.path.join(gisdbase, 'images', 'sample_data')
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region', region='region', res=res, align='elevation_2012')

    for year in years:
        # compute skyview
        gscript.run_command('r.skyview',
            input='elevation_'+str(year),
            output='skyview_'+str(year),
            ndir=16,
            colorized_output='colorized_skyview_'+str(year),
            overwrite=overwrite)

        # compute partial derivatives
        gscript.run_command('r.slope.aspect',
            elevation='elevation_'+str(year),
            dx='dx_'+str(year),
            dy='dy_'+str(year),
            overwrite=overwrite)

        # compute overland flow and erosion with SIMWE
        gscript.run_command('r.sim.water',
            elevation='elevation_'+str(year),
            dx='dx_'+str(year),
            dy='dy_'+str(year),
            man='mannings',
            depth='depth_'+str(year),
            nwalkers=1000000,
            output_step=1,
            niterations=10,
            nprocs=8,
            overwrite=overwrite)
        gscript.run_command('r.mapcalc',
            expression="detachment = 0.001",
            overwrite=True)
        gscript.run_command('r.mapcalc',
            expression="transport = 0.001",
            overwrite=True)
        gscript.run_command('r.mapcalc',
            expression="shear_stress = 0.0",
            overwrite=True)
        gscript.run_command('r.sim.sediment',
            elevation='elevation_'+str(year),
            water_depth='depth_'+str(year),
            dx='dx_'+str(year),
            dy='dy_'+str(year),
            detachment_coeff='detachment',
            transport_coeff='transport',
            shear_stress='shear_stress',
            man='mannings',
            sediment_flux='sediment_flux_'+str(year),
            erosion_deposition='erosion_deposition_'+str(year),
            nwalkers=1000000,
            output_step=1,
            nprocs=8,
            overwrite=overwrite)

    # compute flow accumulation and erosion with RUSLE3D
    for year in years:
        gscript.run_command('r.watershed',
            elevation='elevation_'+str(year),
            accumulation='flow_accumulation_'+str(year),
            flags='a',
            overwrite=overwrite)
        gscript.run_command('r.slope.aspect',
            elevation='elevation_'+str(year),
            slope='slope_'+str(year),
            overwrite=overwrite)
        gscript.run_command('r.mapcalc',
            expression="{ls_factor}"
            "=(0.4+1.0)"
            "*(({flow_accumulation}/22.1)^0.4)"
            "*((sin({slope})/5.14)^1.3)".format(
                ls_factor='ls_factor_'+str(year),
                flow_accumulation='flow_accumulation_'+str(year),
                slope='slope_'+str(year)),
            overwrite=True)
        gscript.run_command('r.mapcalc',
            expression="{flux}"
            "=310.0"
            "*{k_factor}"
            "*{ls_factor}"
            "*{c_factor}".format(
                flux='sediment_flow_'+str(year),
                k_factor='k_factor',
                ls_factor='ls_factor_'+str(year),
                c_factor='c_factor'),
            overwrite=True)
        # set color tables
        gscript.write_command(
            'r.colors',
            map='ls_factor_'+str(year),
            rules='-',
            stdin=lsfactor_colors)
        gscript.write_command(
            'r.colors',
            map='sediment_flow_'+str(year),
            rules='-',
            stdin=flux_colors)

    # set mask
    gscript.run_command('r.mask', vector='watershed')

    # render map with imagery and subwatersheds
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'imagery_subwatersheds'+'.png'),
        overwrite=overwrite)
    gscript.run_command('d.rast',
        map='naip_2014')
    gscript.run_command('d.vect',
        map='subwatersheds',
        fill_color='none',
        width=3)
    gscript.run_command('d.vect',
        map='watershed',
        fill_color='none',
        width=6)
    gscript.run_command('d.mon', stop=driver)

    # render map with depth and subwatershed
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'depth_subwatersheds'+'.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief_2012',
        color='depth_2012',
        brighten=0)
    gscript.run_command('d.vect',
        map='subwatershed',
        fill_color='none',
        width=6)
    gscript.run_command('d.legend',
        raster='depth_2012',
        font=font,
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # render map with flow accumlation and subwatershed
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'flowacc_subwatersheds'+'.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief_2012',
        color='flow_accumulation_2012',
        brighten=0)
    gscript.run_command('d.vect',
        map='subwatershed',
        fill_color='none',
        width=6)
    gscript.run_command('d.legend',
        raster='flow_accumulation_2012',
        font=font,
        fontsize=fontsize,
        at=legend_coord,
        flags='nl')
    gscript.run_command('d.mon', stop=driver)

    # render map with subwatersheds
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'subwatersheds'+'.png'),
        overwrite=overwrite)
    gscript.run_command('d.vect',
        map='subwatersheds',
        fill_color='none',
        width=3)
    gscript.run_command('d.vect',
        map='watershed',
        fill_color='none',
        width=6)
    gscript.run_command('d.mon', stop=driver)

    # render map with subwatershed
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'subwatershed'+'.png'),
        overwrite=overwrite)
    gscript.run_command('d.vect',
        map='subwatershed',
        fill_color='none',
        width=6)
    gscript.run_command('d.mon', stop=driver)

    # render shaded relief maps
    for year in years:
        gscript.run_command('d.mon',
            start=driver,
            width=width,
            height=height,
            output=os.path.join(render, 'elevation_'+str(year)+'.png'),
            overwrite=overwrite)
        gscript.run_command('r.relief',
            input='elevation_'+str(year),
            output='relief_'+str(year),
            altitude=90,
            azimuth=45,
            zscale=3,
            overwrite=overwrite)
        gscript.run_command('d.shade',
            shade='relief_'+str(year),
            color='elevation_'+str(year),
            brighten=5,
            overwrite=overwrite)
        gscript.run_command('d.legend',
            raster='elevation_'+str(year),
            font=font,
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

    # render landforms
    for year in years:
        gscript.run_command('d.mon',
            start=driver,
            width=width,
            height=height,
            output=os.path.join(render, 'landforms_'+str(year)+'.png'),
            overwrite=overwrite)
        gscript.run_command('r.geomorphon',
            elevation='elevation_'+str(year),
            forms='landforms_'+str(year),
            search=64,
            skip=0,
            flat=1,
            dist=0,
            step=0,
            start=0,
            overwrite=overwrite)
        gscript.run_command('d.rast',
            map='landforms_'+str(year))
        gscript.run_command('d.legend',
            raster='landforms_'+str(year),
            font=font,
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

    # render differences 2012-2016
    gscript.run_command('d.mon',
        start=driver,
        width=width,
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
        width=width,
        height=height,
        output=os.path.join(render, 'depth_2012.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief_2012',
        color='depth_2012',
        brighten=0)
    gscript.run_command('d.legend',
        raster='depth_2012',
        font=font,
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
        shade='relief_2012',
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
        shade='relief_2012',
        color='landcover',
        brighten=0)
    gscript.run_command('d.legend',
        raster='landcover',
        font=font,
        fontsize=fontsize,
        at=legend_coord,
        flags='n')
    gscript.run_command('d.mon', stop=driver)

    # render flow accumulation
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'flow_accumulation_2012.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief_2012',
        color='flow_accumulation_2012',
        brighten=0)
    gscript.run_command('d.legend',
        raster='flow_accumulation_2012',
        font=font,
        fontsize=fontsize,
        at=legend_coord,
        flags='nl')
    gscript.run_command('d.mon', stop=driver)

    # render ls factor
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'ls_factor.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief_2012',
        color='ls_factor_2012',
        brighten=0)
    gscript.run_command('d.legend',
        raster='ls_factor_2012',
        font=font,
        fontsize=fontsize,
        at=legend_coord,
        label_values=[0.001,1.8],
        label_step=0.5)
    gscript.run_command('d.mon', stop=driver)

    # render sediment flow
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'sediment_flow_2012.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief_2012',
        color='sediment_flow_2012',
        brighten=0)
    gscript.run_command('d.legend',
        raster='sediment_flow_2012',
        font=font,
        fontsize=fontsize,
        at=legend_coord,
        range='0,3')
    gscript.run_command('d.mon', stop=driver)

    # render sediment flux
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'sediment_flux_2012.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief_2012',
        color='sediment_flux_2012',
        brighten=0)
    gscript.run_command('d.legend',
        raster='sediment_flux_2012',
        font=font,
        fontsize=fontsize,
        at=legend_coord,
        range='0,1',
        digits='2',
        flags='n')
    gscript.run_command('d.mon', stop=driver)

    # render erosion deposition
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'erosion_deposition_2012.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief_2012',
        color='erosion_deposition_2012',
        brighten=0)
    gscript.run_command('d.legend',
        raster='erosion_deposition_2012',
        font=font,
        fontsize=fontsize,
        at=legend_coord,
        range='-0.1,0.1',
        digits='2',
        flags='n')
    gscript.run_command('d.mon', stop=driver)

    # remove mask
    gscript.run_command('r.mask', flags='r')

    # remove temporary maps
    gscript.run_command(
        'g.remove',
        type='raster',
        name=['dx'+str(year),
            'dy'+str(year),
            'detachment',
            'transport',
            'shear_stress'],
        flags='f')


def render_subregion_2d():
    """2D rendering of region"""

    # create rendering directory
    render = os.path.join(gisdbase, 'images', 'sample_data_detail')
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region',
        region='subregion',
        res=res,
        align='elevation_2012')

    # set mask
    gscript.run_command('r.mask', vector='subwatershed')

    # render shaded relief maps
    for year in years:
        gscript.run_command('d.mon',
            start=driver,
            width=width,
            height=height,
            output=os.path.join(render, 'elevation_'+str(year)+'.png'),
            overwrite=overwrite)
        gscript.run_command('d.shade',
            shade='relief_'+str(year),
            color='elevation_'+str(year),
            brighten=0)
        gscript.run_command('d.legend',
            raster='elevation_'+str(year),
            font=font,
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

    # render landforms
    for year in years:
        gscript.run_command('d.mon',
            start=driver,
            width=width,
            height=height,
            output=os.path.join(render, 'landforms_'+str(year)+'.png'),
            overwrite=overwrite)
        gscript.run_command('d.shade',
            shade='relief_'+str(year),
            color='landforms_'+str(year),
            brighten=0)
        gscript.run_command('d.legend',
            raster='landforms_'+str(year),
            font=font,
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

    # render differences 2004-2016
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'difference_2004_2016.png'),
        overwrite=overwrite)
    gscript.run_command('d.rast',
        map='difference_2004_2016')
    gscript.run_command('d.legend',
        raster='difference_2004_2016',
        font=font,
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # render differences 2004-2012
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'difference_2004_2012.png'),
        overwrite=overwrite)
    gscript.run_command('d.rast',
        map='difference_2004_2012')
    gscript.run_command('d.legend',
        raster='difference_2004_2012',
        font=font,
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # render differences 2012-2016
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'difference_2012_2016.png'),
        overwrite=overwrite)
    gscript.run_command('d.rast',
        map='difference_2012_2016')
    gscript.run_command('d.legend',
        raster='difference_2012_2016',
        font=font,
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # render water depth
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'depth_2012.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief_2012',
        color='depth_2012',
        brighten=0)
    gscript.run_command('d.legend',
        raster='depth_2012',
        font=font,
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
        shade='relief_2012',
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
        shade='relief_2012',
        color='landcover',
        brighten=0)
    gscript.run_command('d.legend',
        raster='landcover',
        font=font,
        fontsize=fontsize,
        at=legend_coord,
        flags='n')
    gscript.run_command('d.mon', stop=driver)

    # render flow accumulation
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'flow_accumulation_2012.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief_2012',
        color='flow_accumulation_2012',
        brighten=0)
    gscript.run_command('d.legend',
        raster='flow_accumulation_2012',
        font=font,
        fontsize=fontsize,
        at=legend_coord,
        flags='nl')
    gscript.run_command('d.mon', stop=driver)

    # render ls factor
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'ls_factor.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief_2012',
        color='ls_factor_2012',
        brighten=0)
    gscript.run_command('d.legend',
        raster='ls_factor_2012',
        font=font,
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # render sediment flow
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'sediment_flow_2012.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief_2012',
        color='sediment_flow_2012',
        brighten=0)
    gscript.run_command('d.legend',
        raster='sediment_flow_2012',
        font=font,
        fontsize=fontsize,
        at=legend_coord,
        range='0,3')
    gscript.run_command('d.mon', stop=driver)

    # render sediment flux
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'sediment_flux_2012.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief_2012',
        color='sediment_flux_2012',
        brighten=0)
    gscript.run_command('d.legend',
        raster='sediment_flux_2012',
        font=font,
        fontsize=fontsize,
        at=legend_coord,
        range='0,1',
        digits='2',
        flags='n')
    gscript.run_command('d.mon', stop=driver)

    # render erosion deposition
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'erosion_deposition_2012.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief_2012',
        color='erosion_deposition_2012',
        brighten=0)
    gscript.run_command('d.legend',
        raster='erosion_deposition_2012',
        font=font,
        fontsize=fontsize,
        at=legend_coord,
        range='-0.1,0.1',
        digits='2',
        flags='n')
    gscript.run_command('d.mon', stop=driver)

    # remove mask
    gscript.run_command('r.mask', flags='r')



def render_fortbragg_2d():

    # create rendering directory
    render = os.path.join(gisdbase, 'images', 'sample_data')
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region',
        region='fortbragg',
        res=10,
        align='fortbragg_elevation_10m_2012')

    # set mask
    gscript.run_command('r.mask', raster='fortbragg_cfactor')

    # render shaded relief maps
    gscript.run_command('d.mon',
        start=driver,
        width=width*2,
        height=height,
        output=os.path.join(render, 'fortbragg_elevation.png'),
        overwrite=overwrite)
    gscript.run_command('d.rast',
        map='fortbragg_shaded_10m_2012')
    gscript.run_command('d.legend',
        raster='fortbragg_elevation_10m_2012',
        font=font,
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # compute relief
    gscript.run_command('r.relief',
        input='fortbragg_elevation_10m_2012',
        output='relief',
        altitude=90,
        azimuth=45,
        zscale=3,
        overwrite=overwrite)

    # render c factor
    gscript.run_command('d.mon',
        start=driver,
        width=width*2,
        height=height,
        output=os.path.join(render, 'fortbragg_cfactor.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief',
        color='fortbragg_cfactor',
        brighten=0)
    gscript.run_command('d.legend',
        raster='fortbragg_cfactor',
        font=font,
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # render landcover
    gscript.run_command('d.mon',
        start=driver,
        width=width*2,
        height=height,
        output=os.path.join(render, 'fortbragg_landcover.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief',
        color='fortbragg_landcover',
        brighten=0)
    gscript.run_command('d.legend',
        raster='fortbragg_landcover',
        fontsize=fontsize,
        font=font,
        at=legend_coord,
        flags='n')
    gscript.run_command('d.mon', stop=driver)

    # render landcover
    gscript.run_command('d.mon',
        start=driver,
        width=width*2,
        height=height,
        output=os.path.join(render, 'fortbragg_erdep.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief',
        color='fortbragg_erdep',
        brighten=0)
    gscript.run_command('d.legend',
        raster='fortbragg_erdep',
        font=font,
        fontsize=fontsize,
        at=legend_coord)
    gscript.run_command('d.mon', stop=driver)

    # render landcover
    gscript.run_command('d.mon',
        start=driver,
        width=width*2,
        height=height,
        output=os.path.join(render, 'fortbragg_classified_erdep.png'),
        overwrite=overwrite)
    gscript.run_command('d.shade',
        shade='relief',
        color='fortbragg_classified_erdep',
        brighten=0)
    gscript.run_command('d.legend',
        raster='fortbragg_classified_erdep',
        font=font,
        fontsize=fontsize,
        at=legend_coord,
        flags='n')
    gscript.run_command('d.mon', stop=driver)

    # remove mask
    gscript.run_command('r.mask', flags='r')


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
    vwidth = 3

    # create rendering directory
    render = os.path.join(gisdbase, 'images', 'sample_data_3d')
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region',
        region='region',
        align='elevation_2016',
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
        'erosion_deposition_2016',
        'flow_accumulation_2016',
        'ls_factor',
        'sediment_flow_2016',
        'sediment_flux_2016',
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

    for raster in rasters_2012:
        # 3D render raster
        gscript.run_command('m.nviz.image',
            elevation_map='elevation_2012',
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

    for raster in rasters_2016:
        # 3D render raster
        gscript.run_command('m.nviz.image',
            elevation_map='elevation_2016',
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


def render_legends():
    """render raster map legends"""

    # create rendering directory
    render = os.path.join(gisdbase, 'images', 'sample_data_3d')
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region',
        region='region',
        align='elevation_2016',
        res=res)

    # mask rasters
    gscript.run_command('r.mask', vector='watershed')

    # export legends
    gscript.run_command('r.out.legend',
        raster='elevation_2016',
        file=os.path.join(render,'legend_elevation.png'),
        filetype='cairo',
        dimensions=[0.8,6],
        resolution=300,
        color='none',
        digits=3,
        font='Lato-Regular',
        overwrite=overwrite)
    gscript.run_command('r.out.legend',
        raster='depth_2016',
        file=os.path.join(render,'legend_depth.png'),
        filetype='cairo',
        dimensions=[0.8,6],
        resolution=300,
        color='none',
        range=[0,1],
        digits=3,
        font='Lato-Regular',
        overwrite=overwrite)
    gscript.run_command('r.out.legend',
        raster='difference_2012_2016',
        file=os.path.join(render,'legend_difference.png'),
        filetype='cairo',
        dimensions=[0.8,6],
        resolution=300,
        color='none',
        digits=4,
        font='Lato-Regular',
        overwrite=overwrite)
    gscript.run_command('r.out.legend',
        raster='erosion_deposition_2016',
        file=os.path.join(render,'legend_erosion_deposition.png'),
        filetype='cairo',
        dimensions=[0.8,6],
        resolution=300,
        color='none',
        range=[-0.25,0.25],
        digits=4,
        font='Lato-Regular',
        overwrite=overwrite)
    gscript.run_command('r.out.legend',
        raster='sediment_flux_2016',
        file=os.path.join(render,'legend_flux.png'),
        filetype='cairo',
        dimensions=[0.8,6],
        resolution=300,
        color='none',
        range=[0,25],
        digits=3,
        font='Lato-Regular',
        overwrite=overwrite)
    gscript.run_command('r.out.legend',
        raster='sediment_flow_2016',
        file=os.path.join(render,'legend_flux.png'),
        filetype='cairo',
        dimensions=[0.8,6],
        resolution=300,
        color='none',
        range=[0,0.25],
        digits=3,
        font='Lato-Regular',
        overwrite=overwrite)
    gscript.run_command('r.out.legend',
        raster='slope_2016',
        file=os.path.join(render,'legend_slope.png'),
        filetype='cairo',
        dimensions=[0.8,6],
        resolution=300,
        color='none',
        range=[0,90],
        digits=3,
        font='Lato-Regular',
        overwrite=overwrite)
    gscript.run_command('r.out.legend',
        raster='landforms_2016',
        file=os.path.join(render,'legend_landforms.png'),
        filetype='cairo',
        dimensions=[0.8,6],
        resolution=300,
        color='none',
        digits=3,
        font='Lato-Regular',
        overwrite=overwrite)

    # remove mask
    gscript.run_command('r.mask', flags='r')


def render_map_elements():
    """render a scale bar and north arrow"""

    # create rendering directory
    render = os.path.join(gisdbase, 'images', 'sample_data')
    if not os.path.exists(render):
        os.makedirs(render)

    # set region
    gscript.run_command('g.region', region='region', res=res)
    # render map scale bar and north arrow
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'map_elements'+'.png'),
        overwrite=overwrite)
    gscript.run_command('d.northarrow',
        style='6',
        at='90.0,10.0',
        flags='t')
    gscript.run_command('d.barscale',
        at='63,5.0',
        segment=2,
        fontsize=fontsize)
    gscript.run_command('d.mon', stop=driver)

    # set subregion
    gscript.run_command('g.region', region='subregion', res=res)
    # render map scale bar and north arrow
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, 'map_elements_detail'+'.png'),
        overwrite=overwrite)
    gscript.run_command('d.northarrow',
        style='6',
        at='90.0,10.0',
        flags='t')
    gscript.run_command('d.barscale',
        at='63,5.0',
        segment=2,
        fontsize=fontsize)
    gscript.run_command('d.mon', stop=driver)


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
