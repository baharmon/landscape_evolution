def erosion_regime(self):
    """determine whether transport limited or detachment limited regime"""

    # assign local variables
    sigma = 'sigma' # first order reaction term dependent on soil and cover properties (m^−1)

    # derive sigma
    """detachment capacity coefficient = sigma * transport capacity coefficient"""
    gscript.run_command('r.mapcalc',
        expression="{sigma} = {detachment}/{transport}".format(sigma=sigma,
            detachment=detachment,
            transport=transport),
        overwrite=True)
    info = gscript.parse_command('r.info',
        map=sigma,
        separator='newline',
        flags='r')
    min_sigma = float(info['min'])
    max_sigma = float(info['max'])

    # determine regime
    if min_sigma <= 0.001 and max_sigma <= 0.001:
        regime = "detachment limited"
    if min_sigma >= 100. and max_sigma >= 100.:
        regime = "transport limited"
    else:
        regime = "erosion deposition"

    # remove temporary maps
    gscript.run_command('g.remove',
        type='raster',
        name=['sigma'],
        flags='f')

    return regime
