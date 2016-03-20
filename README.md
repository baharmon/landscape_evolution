# r.evolution
A short term landscape evolution using a path sampling method to solve water and sediment flow continuity equations and model mass flows over complex topographies.

#TODO
Develop as grass add-on module
Return depth, erdep, and difference
Register depth, erdep, difference, and flux in temporal framework
Optional outputs: depth, erdep, flux, difference, net_difference
Create new functions for rainfall_flux and series_flux
Allow choice of maps or constants as inputs
Rain as list, input parameters, or maps
Time as list or input parameters
Convert both maps and constants' units
Test by experimenting with different dems and parameters
Test with uav timeseries
Test with field data
Empirically calibrate parameters
Create documentation
Write an article

#ADD-ON TODO
Use r.sim.water as a guide for g.parser parameters
Run r.sim.water --script in the command line to show parameters
Manual page for g.parser: https://grass.osgeo.org/grass70/manuals/g.parser.html
Parser standard options: https://grass.osgeo.org/grass71/manuals/parser_standard_options.html
Guidelines for add-ons: https://trac.osgeo.org/grass/wiki/Submitting/Python
Create tabs in gui with #% guisection: Input
Set alternative requirements with  #%rules #% required: key_1, key_2 #%end

#CLEANUP TODO
Remove process.py
Remove dynamics.py
Keep evolution.py for running as script
