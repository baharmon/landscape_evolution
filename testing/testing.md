# EXTENSION
g.extension r.evolution url=github.com/baharmon/landscape_evolution

# RUN SCRIPT
/Users/baharmon/landscape_evolution/testing/simulations.py

# FATRA
ssh -Y baharmon@fatra.cnr.ncsu.edu
mkdir grassdata
exit
scp /Users/Brendan/Downloads/nc_spm_evolution.zip baharmon@fatra.cnr.ncsu.edu:grassdata/nc_spm_evolution.zip
ssh -X baharmon@fatra.cnr.ncsu.edu
cd grassdata
unzip nc_spm_evolution.zip
rm nc_spm_evolution.zip
git clone https://github.com/baharmon/landscape_evolution.git
cp ~/landscape_evolution/testing/{design_storm_1m.txt,design_storm_2m.txt,design_storm_3m.txt} ~/grassdata/nc_spm_evolution
grass-trunk
g.extension r.sim.water.mp
landscape_evolution/testing/decadal_simulations.py
landscape_evolution/testing/simulations_06_22_2017.py
top
exit

# TODO
Troubleshoot RUSLE
Run steady state simulations
Run event based simulations for 1 min intervals for 3 hrs parameterized to generate +-1m elevation change
Run series based SIMWE simulations with design storm with 1 min intervals for 1 hr
Run 2 year simulation
Run 12 year simulation
