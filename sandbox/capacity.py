

"""
sigma = Vs/2q

sigma = first order reaction term dependent on soil and cover properties [m^−1]
Vs = settling velocity [m/s]
q = flow discharge per unit width [(m^2)/s]
"""

"""
sigma = Dc/T

sigma = first order reaction term dependent on soil and cover properties [m^−1]
Dc = detachment capacity
T = transport capacity [kg/(ms)]
"""

"""
detachment capacity limited
Tc >> Dc when sigma -> 0
"""

# default: cecil soils
particle_size = 0.0066

settling_velocity = 2.81 * (particle_size^2)

q = 

sigma = settling_velocity / (2 * q)

sigma = detachment_capacity / transport_capacity




# settling velocity
"""
eroded particle size (D15) for cecil soils: 0.0066
if D15 > 0.01 mm then
Vs = 2.81d^2
Where:
Vs = settling velocity in ft/sec
d = particle diameter in mm
"""
# d15 = soil particle size in the 15th percentile




"""
The sources and sinks term is derived from the assumption that the detachment and
deposition rates are proportional to the difference between the sediment transport capacity
and the actual sediment flow rate [19]:
D(r) = σ(r)[T (r) − |qs(r)|] (12)
where T (r) [kg/(ms)] is the sediment transport capacity, σ(r) [m−1] is the first order reaction
term dependent on soil and cover properties. The expression for σ(r) = Dc(r)/T (r)
is obtained from the following relationship [19]:
D(r)/Dc(r) + |qs(r)|/T (r) = 1 (13)
The qualitative arguments, experimental observations, and values for σ(r) are discussed,
for example, by Foster and Meyer [19].
The sediment transport capacity T (r) and detachment capacity Dc(r)
"""

"""
If D15 is greater than or equal to 0.01 mm, then settling velocity should be found using:
log10Vs = -0.34246 (log10d)2 + 0.98912 (log10d) - 0.33801
Where:
Vs = settling velocity in ft/sec
d = particle diameter in mm (Wilson et al., 1982)
"""
