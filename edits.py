"""REMOVED"""

#%rules
#% required: erdepmin,erdepmax,fluxmin,fluxmax,runoff,runoff_value,mannings,mannings_value,detachment,detachment_value,transport,transport_value,shearstress,shearstress_value,mass,mass_value,density,density_value
#% collective: runoff,runoff_value
#% collective: mannings,mannings_value
#% collective: detachment,detachment_value
#% collective: transport,transport_value
#% collective: shearstress,shearstress_value
#% collective: mass,mass_value
#% collective: density,density_value
#% collective: mass,density
#% collective: fluxmin,fluxmax
#% collective: erdepmin,erdepmax
#%end


"""ADDED"""
"""
runoff
mannings
detachment
transport
shearstress
mass
density
"""
#% required: no

"""
CHANGE ?
"""
Why did I need to recast rain_duration and rain_interval as int on line 631?

""" WARNINGS """ # OKAY
WARNING: Overwriting space time raster dataset <elevation_timeseries> and unregistering all maps
WARNING: Overwriting space time raster dataset <depth_timeseries> and unregistering all maps
WARNING: Overwriting space time raster dataset <erdep_timeseries> and unregistering all maps
WARNING: Overwriting space time raster dataset <flux_timeseries> and unregistering all maps

""" REINSTALL EXTENSION """
g.extension extension=r.evolution operation=add url=/Users/Brendan/landscape_evolution


""" RUN TEST """
r.evolution elevation=elevation@landscape_evolution precipitation=/Users/Brendan/landscape_evolution/precipitation.txt start="2015-10-06 00:00:00" walkers=10000 rain_intensity=155 rain_duration=60 rain_interval=1 temporaltype=absolute elevation_timeseries=elevation_timeseries


""" DEBUGGING """

ERROR: invalid literal for int() with base 10: '2015-10-06 00:01:00'
Traceback (most recent call last):
  File "/Users/Brendan/Library/GRASS/7.3/Modules/scripts/r.e
volution", line 778, in <module>
    main()
  File "/Users/Brendan/Library/GRASS/7.3/Modules/scripts/r.e
volution", line 387, in main
    elevation = event.rainfall_event()
  File "/Users/Brendan/Library/GRASS/7.3/Modules/scripts/r.e
volution", line 676, in rainfall_event
    gscript.run_command('t.register', type=raster,
input=self.depth_timeseries, maps=depth, start=evol.start,
increment=increment, flags='i', overwrite=True)
  File "/Applications/GRASS-7.3.app/Contents/MacOS/etc/pytho
n/grass/script/core.py", line 410, in run_command
    return handle_errors(returncode, returncode, args,
kwargs)
  File "/Applications/GRASS-7.3.app/Contents/MacOS/etc/pytho
n/grass/script/core.py", line 329, in handle_errors
    returncode=returncode)
grass.exceptions.CalledModuleError: Module run None
['t.register', '--o', '-i',
'maps=depth_2015_10_06_00_02_00', 'type=raster',
'input=depth_timeseries', 'increment=1 minutes',
'start=2015-10-06 00:01:00'] ended with error
Process ended with non-zero return code 1. See errors in the
(error) output.
elevation_2015_10_06_00_01_00
2015-10-06 00:01:00
(Mon Sep  5 17:47:53 2016) Command finished (1 min 43 sec)


"""<---NOTES ON THIS BUG..."""
all strds except elevation_timeseries are empty!

ERROR: invalid literal for int() with base 10: '2015-10-06 00:01:00'

t.register -i --overwrite input=depth_timeseries@landscape_evolution maps=depth_2015_10_06_00_02_00 start="2015-10-06 00:01:00" increment="1 minutes"

't.register', '--o', '-i', 'maps=depth_2015_10_06_00_02_00', 'type=raster', 'input=depth_timeseries', 'increment=1 minutes', 'start=2015-10-06 00:01:00'





""" DEBUGGING rainfall_series"""
TODO
