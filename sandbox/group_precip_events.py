#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from collections import defaultdict
import csv
import pandas as pd
import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)

records_2006_2012 = 'rain_events_2006_2012.csv'
records_2013_2016 = 'rain_events_2013_2016.csv'
records_2006_2016 = 'rain_events_2006_2016.csv'

period_1 = range(2006,2013)
period_2 = range(2013,2017)
period_3 = range(2006,2017)


filenames = defaultdict(list)

years = range(2006,2017)

data_dir = input_file = os.path.join(os.path.dirname(__file__), 'precipitation', 'horticultural_crops_research_station')

files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]

for filename in files:
    year = filename[-8:-4]
    filenames[year].append(filename)

filenamesbyyear = filenames['{year}'.format(year=year)]


output_file = os.path.join(data_dir, records_2006_2012)
# write new csv header
with open(output_file, 'wb') as csvfile:
    write = csv.writer(csvfile,
                       delimiter=',',
                       quotechar='|',
                       quoting=csv.QUOTE_MINIMAL)
    write.writerow(['ob', 'precip'])

#        for year in period_1:

    for input_filename in filenamesbyyear:
        input_file = os.path.join(data_dir, input_filename)
        print input_file

        with open(input_file, 'rb') as incsvfile:
            read = csv.reader(incsvfile, delimiter=' ', quotechar='|')
            for row in read:
                print row
                write.writerow(row)

#            with open(input_file, 'rb') as incsvfile:
#                read = csv.reader(incsvfile,
#                                  delimiter=',',
#                                  quotechar='|',
#                                  quoting=csv.QUOTE_MINIMAL)
#                # check for header
#                has_header = csv.Sniffer().has_header(incsvfile.read(1024))
#                # rewind
#                incsvfile.seek(0)
#                # skip header
#                if has_header:
#                    next(incsvfile)
#                # parse time and precipitation
#                precip = csv.reader(incsvfile, delimiter=',', skipinitialspace=True)
#                for row in precip:
#                    write.writerow(row)

