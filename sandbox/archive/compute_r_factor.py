def compute_r_factor(self):
    """compute event-based erosivity (R) factor (MJ mm ha^-1 hr^-1)"""

    # assign variables
    rain_energy = 'rain_energy'
    rain_volume = 'rain_volume'
    erosivity = 'erosivity'
    r_factor = 'r_factor'

    # derive rainfall energy (MJ ha^-1 mm^-1)
    gscript.run_command('r.mapcalc',
        expression="{rain_energy} = 0.29*(1.-(0.72*exp(-0.05*{rain_intensity})))".format(rain_energy=rain_energy,
            rain_intensity=self.rain_intensity),
        overwrite=True)

    # derive rainfall volume (mm) = rainfall intensity (mm/hr) * (rainfall interval (min) * (1 hr / 60 min))
    gscript.run_command('r.mapcalc',
        expression="{rain_volume} = {rain_intensity}*({rain_interval}/60.)".format(rain_volume=rain_volume,
            rain_intensity=self.rain_intensity,
            rain_interval=self.rain_interval),
        overwrite=True)

    # derive event erosivity index (MJ mm ha^-1 hr^-1)
    gscript.run_command('r.mapcalc',
        expression="{erosivity} = ({rain_energy}*{rain_volume})*{rain_intensity}*1.".format(erosivity=erosivity,
            rain_energy=rain_energy,
            rain_volume=rain_volume,
            rain_intensity=self.rain_intensity),
        overwrite=True)

    # multiply by rainfall interval in seconds (MJ mm ha^-1 hr^-1 s^-1)
    gscript.run_command('r.mapcalc',
        expression="{r_factor} = {erosivity}/({rain_interval}*60.)".format(r_factor=r_factor,
            erosivity=erosivity,
            rain_interval=self.rain_interval),
        overwrite=True)

    # remove temporary maps
    gscript.run_command('g.remove',
        type='raster',
        name=['rain_energy',
            'rain_volume',
            'erosivity'],
        flags='f')

    return r_factor
