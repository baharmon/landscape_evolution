#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grass.script as gscript
from grass.exceptions import CalledModuleError


r_factor = 'r_factor'
erosivity = 2.0
rain_interval = 1.0


# multiply by rainfall interval in seconds (MJ mm ha^-1 hr^-1 s^-1)
gscript.run_command(
    'r.mapcalc',
    expression="{r_factor} = {erosivity}/({rain_interval}*60.)".format(r_factor=r_factor,
        erosivity=erosivity,
        rain_interval=rain_interval),
    overwrite=True)

# multiply by rainfall interval in seconds (MJ mm ha^-1 hr^-1 s^-1)
gscript.run_command(
    'r.mapcalc',
    expression = "{r_factor}"
    "= {erosivity}"
    "/ ({rain_interval}"
    "* 60.)".format(r_factor=r_factor,
        erosivity=erosivity,
        rain_interval=rain_interval),
    overwrite=True)
