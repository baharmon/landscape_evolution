
""" REINSTALL EXTENSION """
g.extension extension=r.evolution operation=add url=/Users/Brendan/landscape_evolution
g.extension extension=r.evolution operation=add url=/Users/baharmon/landscape_evolution

""" RUN TEST """
r.evolution elevation=elevation@landscape_evolution precipitation=/Users/Brendan/landscape_evolution/precipitation.txt start="2015-10-06 00:00:00" walkers=10000 rain_intensity=155 rain_duration=60 rain_interval=1 temporaltype=absolute elevation_timeseries=elevation_timeseries


""" DEBUGGING """


""" TODO """
rainfall_event input parameters
