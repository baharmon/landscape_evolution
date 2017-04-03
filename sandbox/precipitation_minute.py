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
        cells_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        cells_writer.writerow(['ob', 'precip'])

        data = pd.read_csv(input_file.format(year=year), iterator=True, chunksize=1000)
        #minute = pd.concat([chunk[chunk['precip'] >= 0.01] for chunk in data])
        minute = pd.concat([chunk[chunk['precip'] >= 0.] for chunk in data])
        minute['ob'] = pd.to_datetime(minute['ob'])
        minute.index = minute['ob']
        del minute['ob']

        buffer = []
        counter = 0
        for row in minute.itertuples():
            print row
            value = row[2]
            print value
            #value = row['precip']
            if value >= 0.01:
                value * 25.4
                buffer.append(row)
                counter = len(buffer)
            else:
                if counter >= 30:
                    # write buffer to output_file
                    cells_writer.writerow(buffer)

                buffer = []
                counter = 0

#    minute_mm = minute
#    minute_mm['precip'] = minute['precip'] * 25.4
#    minute_mm.to_csv(output_file, sep=',', encoding='utf-8') # index=False, header=False

#for row in minute.iterrows():
#    print row['c1'], row['c2']
#
#for row in minute.itertuples():
#    print row[1]
#
#row[1] * 2 for row in df.itertuples()

#    buffer = []
#    counter = 0
#    for row in minute:
#        value = row['precip']
#        if value >= 0.01:
#            value * 25.4
#            buffer.append(row)
#            counter = len(buffer)
#        else:
#            if counter >= 30:
#                # write buffer to output_file
#                cells_writer.writerow(buffer)