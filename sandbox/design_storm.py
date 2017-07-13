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

import numpy as np
import csv
import os

# assign variables
interval = 3 # minutes
duration = 60 # minutes
min_precip = 0.3 # mm
max_precip = 60 # mm
year = 2016
month = 01
day = 01
hour = 00
second = 00

filename = os.path.join(
    os.path.dirname(__file__),
    'design_storm.txt'.format(
        interval=interval))

# # linearly interpolate precipitation
# precipitation = np.linspace(
#     max_precip, min_precip, num=duration/interval, endpoint=True)

# logarithmically interpolate precipitation
precipitation = np.logspace(
    np.log10(max_precip), np.log10(min_precip), num=duration/interval)

# linearly interpolate time
time = np.linspace(
    0, duration-interval, num=duration/interval, endpoint=True)

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
