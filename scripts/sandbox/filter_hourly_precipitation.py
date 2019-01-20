#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import pandas as pd
import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)

input_file = os.path.join(os.path.dirname(__file__),
    'precipitation',
    'Harmon_NFBR_Hourly_Precip_2011-2016.txt')
output_file = os.path.join(os.path.dirname(__file__),
    'precipitation',
    'rain_events_2011_2016.csv')

# write new csv header
with open(output_file, 'wb') as csvfile:
    write = csv.writer(csvfile,
        delimiter=',',
        quotechar='|',
        quoting=csv.QUOTE_MINIMAL)
    write.writerow(['ob', 'precip'])

    data = pd.read_csv(input_file,
        iterator=True,
        chunksize=1000)
    minute = pd.concat([chunk[chunk['precip'] >= 0.] for chunk in data])
    minute['ob'] = pd.to_datetime(minute['ob'])
    minute.index = minute['ob']
    del minute['ob']

    buffer = []
    counter = 0
    for row in minute.itertuples():
        value = float(row[1])
        if value >= 0.1:
            new_row = [row[0],value * 25.4]
            write.writerow(new_row)

