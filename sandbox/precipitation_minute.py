import pandas as pd
import datetime as dt
#import matplotlib.pyplot as pyplot
import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)

iter_csv = pd.read_csv('//Users//Brendan//landscape_evolution//sandbox//precipitation//Filtered_Minute//Minute_2015.csv', iterator=True, chunksize=1000)
#df = pd.concat([chunk[chunk['precip'] > 0.01] for chunk in iter_csv])
df = pd.concat([chunk[chunk['precip'] > 0.01] for chunk in iter_csv])

df['ob'] = pd.to_datetime(df['ob'])
df.index = df['ob']
del df['ob']

# df.to_csv('//Users//Brendan//landscape_evolution//sandbox//precipitation//Filtered_Minute//Filtered_2015.csv', sep=',', encoding='utf-8') # index=False, header=False

# find days with rain >= than 1"
daily = pd.DataFrame()
daily = (df.resample('D', how='sum')) #.notnull()
daily = daily.dropna(subset=['precip'])
daily = daily[daily['precip'] >= 1.0]
#print daily

# make list of days from daily
list_of_days = pd.Series(daily.index.format()).tolist()
#print df['2015-01-12']

# find minutes with rain >= 0.01"
# make list of days from daily
# locate only minutes with those days
# filter for precip >= 0.01

##minutes = df['precip'] > 0.01




## plot results
#df['2015-01-12'].resample('D', how='sum').plot()

# seabourn viz: http://chrisalbon.com/python/pandas_with_seaborn.html

df.to_csv('//Users//Brendan//landscape_evolution//sandbox//precipitation//Filtered_Minute//Filtered_2015.csv', sep=',', encoding='utf-8') # index=False, header=False
