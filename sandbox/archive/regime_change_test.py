#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@brief: testing regime change toggle

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

import os
import sys
import atexit
import grass.script as gscript
from grass.exceptions import CalledModuleError

# use temporary region
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

# assign local variables
sigma = 'sigma' # first order reaction term dependent on soil and cover properties (m^−1)
detachment = 'detachment'
transport = 'transport'

gscript.run_command('r.mapcalc',
    expression="{detachment} = 0.01".format(detachment=detachment),
    overwrite=True)
gscript.run_command('r.mapcalc',
    expression="{transport} = 1.0".format(transport=transport),
    overwrite=True)

# derive sigma
"""detachment capacity coefficient = sigma * transport capacity coefficient"""
gscript.run_command('r.mapcalc',
    expression="{sigma} = {detachment}/{transport}".format(sigma=sigma,
        detachment=detachment,
        transport=transport),
    overwrite=True)
info = gscript.parse_command('r.info',
    map=sigma,
    flags='r')
min_sigma = float(info['min'])
max_sigma = float(info['max'])

if max_sigma <= 0.01:
    regime = "detachment limited"
elif min_sigma >= 100.:
    regime = "transport limited"
else:
    regime = "erosion deposition"

#remove temporary maps
gscript.run_command('g.remove',
    type='raster',
    name=['sigma','detachment','transport'],
    flags='f')

print regime
