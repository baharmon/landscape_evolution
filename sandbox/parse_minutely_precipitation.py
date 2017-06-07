#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from collections import defaultdict
import csv
import pandas as pd
import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)

data_dir = input_file = os.path.join(os.path.dirname(__file__), 'precipitation', 'horticultural_crops_research_station', 'source_data')
output_dir = input_file = os.path.join(os.path.dirname(__file__), 'precipitation', 'horticultural_crops_research_station')
filenames = defaultdict(list)
years = range(2006,2017)

files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
for filename in files:
    year = filename[-9:-5]
    filenames[year].append(filename)

for year in years:

    output_file = os.path.join(output_dir, 'rain_events_{year}.csv'.format(year=year))

    # write new csv header
    with open(output_file, 'wb') as csvfile:
        write = csv.writer(csvfile,
                           delimiter=',',
                           quotechar='|',
                           quoting=csv.QUOTE_MINIMAL)
        write.writerow(['ob', 'precip'])

        filenamesbyyear = filenames['{year}'.format(year=year)]
        for input_filename in filenamesbyyear:
            input_file = os.path.join(data_dir, input_filename)

            data = pd.DataFrame()
            xls = pd.ExcelFile(input_file)

            for x in range(0, len(xls.sheet_names)):
                parsed_data = xls.parse(x,header = 0, parse_cols = 'A:B')
                data = data.append(parsed_data)

            minute = data.loc[data['precip'] >= 0.]
            minute['ob'] = pd.to_datetime(minute['ob'])
            minute.index = minute['ob']
            del minute['ob']

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
