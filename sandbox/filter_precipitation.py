#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import pandas as pd
import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)


for year in range(2006,2016):

    input_file = os.path.join(os.path.dirname(__file__), 'precipitation', 'Harmon_Lake_Minute', 'LAKE_Minute_{year}.csv'.format(year=year))
    output_file = os.path.join(os.path.dirname(__file__), 'precipitation', 'rain_events', 'rain_events_{year}.csv'.format(year=year))

    # write new csv header
    with open(output_file, 'wb') as csvfile:
        write = csv.writer(csvfile,
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL)
        write.writerow(['ob', 'precip'])

        data = pd.read_csv(input_file.format(year=year),
            iterator=True,
            chunksize=1000)
        minute = pd.concat([chunk[chunk['precip'] >= 0.] for chunk in data])
        minute['ob'] = pd.to_datetime(minute['ob'])
        minute.index = minute['ob']
        del minute['ob']
        del minute['station']

        buffer = []
        counter = 0
        for row in minute.itertuples():
            value = float(row[1])
            if value >= 0.01:
                new_row = [row[0],value * 25.4]
                buffer.append(new_row)
                counter = len(buffer)
            else:
                if counter >= 30:
                    for buffer_row in buffer:
                        write.writerow(buffer_row)
                buffer = []
                counter = 0
