
""" REINSTALL EXTENSION """
g.extension extension=r.evolution operation=add url=/Users/Brendan/landscape_evolution
g.extension extension=r.evolution operation=add url=/Users/baharmon/landscape_evolution

""" RUN TEST """
r.evolution elevation=elevation@landscape_evolution precipitation=/Users/Brendan/landscape_evolution/precipitation.txt start="2015-10-06 00:00:00" walkers=10000 rain_intensity=155 rain_duration=60 rain_interval=1 temporaltype=absolute elevation_timeseries=elevation_timeseries

""" DEBUGGING """












""" alternative slope and aspect calculations """
#        # comute the slope and aspect
#        gscript.run_command('r.param.scale', input=self.elevation, output=slope, size=search_size, method="slope", overwrite=True)
#        gscript.run_command('r.param.scale', input=self.elevation, output=aspect, size=search_size, method="aspect", overwrite=True)

#        # comute the partial derivatives from the slope and aspect
#        # dz/dy = tan(slope)*sin(aspect)
#        gscript.run_command('r.mapcalc', expression="{dx} = tan({slope}* 0.01745)*cos((({aspect}*(-1))+450)*0.01745)".format(aspect=aspect, slope=slope, dx=dx), overwrite=True)
#        # dz/dy = tan(slope)*sin(aspect)
#        gscript.run_command('r.mapcalc', expression="{dy} = tan({slope}* 0.01745)*sin((({aspect}*(-1))+450)*0.01745)".format(aspect=aspect, slope=slope, dy=dy), overwrite=True)
