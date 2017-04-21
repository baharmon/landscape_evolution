#!/bin/bash

GRASSDATA=../grassdata/nc_spm_evolution/event_erdep

grass $GRASSDATA --exec g.copy raster=elevation_30cm_2013@PERMANENT,elevation

grass $GRASSDATA --exec g.region raster=elevation res=0.3

grass $GRASSDATA --exec r.evolution elevation=elevation runs=event rain_duration=30 start="2013-01-01 00:00:00" rain_interval=1
