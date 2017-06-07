#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from collections import defaultdict
import csv
import pandas as pd
import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)

data_dir = input_file = os.path.join(os.path.dirname(__file__), 'precipitation', 'horticultural_crops_research_station')

filenames = defaultdict(list)

years = range(2006,2017)

files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]

for filename in files:
    year = filename[-9:-5]
    filenames[year].append(filename)

for year in years:
    filenamesbyyear = filenames['{year}'.format(year=year)]
    for input_filename in filenamesbyyear:
        input_file = os.path.join(data_dir, input_filename)
    output_file = os.path.join(data_dir, 'rain_events_{year}.csv'.format(year=year))
    print output_file

