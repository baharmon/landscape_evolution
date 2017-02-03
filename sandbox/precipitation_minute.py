#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import datetime as dt
#import matplotlib.pyplot as pyplot
import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)

"""
filter for days with precip >= 1"
filter for minutes with rain >= 0.01"
"""

data = pd.read_csv('//Users//Brendan//landscape_evolution//sandbox//precipitation//Filtered_Minute//Minute_2015.csv', iterator=True, chunksize=1000)

minute = pd.concat([chunk[chunk['precip'] >= 0.01] for chunk in data])

minute['ob'] = pd.to_datetime(minute['ob'])
minute.index = minute['ob']
del minute['ob']

# df.to_csv('//Users//Brendan//landscape_evolution//sandbox//precipitation//Filtered_Minute//Filtered_2015.csv', sep=',', encoding='utf-8') # index=False, header=False

# find days with rain >= than 1"
daily = pd.DataFrame()
daily = (minute.resample('D', how='sum')) #.notnull()
#daily = daily.dropna(subset=['precip'])
daily = daily['precip'] >= 1.0
#daily = daily[daily['precip'] >= 1.0]
daily = daily.resample('T').ffill()
#print daily

##minutes = df['precip'] > 0.01

#filtered = pd.concat([minute, daily], axis=1)

#filtered = pd.merge(minute, daily, how='left', left_index=True, right_index=True) #, on='index'

#filtered = minute.merge(daily, how='left', left_index=True, right_index=True) #, on='index'

#print filtered

#print (minute['precip'] > 0.01) & daily.notnull()



## plot results
#df['2015-01-12'].resample('D', how='sum').plot()

# seabourn viz: http://chrisalbon.com/python/pandas_with_seaborn.html
# seabourn timeseries: http://chrisalbon.com/python/seaborn_pandas_timeseries_plot.html

minute.to_csv('//Users//Brendan//landscape_evolution//sandbox//precipitation//Filtered_Minute//Filtered_2015.csv', sep=',', encoding='utf-8') # index=False, header=False
