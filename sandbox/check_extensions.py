#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grass.script as gscript
from grass.exceptions import CalledModuleError

threads = 2

# mp = gscript.find_program('r.sim.water.mp', '--help')
# print mp

if threads > 1 and gscript.find_program('r.sim.water.mp', '--help'):
    print 'run r.sim.water.mp'
