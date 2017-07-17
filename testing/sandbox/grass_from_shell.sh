#!/bin/bash

GRASS=/Applications/GRASS-7.3.app/Contents/MacOS/grass73

GRASSDATA=grassdata/nc_spm_evolution/PERMANENT

$GRASS $GRASSDATA --exec landscape_evolution/testing/sandbox/map_production.py

# $GRASS $GRASSDATA --exec g.extension r.evolution url=github.com/baharmon/landscape_evolution

# $GRASS $GRASSDATA --exec g.region raster=elevation_2012 res=1

# $GRASS $GRASSDATA --exec r.evolution elevation=elevation_2012 runs=event rain_duration=30 start="2013-01-01 00:00:00" rain_interval=1 overwrite=True

# $GRASS $GRASSDATA --exec /testing/render.py

# /Applications/GRASS-7.3.app/Contents/MacOS/grass73 /Users/Brendan/grassdata/nc_spm_evolution/PERMANENT --gui
