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
ssh -Y baharmon@fatra.cnr.ncsu.edu
mkdir grassdata
~.
scp /Users/Brendan/Downloads/nc_spm_evolution.zip baharmon@fatra.cnr.ncsu.edu:grassdata/nc_spm_evolution.zip
ssh -X baharmon@fatra.cnr.ncsu.edu
cd grassdata
unzip nc_spm_evolution.zip
rm nc_spm_evolution.zip
git clone https://github.com/baharmon/landscape_evolution.git
grass-trunk
landscape_evolution/testing/decadal_simulations.py
~.
