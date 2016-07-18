# r.evolution
A short term landscape evolution using a path sampling method to solve water and sediment flow continuity equations to model mass flows over complex topographies.
Implemented as an add-on for [GRASS GIS](https://grass.osgeo.org/), a free open source GIS.

## Installation
* Launch GRASS GIS
* Install using the GRASS Console / Command Line Interface with 'g.extension r.evolution.py url=github.com/baharmon/landscape_evolution'
* Or install using the GRASS GUI with the module g.extension under Settings/Addons Extensions/Install extension from addons
- extension = r.evolution.py
- operation = add
- url = github.com/baharmon/landscape_evolution

# Future work
##TODO
* Develop as grass add-on module
* Return depth, erdep, and difference
* Create elevation, depth, erdep, and difference strds with temporal framework
* Register depth, erdep, difference, and flux in temporal framework
* Optional outputs: depth, erdep, flux, difference, net_difference
- G_OPT_R_OUTPUT
* Create new functions for rainfall_flux and series_flux
* Allow choice of maps or constants as inputs
* Rain as list, input parameters, or maps
* Time as list or input parameters
* Convert both maps and constants' units
* Reverse landscape evolution
* Subsurface soil moisture
* Test by experimenting with different dems and parameters
* Test with uav timeseries
* Test with field data
* Empirically calibrate parameters
* Create documentation
* Write an article

##ADD-ON TODO
* Use r.sim.water as a guide for g.parser parameters
* Run r.sim.water --script in the command line to show parameters
* Manual page for g.parser: https://grass.osgeo.org/grass70/manuals/g.parser.html
* Parser standard options: https://grass.osgeo.org/grass71/manuals/parser_standard_options.html
* Guidelines for add-ons: https://trac.osgeo.org/grass/wiki/Submitting/Python
* Create tabs in gui with #% guisection: Input
* Set alternative requirements with  #%rules #% required: key_1, key_2 #%end
* Guide: https://github.com/wenzeslaus/python-grass-addon/blob/master/04_script_to_grass_module.ipynb
* Documentation (html)
* Compile (makefile)
- install with 'g.extension r.evolution url=github.com/baharmon/landscape_evolution'
* Style (PEP8)
* Alternative input types
- Standard input
- Text files
