
""" REINSTALL EXTENSION """
g.extension extension=r.evolution operation=add url=/Users/Brendan/landscape_evolution
g.extension extension=r.evolution operation=add url=/Users/baharmon/landscape_evolution

""" RUN TEST """
r.evolution elevation=elevation@landscape_evolution precipitation=/Users/Brendan/landscape_evolution/precipitation.txt start="2015-10-06 00:00:00" walkers=10000 rain_intensity=155 rain_duration=60 rain_interval=1 temporaltype=absolute elevation_timeseries=elevation_timeseries


""" DEBUGGING """
Traceback (most recent call last):
  File "/Users/Brendan/Library/GRASS/7.3/Modules/scripts/r.e
volution", line 1215, in <module>
    main()
  File "/Users/Brendan/Library/GRASS/7.3/Modules/scripts/r.e
volution", line 465, in main
    elevation = event.rainfall_event()
  File "/Users/Brendan/Library/GRASS/7.3/Modules/scripts/r.e
volution", line 819, in rainfall_event
    evolved_elevation, time, depth, erosion_deposition,
sediment_flux, difference = evol.flux()
  File "/Users/Brendan/Library/GRASS/7.3/Modules/scripts/r.e
volution", line 689, in flux
    gscript.run_command('r.sim.sediment',
elevation=self.elevation, water_depth=depth, dx=dx, dy=dy,
detachment_coeff=self.detachment,
transport_coeff=self.transport,
shear_stress=self.shearstress, man=self.mannings,
sediment_flux=flux, niterations=self.rain_interval,
nwalkers=self.walkers, overwrite=True)
NameError: global name 'flux' is not defined
