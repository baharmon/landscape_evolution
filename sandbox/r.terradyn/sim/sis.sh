# SIS (SIMWE Iteration Slave) shell script for iterative SIMWE runs with elevation modification
# All SIMWE parameter definitions are done here and are therefore fixed for each loop
#
# run r.sim.water and r.sim.sediment with
# niter=1000, outiter=1000
# diffc 0.8 - prepare for iterations for initial elevation change shell scripts
#
r.sim.water -t elevin=elev.6 dxin=eldx.6 dyin=eldy.6 rain=rain01@helena inf=infil0@helena manin=man05@helena diffc=0.8 disch=$1.disch depth=$1.depth nwalk=400000 niter=1000 outiter=1000 

r.sim.sediment -t elevin=elev.6 wdepth=$1.depth.00999 dxin=eldx.6 dyin=eldy.6 detin=det001@helena tranin=tran001@helena tauin=tau01@helena manin=man05@helena diffc=0.8 flux=$1.flux erdep=$1.erdep tc=c0107b.tc et=$1.et niter=1000 outiter=1000

# compute change in elevation
r.mapcalc $1.del_elev.6=-1000.0*$1.erdep

# remove excessive gradients (-1<erdep<1)
# later, this should be governed by water depth in excess of, say, 20cm (shallow water no longer applies)
r.mapcalc $1.del_elev.6=if"($1.erdep>1, 1, $1.erdep)"

r.mapcalc $1.del_elev.6=if"($1.erdep<-1, -1, $1.erdep)"

# now smooth the delta(z) only (not the original elev.6)
# size=9 matches well with original localized terrain variability (size should be at least 3)
r.neighbors input=$1.del_elev.6 output=$1.del_elev_smooth.6 method=average size=9

# compute new elevation and store as ...itX_elev... where itX is iteration #X
r.mapcalc $1.it$2_elev.6=elev.6+$1.del_elev.6

# assign elev.6 the new elevation for the next iteration in the master shell
# NOTE: original elev.6 is stored in the helena mapset and as elev.6.original in chris mapset
# NOTE: All previously generated files (i.e. c0107b.disch) will be replaced each iteration
r.mapcalc elev.6=1.0*$1.it$2_elev.6

# compute slopes
r.slope.aspect elevation=elev.6 dx=eldx_temp.6 dy=eldy_temp.6

# correct edge NULLs by assigning the original values of elev.6.original to the boundary locations
# this will be fixed later (we'll see if this works over iterations)
r.mapcalc eldx.6=if"(isnull(eldx_temp.6), eldx.6.original, eldx_temp.6)"

r.mapcalc eldy.6=if"(isnull(eldy_temp.6), eldy.6.original, eldy_temp.6)"





