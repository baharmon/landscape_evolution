# TRANSPORT LIMITED
r.evolution elevation=elevation runs=event rain_duration=30 walkers=1000000 detachment_value=1 start="2013-01-01 00:00:00" rain_interval=1 temporaltype=absolute elevation_timeseries=elevation_timeseries

# TRANSPORT 1m
g.region res=1
r.evolution elevation=elevation runs=event rain_duration=30 walkers=100000 detachment_value=1 start="2013-01-01 00:00:00" rain_interval=1 temporaltype=absolute elevation_timeseries=elevation_timeseries
DONE!

# ERDEP
r.evolution elevation=elevation runs=event rain_duration=30 walkers=1000000 start="2013-01-01 00:00:00" rain_interval=1 temporaltype=absolute elevation_timeseries=elevation_timeseries

# ERDEP 1m
g.region res=1
r.evolution elevation=elevation runs=event rain_duration=30 walkers=100000 start="2013-01-01 00:00:00" rain_interval=1

# FLUX 1m
g.region res=1
r.evolution elevation=elevation runs=event rain_duration=30 walkers=100000 transport_value=1 start="2013-01-01 00:00:00" rain_interval=1 temporaltype=absolute elevation_timeseries=elevation_timeseries



# TODO

set c factor

test resolution

test smoothing
