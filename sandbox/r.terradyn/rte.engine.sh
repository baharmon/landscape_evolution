# *********************************************************************************
#
# rte0131.sh (r.terradyn.engine) - called by r.terradyn script.
# Updates terrain based on SIMWE erdep and modified Exner equation.
# Assumes predefined region and existing mapsets with required inputs.
#
# C.S. Thaxton, NCSU
#
# INPUT ARGUMENTS:
#   $1: name       - name assigned to output (should be unique)
#   $2: numiter    - number of terrain change iterations
#   $3: dzthresh   - SIMWE niter
#   $4: smoothsize - SIMWE nwalkers
#   $5: dtoverrhob - bulk density (i.e. 0.1/0.4=0.25)
#   $6: grdiff     - gravitational diffusion term (select 0 to turn this off)
#                    (select 1 to turn off $9 and $10)
#   $7: niter      - band-pass averaging span (e.g. 25)
#   $8: alpha      - band-pass attenuation scalar (e.g. 0.5)
#   $9: sigma      - band-pass threshold (e.g. 0.01) - proportional to dt/rho
#
# INPUT FILES: These files must uniquely exist in an accessible mapset:
#   SIMWE inputs: elin, dxin, dyin, rainin, infilin(0), manin, tauin, detin, tranin
#   rte.sh inputs: el.initial, dx.initial, dy.initial, tran.initial
#   NOTE: elin, dxin, dyin, and (possibly) tranin are modified at each rte.sh iteration
#
# OUTPUT FILES: Produces a time series of as "name_numiter.***" where *** is:
#   SIMWE: disch, depth, flux, erdep, tc, et
#   rte.sh: del_elev, truncp, truncn, del_elev_smooth, elev
#
# *********************************************************************************
#
echo "*** Calling r.sim.water2"
echo " "
echo "--nwalkers            = $4"
echo "--niter               = $3"
echo " "
echo "    running..."
r.sim.water2 elevin=elin dxin=dxin dyin=dyin rain=rainin inf=infilin manin=manin diffc=0.3 halpha=10 disch=$1.$2.disch depth=$1.$2.depth nwalk=$4 niter=$3 outiter=$3
echo " "
echo "*** Calling r.sim.sediment2" 
echo " "
echo "--nwalkers            = $4"
echo "--niter               = $3"
echo " "
echo "    running..."
r.sim.sediment2 elevin=elin wdepth=$1.$2.depth dxin=dxin dyin=dyin detin=detin tranin=tranin tauin=tauin manin=manin diffc=0.3 flux=$1.$2.flux erdep=$1.$2.erdep tc=r.terradyn.tc et=r.terradyn.et nwalk=$4 niter=$3 outiter=$3
echo " "
echo "*** Computing initial elevation change request..."
echo " "
# NOTE: *.flux is qs
echo "--dt/rho              = $5"
#
# Compute slope and aspect from t-1 to derive divergence of qs*s-hat 
# (s-hat is unit vector of steepest slope defined by the aspect angles)
r.slope.aspect elevation=elin aspect=r.terradyn.aspect zfactor=0.3048
#
# Fix boundaries
r.neighbors input=r.terradyn.aspect output=temp.aspect method=sum size=3
r.mapcalc temp.aspect="0.33333*temp.aspect"
r.mapcalc r.terradyn.aspect="if(isnull(r.terradyn.aspect),temp.aspect,r.terradyn.aspect)"
#
r.mapcalc qsx="$1.$2.flux*cos(r.terradyn.aspect)"
r.mapcalc qsy="$1.$2.flux*sin(r.terradyn.aspect)"
r.slope.aspect elevation=qsx dx=dqsxdx
r.slope.aspect elevation=qsy dy=dqsydy
# Correct for -dx and -dy (not for CVS version)
# r.mapcalc dqsxdx="-1.0*dqsxdx"
# r.mapcalc dqsydy="-1.0*dqsydy"
#
# Fix boundaries
r.neighbors input=dqsxdx output=temp.dqsxdx method=sum size=3
r.mapcalc temp.dqsxdx="0.33333*temp.dqsxdx"
r.mapcalc dqsxdx="if(isnull(dqsxdx),temp.dqsxdx,dqsxdx)"
r.neighbors input=dqsydy output=temp.dqsydy method=sum size=3
r.mapcalc temp.dqsydy="0.33333*temp.dqsydy"
r.mapcalc dqsydy="if(isnull(dqsydy),temp.dqsydy,dqsydy)"
#
r.mapcalc delqs="dqsxdx+dqsydy"
# r.mapcalc temp.elev="-1.0*$5*0.5*delqs"
r.mapcalc temp.elev="$5*0.5*delqs"
#
# HELENA:
# PROBLEM HAS JUST OCCURRED: IT IS IN THE EXNER
# EQUATION ABOVE
#
echo " "
echo "*** Applying band-pass filter"
echo " "
echo "--span of averaging   = $7"
echo "--alpha(attentuation) = $8"
echo "--sigma(threshold)    = $9"
#
r.neighbors input=temp.elev output=ave.elev method=average size=$7
r.mapcalc osc.elev="temp.elev-ave.elev"
r.mapcalc osc.sign="if(osc.elev>0,1,-1)"
r.mapcalc mod.elev="ave.elev+$8*osc.elev+(1-$8)*osc.sign*$9"
echo " "
echo "*** Computing change in elevation..."
echo " "
r.mapcalc $1_$2.elev="elin+temp.elev"
echo " "
echo "*** Applying gravitational diffusion"
echo " "
echo "--dt/rho              = $5"
echo "--grav. diffusion     = $6"
#
r.mapcalc pregrav.elev="1.0*$1_$2.elev"
r.slope.aspect elevation=$1_$2.elev dxx=dzdxx dyy=dzdyy zfactor=0.3048
# Correct for -dxx and -dyy (not needed for CVS version)
r.mapcalc dzdxx="-1.0*dzdxx"
r.mapcalc dzdyy="-1.0*dzdyy"
# Fix boundaries
r.neighbors input=dzdxx output=temp.dzdxx method=sum size=3
r.mapcalc temp.dzdxx="0.33333*temp.dzdxx"
r.neighbors input=dzdyy output=temp.dzdyy method=sum size=3
r.mapcalc temp.dzdyy="0.33333*temp.dzdyy"
r.mapcalc dzdxx="if(isnull(dzdxx), temp.dzdxx, dzdxx)"
r.mapcalc dzdyy="if(isnull(dzdyy), temp.dzdyy, dzdyy)"
r.mapcalc del2z="dzdxx+dzdyy"
#
r.mapcalc $1_$2.elev="$1_$2.elev-$5*$6*0.5*del2z"
#
# echo " "
# echo "*** Smoothing del(z)..."
# echo " "
# r.neighbors input=$1_$2.elev output=$1_$2.elev method=average size=3
echo " "
echo "*** Computing and assigning elevation for next iteration..."
echo " "
r.mapcalc elin="1.0*$1_$2.elev"
#
# For evaluation of relative effect of grav diff term.
r.mapcalc $1_$2.omega="delqs/del2z"
r.mapcalc $1_$2.omega="if(abs($1_$2.omega)<$6,abs($1_$2.omega),$6)"
echo " "
echo "*** Computing new slopes for next iteration..."
echo " "
r.slope.aspect elevation=elin dx=eldx dy=eldy zfactor=0.3048
# Correct for -dx and -dy (not for CVS version)
# r.mapcalc eldx="-1.0*eldx"
# r.mapcalc eldy="-1.0*eldy"
# Fix boundaries
r.neighbors input=eldx output=temp.eldx method=sum size=3
r.mapcalc temp.eldx="0.33333*temp.eldx"
r.neighbors input=eldy output=temp.eldy method=sum size=3
r.mapcalc temp.eldy="0.33333*temp.eldy"
r.mapcalc dxin="if(isnull(eldx), temp.eldx, eldx)"
r.mapcalc dyin="if(isnull(eldy), temp.eldy, eldy)"
#
echo " "
echo "*** Iteration $2 of $1 complete...moving on..."
echo " "
