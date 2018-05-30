[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

# r.evolution
A short term landscape evolution using a path sampling method to solve water and sediment flow continuity equations to model mass flows over complex topographies. Implemented as an add-on for [GRASS GIS](https://grass.osgeo.org/), a free open source GIS.

## About
A dynamic, process-based landscape evolution model using simulated erosion and deposition to generate a timeseries of digital elevation models in GRASS GIS. This is a simple, fine-scale, short term landscape evolution model using a path sampling method to solve water and sediment flow continuity equations and model mass flows over complex topographies based on topographic, land cover, soil, and rainfall parameters. This either steady state or dynamic model can simulate landscape evolution for a range of hydrologic soil erosion regimes. The GRASS modules [r.sim.water](https://grass.osgeo.org/grass73/manuals/r.sim.water.html) and [r.sim.sediment](https://grass.osgeo.org/grass73/manuals/r.sim.sediment.html) are used to simulate erosion and deposition. The change in elevation is a function of time, net erosion-deposition, and sediment mass density. This module can also simulate landscape evolution based on the RUSLE3D and USPED soil erosion models.

change in elevation (m) = change in time (s) * net erosion-deposition (kg/m^2s) / sediment mass density (kg/m^3)

## Installation
* Launch GRASS GIS
* Install using the GRASS Console / Command Line Interface (CLI) with *g.extension r.evolution url=github.com/baharmon/landscape_evolution*
* Launch from the CLI with *r.evolution --ui*

## Sample dataset
Clone or download the
[sample dataset](https://github.com/baharmon/landscape_evolution_dataset)
with a time series of lidar-based digital elevation models
and orthoimagery
for a highly eroded watershed near Patterson Branch Creek, Fort Bragg, NC, USA.

## License
GNU General Public License >= version 2
