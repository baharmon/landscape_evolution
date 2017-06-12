# EXTENSION
g.extension r.evolution url=github.com/baharmon/landscape_evolution

# LAUNCH GRASS
/Applications/GRASS-7.3.app/Contents/MacOS/grass73

# RUN SCRIPT
/Users/Brendan/landscape_evolution/testing/simulations.py
/Users/baharmon/landscape_evolution/testing/simulations.py

# PYTHON
/Users/Brendan/landscape_evolution/testing/launch_grass_session.py
/Users/baharmon/landscape_evolution/testing/launch_grass_session.py

# FATRA
scp -rC /Users/Brendan/grassdata/nc_spm_evolution baharmon@fatra.cnr.ncsu.edu:Downloads
scp /Users/Brendan/Downloads/nc_spm_evolution.zip baharmon@fatra.cnr.ncsu.edu:Downloads
ssh -X baharmon@fatra.cnr.ncsu.edu
scp -rC baharmon@fatra.cnr.ncsu.edu:Downloads/nc_spm_evolution /Users/Brendan/Downloads
