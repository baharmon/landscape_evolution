# determine whether transport limited or detachment limited regime

if mode == "simwe_mode":
    regime = erosion_regime()

# or create function in DynamicEvolution class and call in rainfall_event and rainfall_series
    # def erosion_regime(self):
def erosion_regime(elevation, rain_intensity, runoff, rain_interval, mannings, walkers, shearstress, detachment, transport):
    """determine whether transport limited or detachment limited regime"""

    # assign local variables
    rho = 1000. # mass density of water (kg * m^-3)
    gravity = 9.81 # gravitational acceleration (m/s^2)
    # hydrostatic pressure with unit height
    # shearstress_exponent = 1.5
    critical_shearstress = 'critical_shearstress'
    sigma = 'sigma' # first order reaction term dependent on soil and cover properties (m^−1)

    # compute slope and partial derivatives
    gscript.run_command('r.slope.aspect',
        elevation=elevation,
        slope=slope,
        dx=dx,
        dy=dy,
        overwrite=True)

    # hyrdology parameters
    gscript.run_command('r.mapcalc',
        expression="{rain} = {rain_intensity}*{runoff}".format(rain=rain,
            rain_intensity=rain_intensity,
            runoff=runoff),
        overwrite=True)

    # hydrologic simulation
    gscript.run_command('r.sim.water',
        elevation=elevation,
        dx=dx,
        dy=dy,
        rain=rain,
        man=mannings,
        depth=depth,
        niterations=rain_interval,
        nwalkers=walkers,
        overwrite=True)

    gscript.run_command('r.mapcalc',
        expression="critical_shearstress = ({rho} * {gravity}) * {depth} * sin({slope})".format(rho=rho,
            gravity=gravity,
            depth=depth,
            slope=slope),
        overwrite=True)

    gscript.run_command('r.mapcalc',
        expression="sigma = if((({critical_shearstress} <= {shearstress}) || ({transport} == 0.)),0., ({detachment} / {transport}) * ({critical_shearstress} - {shearstress}) / ({critical_shearstress}^1.5))".format(critical_shearstress=critical_shearstress,
            shearstress=shearstress,
            transport=transport,
            detachment=detachment),
        overwrite=True)

    # detachment capacity = sigma * transport capacity
    # transport capacity >> detachment capacity when sigma -> 0
    # r.info -r
    univar = gscript.parse_command('r.univar',
        map=elevation,
        separator='newline',
        flags='g')
    mean_sigma = float(univar['mean'])
    if mean_sigma >= 0.001:
        regime = "detachment limited"
    else:
        regime = "transport limited"

    # remove temporary maps
    gscript.run_command('g.remove',
        type='raster',
        name=['slope',
            'dx',
            'dy',
            'rain',
            'depth',
            'critical_shearstress',
            'sigma'],
        flags='f')

    return regime



# add variable regime to classes
    # self.regime ?

if self.mode == "simwe_mode":
    if self.regime == "detachment limited":
        evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.flux()
    if self.regime == "transport limited":
        evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.erosion_deposition()













""" replace:
                if self.mode == "erosion_deposition_mode":
                    evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.erosion_deposition()

                if self.mode == "flux_mode":
                    evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.flux()


7	    int k, l;
378	    double zx, zy, zd2, zd4, sinsl;
379	    double cc, cmul2;
380	    double sheer;
381	    double vsum = 0.;
382	    double vmax = 0.;
383	    double chsum = 0.;
384	    double zmin = 1.e12;
385	    double zmax = -1.e12;
386	    double zd2min = 1.e12;
387	    double zd2max = -1.e12;
388	    double smin = 1.e12;
389	    double smax = -1.e12;
390	    double infmin = 1.e12;
391	    double infmax = -1.e12;
392	    double sigmax = -1.e12;
393	    double cchezmax = -1.e12;
394	    double rho = 1000.;
395	    double gravity= 9.81;
396	    double hh = 1.;
397	    double deltaw = 1.e12;
398
399	    sisum = 0.;
400	    infsum = 0.;
401	    cmul2 = rho * gacc;

    for (k = 0; k < my; k++) {
404	        for (l = 0; l < mx; l++) {
405	            if (zz[k][l] != UNDEF) {
406	                zx = v1[k][l];
407	                zy = v2[k][l];
408	                zd2 = zx * zx + zy * zy;
409	                sinsl = sqrt(zd2) / sqrt(zd2 + 1);      /* sin(terrain slope) */

                if (wdepth) {
438	                    sheer = (double)(cmul2 * gama[k][l] * sinsl);       /* shear stress */
439	                    /* if critical shear stress >= shear then all zero */
440	                    if ((sheer <= tau[k][l]) || (ct[k][l] == 0.)) {
441	                        si[k][l] = 0.;
442	                        sigma[k][l] = 0.;
443	                    }
444	                    else {
445	                        si[k][l] = (double)(dc[k][l] * (sheer - tau[k][l]));
446	                        sigma[k][l] = (double)(dc[k][l] / ct[k][l]) * (sheer - tau[k][l]) / (pow(sheer, 1.5));  /* rill erosion=1.5, sheet = 1.1 */
447	                    }
