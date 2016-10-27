""" Compute event based R factor from rainfall data """

from math import exp

rain_intensity = 50. # mm/hr
rain_interval = 15. # minutes

# derive rainfall energy (MJ ha^-1 mm^-1)
rain_energy = 0.29*(1-(0.72*exp(-0.05*rain_intensity)))

# derive rainfall volume (mm) = rainfall intensity (mm/hr) * (rainfall interval (min) * (1 hr / 60 min))
rain_volume = rain_intensity*(rain_interval/60.)

# derive event erosivity index (MJ mm ha^-1 hr^-1)
erosivity = rain_energy*rain_volume*rain_intensity

print "rain_energy = {rain_energy}".format(rain_energy=rain_energy)
print "rain_volume = {rain_volume}".format(rain_volume=rain_volume)
print "erosivity = {erosivity}".format(erosivity=erosivity)

""" convert to kg/ms """

k_factor = 0.3 # (ton ha hr / ha MJ mm)
ton_to_kg = 1000
ha_to_m2 = 10000

print erosivity * k_factor / ha_to_m2 * ton_to_kg

print erosivity * k_factor / ha_to_m2 * ton_to_kg / rain_interval*60


"""
# Cooley 1980
fD = 2.119*(rain_interval**0.0086)
# regression coefficents
a = 17.90
b = 0.4134
# single storm erosion index (MJ mm ha^-1 h^-1)
single_storm_erosivity = (a*(rain_volume**fD))/(rain_interval**b)

print "single_storm_erosivity = {single_storm_erosivity}".format(single_storm_erosivity=single_storm_erosivity)
"""


"""
# Yin et al. 2007

# derive rainfall kinetic energy (MJ ha^-1)
kinetic_energy = 0.29*(1-(0.72*exp(-0.05*rain_intensity)))*rain_volume

print "kinetic_energy = {kinetic_energy}".format(kinetic_energy=kinetic_energy)

"""
