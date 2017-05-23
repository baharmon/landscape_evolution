#!/bin/bash

GRASS=/Applications/GRASS-7.3.app/Contents/MacOS/grass73

GRASSDATA=~baharmon/grassdata/nc_spm_evolution/event_erdep

$GRASS $GRASSDATA --exec g.copy raster=elevation_30cm_2013@PERMANENT,elevation

$GRASS $GRASSDATA --exec g.region raster=elevation res=0.3

# $GRASS $GRASSDATA --exec g.extension r.evolution url=github.com/baharmon/landscape_evolution

# $GRASS $GRASSDATA --exec r.evolution elevation=elevation runs=event rain_duration=30 start="2013-01-01 00:00:00" rain_interval=1 overwrite=True

# $GRASS $GRASSDATA --exec /testing/render.py
