# find discharge rate

r.slope.aspect elevation=elevation_2004@PERMANENT dx=dx dy=dy

r.sim.water --overwrite elevation=elevation_2004@PERMANENT dx=dx@traveltime dy=dy@traveltime depth=depth discharge=discharge nwalkers=2000000

r.info map=discharge@traveltime

mean velocity = 0.36833 m/s

# find travel time based on SIMWE

r.stream.distance

travel time = mean velocity (m/s) * distance (m)
184.165 s = 0.36833 m/s * 500 m

# find travel time with r.traveltime

g.extension extension=r.traveltime

r.mapcalc --overwrite expression=n = 0.01f

r.fill.dir --overwrite input=elevation_2004@PERMANENT output=temp_dem direction=temp_flowdir areas=problem_areas format=agnps

r.fill.dir --overwrite input=temp_dem output=depressionless_dem direction=depressionless_flowdir areas=problem_areas format=agnps

r.watershed -s -a elevation=depressionless_dem@traveltime accumulation=accumulation memory=3000

r.traveltime --overwrite dir=depressionless_flowdir@traveltime accu=accumulation@traveltime dtm=depressionless_dem@traveltime manningsn=n@traveltime out_x=597644.698747 out_y=150599.475605 threshold=50 b=2 nchannel=0.01 dis=60000000 slopemin=0.01 out=traveltime

r.info map=traveltime@traveltime

max travel time = 95 s

mean travel time = 60 s
