#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)

for year in range(2006,2015):

    data = pd.read_csv('//Users//Brendan//landscape_evolution//sandbox//precipitation//Harmon_Lake_Minute//LAKE_Minute_{year}.csv'.format(year=year), iterator=True, chunksize=1000)
    minute = pd.concat([chunk[chunk['precip'] >= 0.03] for chunk in data])
    minute['ob'] = pd.to_datetime(minute['ob'])
    minute.index = minute['ob']
    del minute['ob']

    # convert from inches to mm
    minute_mm = minute
    minute_mm['precip'] = minute['precip'] * 25.4
    minute_mm.to_csv('//Users//Brendan//landscape_evolution//sandbox//precipitation//filtered_minute_mm//filtered_{year}.csv'.format(year=year), sep=',', encoding='utf-8') # index=False, header=False
