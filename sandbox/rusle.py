"""
E = R.K.L.S.C.P
where
E is average annual soil loss in ton/(acre.year) = 0.2242kg/(m2.year) = 2.242ton/(ha.year),
R is rainfall factor in (hundreds of ft-tonf.in)/(acre.hr.year) = 17.02(MJ.mm)/(ha.hr.year),
K is soil erodibility factor in (ton acre.hr)/(hundreds of acre ft-tonf.in) = 0.1317(ton.ha.hr)/(ha.MJ.mm),
LS is a dimensionless topographic (length-slope) factor,
C is a dimensionless land cover factor, and
P is a dimensionless prevention measures factor.

The modified 3D topographgic factor LS3D, representing topographic potential for erosion at a point on the hillslope, is a function of the upslope contributing area per unit width and the slope angle:

LS = (m + 1) (U/22.1)^m (sin β/0.09)^n
where
U is the upslope area per unit width (measure of water flow) in meters (m^2/m),
β is the slope angle in degree,
22.1 is the length of the standard USLE plot in meters,
0.09 = 9% = 5.15◦ is the slope of the standard USLE plot.
The values of exponents range for m = 0.2 − 0.6 and n = 1.0 − 1.3, where the lower values are used for prevailing sheet flow and higher values for prevailing rill flow.
"""

"""RUSLE 3D"""
# simple detachment limited
# LS = (m + 1) (U/22.1)^m (sin β/0.09)^n

        # compute dimensionless topographic factor
        gscript.run_command('r.mapcalc',
            expression="{ls_factor} = ({m} + 1.0) * (({flowacc} / 22.1)^ {m}) * ((sin({slope}) / 0.09)^{n})".format(ls_factor=ls_factor,
                m=self.m,
                flowacc=depth,
                slope=slope,
                n=self.n),
            overwrite=True)

        # compute sediment flow at sediment transport capacity
        gscript.run_command('r.mapcalc',
            expression="{sedflow} = {r_factor} * {k_factor} * {c_factor} * {ls_factor}".format(r_factor=r_factor,
                k_factor=self.k_factor,
                c_factor=self.c_factor,
                ls_factor=ls_factor
                sedflow=sedflow),
            overwrite=True)

"""toggle"""
            if self.mode == "rusle_mode":
                evolved_elevation, time, depth, erosion_deposition, sediment_flux, difference = evol.rusle()


"""USPED"""

        # LST = U^m.(sinβ)^n
        # T = R.K.C.P.U^m.(sinβ)^n
        # m = 0.2 − 0.6
        # n = 1.0 − 1.3
        # lower values are used for prevailing sheet flow
        # higher values for prevailing rill flow.

        # new variables = ls_factor, self.m, self.n
