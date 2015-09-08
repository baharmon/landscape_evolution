# -*- coding: utf-8 -*-

"""
@brief: landscape evolution model for gully formation

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

# TO DO:
#
# allow choice of maps or constants as inputs
# convert both maps and constants' units
# option to compute mannings from difference between dem and dsm
# run the procedure in a series based on storm data
# use temporal framework to save as strds
# create modules

from grass.script import core as gcore

import landscape_evolution as evolution

# set input digital elevation model
dem='dem'

# set model parameters
walkers=6500000  # max walkers = 7000000

# set landscape parameters
runoff=0.25 # runoff coefficient
mannings=0.1 # manning's roughness coefficient
# 0.03 for bare earth
# 0.04 for grass or crops
# 0.06 for shrubs and trees
# 0.1 for forest
detachment=0.001 # detachment coefficient
transport=0.01 # transport coefficient
shearstress=0 # shear stress coefficient
density=1.4 # sediment mass density in g/cm^3

# set minimum and maximum values for sediment flux
fluxmin=-1 # kg/ms
fluxmax=1 # kg/ms

# set temporal parameters
datatype='strds'
temporaltype='absolute'
strds='landscape_evolution_timeseries'
title="landscape evolution timeseries"
description="timeseries of digital elevation models simulated using a process-based landscape evolution model"
raster='raster'
start="2009-01-01 12:00"
increment="1 hours"

# create a raster space time dataset
gcore.run_command('t.create', type=datatype, temporaltype=temporaltype, output=strds, title=title, description=description)

# register the initial digital elevation model
gcore.run_command('t.register', type=raster, input=strds, maps=dem, start=start, increment=increment, flags='i')





# set rainfall parameter
rainintensity=155 # mm/hr
stormduration=10 # minutes

# run model
evolution.landscape(dem=dem, walkers=walkers, rainintensity=rainintensity, stormduration=stormduration, runoff=runoff, mannings=mannings, detachment=detachment, transport=transport, shearstress=shearstress, density=density, fluxmin=fluxmin, fluxmax=fluxmax)
