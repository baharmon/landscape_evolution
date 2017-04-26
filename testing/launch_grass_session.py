#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

grass7bin_mac = '/Applications/GRASS-7.3.app/'
# grass7bin_mac = '/Applications/GRASS-7.3.app/Contents/MacOS/grass73'

# define GRASS DATABASE
gisdb = os.path.join(os.path.expanduser("~"), "grassdata")

# specify (existing) location and mapset
location = "nc_spm_evolution"
mapset   = "PERMANENT"

# query GRASS 7 itself for its GISBASE
startcmd = [grass7bin_mac, '--config', 'path']

p = subprocess.Popen(startcmd, shell=False,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
if p.returncode != 0:
    print >>sys.stderr, "ERROR: Cannot find GRASS GIS 7 start script (%s)" % startcmd
    sys.exit(-1)
gisbase = out.strip('\n\r')

# Set GISBASE environment variable
os.environ['GISBASE'] = gisbase
# the following not needed with trunk
os.environ['PATH'] += os.pathsep + os.path.join(gisbase, 'extrabin')
# add path to GRASS addons
home = os.path.expanduser("~")
os.environ['PATH'] += os.pathsep + os.path.join(home, '.grass7', 'addons', 'scripts')

# define GRASS-Python environment
gpydir = os.path.join(gisbase, "etc", "python")
sys.path.append(gpydir)

# Set GISDBASE environment variable
os.environ['GISDBASE'] = gisdb

# import GRASS Python bindings (see also pygrass)
import grass.script as gscript
import grass.script.setup as gsetup

# launch session
gsetup.init(gisbase,
            gisdb, location, mapset)

gscript.message('Current GRASS GIS 7 environment:')
print gscript.gisenv()

gscript.message('Available raster maps:')
for rast in gscript.list_strings(type = 'rast'):
    print rast

gscript.message('Available vector maps:')
for vect in gscript.list_strings(type = 'vect'):
    print vect
