#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SCRIPT:    design_storm.py

AUTHOR(S): Brendan Harmon <brendan.harmon@gmail.com>

PURPOSE:   Interpolate values for design storms

COPYRIGHT: (C) 2017 Brendan Harmon

           This program is free software under the GNU General Public
           License (>=v2). Read the file COPYING that comes with GRASS
           for details.
"""

# docs: https://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html

import numpy as np
import csv
import os

# assign variables
interval = 3 # minutes
duration = 60 # minutes
min_precip = 1 # mm
max_precip = 60 # mm
year = 2015
month = 01
day = 01
hour = 00
second = 00

filename = os.path.join(
    os.path.dirname(__file__),
    'design_storms',
    'design_storm_{interval}m.txt'.format(
        interval=interval))

# interpolate values
precipitation = np.linspace(
    max_precip, min_precip, num=duration/interval, endpoint=True) # precipitation in m
time = np.linspace(
    0, duration-interval, num=duration/interval, endpoint=True) # time in minutes


# open csv file
with open(filename, 'wb') as csvfile:
    write = csv.writer(csvfile,
                       delimiter=',',
                       quotechar='|',
                       quoting=csv.QUOTE_MINIMAL)

    # write new csv header
    write.writerow(['Date/Time (EST)', 'Precipitation (mm)'])

    # write interpolated values

    for counter, value in enumerate(range(0,duration,interval)):
        write.writerow([
            '{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}'.format(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=int(time[counter]),
                second=second),
            precipitation[counter]])
